from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import User

# Ingredient and tags and in_favorites

class Tag(models.Model):
    """Модель тэгов для рецептов."""
    name = models.CharField(
        max_length=200,
        verbose_name='Тэг',
    )
    color = models.CharField(
        max_length=7,
        default='#ffffff',
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
    )

    class Meta:
        ordering = ['name',]
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.slug
    

class Ingredient(models.Model):
    """Модель для ингридиентов для рецепта."""
    name = models.CharField(
        verbose_name='Ингридиент',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=200
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
    
    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель для рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название блюда'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name='Описание рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    is_favorite = models.ManyToManyField(
        User,
        verbose_name='Избранное',
        related_name='favorites'
    )
    is_in_shopping_list = models.ManyToManyField(
        User,
        verbose_name='Список покупок',
        related_name='shopping_list'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
    

class AmountIngredient(models.Model):
    """Модель количества игредиентов для рецепта."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    amount = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    class Meta:
        ordering = ('recipe',)
        constraints = (
            UniqueConstraint(
                fields=('recipe', 'ingredients', ),
                name='Ингридиент уже добавлен',
            ),
        )
