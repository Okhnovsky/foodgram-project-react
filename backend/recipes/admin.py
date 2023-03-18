from django.contrib import admin
from django.contrib.admin import TabularInline, register
from django.utils.safestring import SafeString, mark_safe
from .models import AmountIngredient, Tag, Ingredient, Recipe


EMPTY_VALUE = 'Значение не задано'


class IngredientInline(TabularInline):
    model = AmountIngredient
    min_num = 1
    extra = 2


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True
    empty_value_display = EMPTY_VALUE


@register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    save_on_top = True
    empty_value_display = EMPTY_VALUE


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author','amount_favorites',
    )
    fields = (
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
        ('image',),
    )
    
    raw_id_fields = ('author', )
    search_fields = (
        'name', 'author',
    )
    list_filter = (
        'name', 'author__username', 'tags__name',
    )

    inlines = (IngredientInline,)
    save_on_top = True
    empty_value_display = EMPTY_VALUE

    def amount_favorites(self, obj):
        return obj.is_favorite.count()

    amount_favorites.short_description = 'В избранном'
