from django.contrib import admin
from django.contrib.admin import TabularInline, register
from .models import AmountIngredient, Tag, Ingredient, Recipe


EMPTY_VALUE = 'Значение не задано'


class IngredientInline(TabularInline):
    model = AmountIngredient
    extra = 2


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    save_on_top = True
    empty_value_display = EMPTY_VALUE


@register(Ingredient)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)
    save_on_top = True
    empty_value_display = EMPTY_VALUE


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author',
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
        'name', 'author__username',
    )

    inlines = (IngredientInline,)
    save_on_top = True
    empty_value_display = EMPTY_VALUE
