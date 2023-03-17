from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class MyUser(AbstractUser):
    """Кастомная модель пользователя с расширенной функциональностью."""
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
    )
    username = models.CharField(
        max_length=154,
        unique=True,
        validators=(UnicodeUsernameValidator(),),
        verbose_name='Логин',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    follow = models.ManyToManyField(
        to='self',
        related_name='followers',
        symmetrical=False,
        verbose_name='Подписка'
    )

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username
