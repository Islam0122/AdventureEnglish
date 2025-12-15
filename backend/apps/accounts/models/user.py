from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from ..managers.user_manager import UserManager

class AuthType(models.TextChoices):
    LOCAL = 'local', 'Local'
    GOOGLE = 'google', 'Google'

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email адрес')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')

    level = models.CharField(
        max_length=3,
        choices=[('A1','A1'),('A2','A2'),('B1','B1'),('B2','B2'),('C1','C1'),('C2','C2')],
        default='A1',
        verbose_name='Уровень английского'
    )
    points = models.IntegerField(default=0, verbose_name='Очки опыта')
    completed_tests = models.IntegerField(default=0, verbose_name='Пройденные тесты')

    is_verified = models.BooleanField(default=False, verbose_name='Email подтвержден')
    auth_type = models.CharField(
        max_length=10,
        choices=AuthType.choices,
        default=AuthType.LOCAL,
        verbose_name='Тип аутентификации'
    )

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-created_at']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.email})"