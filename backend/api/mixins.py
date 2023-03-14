from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)


class CreateDeleteViewMixin:
    """Добавляет методы создания и удаления связей M2M"""
    add_serializer = None

    def get_obj_exist(manager, obj_id):
        obj_exist = manager.filter(id=obj_id).exists()
        return obj_exist

    def add_remove_relation(self, obj_id, manager):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=HTTP_401_UNAUTHORIZED)

        managers = {
            'follow_M2M': user.follow,
            'is_favorite_M2M': user.favorites,
            'shopping_cart_M2M': user.buy_list,
        }
        manager = managers[manager]

        obj = get_object_or_404(self.queryset, id=obj_id)
        serializer = self.add_serializer(
            obj, context={'request': self.request}
        )
        obj_exist = self.get_obj_exist(manager, obj_id)

        if (self.request.method in ('GET', 'POST',)) and not obj_exist:
            manager.add(obj)
            return Response(serializer.data, status=HTTP_201_CREATED)

        if (self.request.method in ('DELETE',)) and obj_exist:
            manager.remove(obj)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)
