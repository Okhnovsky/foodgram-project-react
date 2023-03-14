from datetime import datetime as dt
from urllib.parse import unquote
from django.db.models import F, Sum
from django.http.response import HttpResponse
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import AmountIngredient, Ingredient, Recipe, Tag
from .extra_func import incorrect_layout

from .mixins import CreateDeleteViewMixin
from .paginator import PageLimitPagination
from .permissions import IsAdminOrReadOnly, IsAuthorStaffOrReadOnly
from .serializers import (UserSubscribeSerializer, TagSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShowRecipeSerializer,)


class UserViewSet(DjoserUserViewSet, CreateDeleteViewMixin):

    pagination_class = PageLimitPagination
    add_serializer = UserSubscribeSerializer

    @action(methods=('GET', 'POST', 'DELETE',), detail=True)
    def subscribe(self, request, id):
        """Метод для содания/удаления связи между пользователями."""
        return self.add_remove_relation(id, 'follow_M2M')

    @action(methods=('get',), detail=False)
    def subscriptions(self, request):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)
        authors = user.follow.all()
        pages = self.paginate_queryset(authors)
        serializer = UserSubscribeSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientsViewSet(ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def find_obj(queryset, name):
        """Поиск объектов по совпадению в начале названия и в середине."""
        stw_queryset = list(queryset.filter(name__startswith=name))
        cnt_queryset = queryset.filter(name__contains=name)
        stw_queryset.extend(
            [i for i in cnt_queryset if i not in stw_queryset]
        )
        queryset = stw_queryset
        return queryset

    def translation(name):
        """Метод преобразования латинских символов в кириллицу."""
        if name[0] == '%':
            name = unquote(name)
        else:
            name = name.translate(incorrect_layout)
        return name

    def get_queryset(self):
        """Получает queryset в соответствии с параметрами запроса.
        Прописные буквы преобразуются в строчные.
        """
        name = self.request.query_params.get('name')
        queryset = self.queryset
        if name:
            name = self.translation(name)
            name = name.lower()
            queryset = self.find_obj(queryset, name)
        return queryset


class RecipeViewSet(ModelViewSet, CreateDeleteViewMixin):

    queryset = Recipe.objects.select_related('author').prefetch_related(
        'tags', 'in_favorites', 'in_buy_list'
    )
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorStaffOrReadOnly,)
    pagination_class = PageLimitPagination
    add_serializer = ShowRecipeSerializer

    def authorized_user(self, user):
        if user.is_anonymous:
            return queryset

        is_in_buy = self.request.query_params.get('is_in_buy_cart')
        if is_in_buy in ('1', 'true',):
            queryset = queryset.filter(is_in_shopping_list=user.id)
        elif is_in_buy in ('0', 'false',):
            queryset = queryset.exclude(is_in_shopping_list=user.id)

        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited in ('1', 'true',):
            queryset = queryset.filter(is_favorite=user.id)
        if is_favorited in ('0', 'false',):
            queryset = queryset.exclude(is_favorite=user.id)

        return queryset

    def get_queryset(self):
        queryset = self.queryset
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(
                tags__slug__in=tags).distinct()

        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)

        user = self.request.user
        queryset = self.authorized_user(self, user)

        return queryset

    @action(methods=('GET', 'POST', 'DELETE',), detail=True)
    def favorite(self, request, pk):
        return self.add_remove_relation(pk, 'is_favorite_M2M')

    @action(methods=('GET', 'POST', 'DELETE',), detail=True)
    def shopping_cart(self, request, pk):
        return self.add_remove_relation(pk, 'shopping_cart_M2M')

    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request):
        TIME_FORMAT = '%d/%m/%Y %H:%M'
        user = self.request.user
        if not user.buy_list.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        ingredients = AmountIngredient.objects.filter(
            recipe__in=(user.buy_list.values('id'))
        ).values(
            ingredient=F('ingredients__name'),
            measure=F('ingredients__measurement_unit')
        ).annotate(amount=Sum('amount'))

        filename = f'{user.username}_buy_list.txt'
        buy_list = (
            f'Список покупок для пользователя {user.first_name}:\n\n'
        )
        for ing in ingredients:
            buy_list += (
                f'{ing["ingredient"]}: {ing["amount"]} {ing["measure"]}\n'
            )

        buy_list += (
            f'\nДата составления {dt.now().strftime(TIME_FORMAT)}.'
            '\n\nMade in Foodgram 2023 (c)'
        )

        response = HttpResponse(
            buy_list, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
