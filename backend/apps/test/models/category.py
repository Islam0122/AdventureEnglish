
from django.db import models
from .base import BaseModel
from ..constants import TestCategoryType


class TestCategory(BaseModel):
    name = models.CharField(
        max_length=50,
        choices=TestCategoryType.choices,
        unique=True,
        verbose_name="Название категории"
    )
    display_name = models.CharField(
        max_length=100,
        verbose_name="Отображаемое название",
        help_text="Например: 'Грамматика', 'Словарный запас'"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание категории"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="CSS класс иконки или emoji",
        verbose_name="Иконка"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
    )

    class Meta:
        verbose_name = "Категория теста"
        verbose_name_plural = "Категории тестов"
        ordering = ['order', 'display_name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active', 'order']),
        ]

    def __str__(self):
        return self.display_name

    @property
    def test_count(self):
        """Количество тестов в категории"""
        return self.tests.filter(is_active=True).count()