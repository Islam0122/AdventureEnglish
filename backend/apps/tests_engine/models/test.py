from django.db import models
from django.core.validators import MinValueValidator
from .base import BaseModel
from .level import Level
from .category import TestCategory
from ..constants import TestType


class Test(BaseModel):
    name = models.CharField(
        max_length=200,
        verbose_name="Название теста",
        help_text="Например: 'Present Simple - Grammar Test'"
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        verbose_name="URL slug"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание теста"
    )

    # Связи
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name="Уровень сложности"
    )
    category = models.ForeignKey(
        TestCategory,
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name="Категория"
    )

    # Настройки
    test_type = models.CharField(
        max_length=20,
        choices=TestType.choices,
        default=TestType.REGULAR,
        verbose_name="Тип теста"
    )
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        verbose_name="Длительность (минуты)",
        help_text="Оставьте пустым для неограниченного времени"
    )
    passing_score = models.PositiveIntegerField(
        default=70,
        validators=[MinValueValidator(0)],
        verbose_name="Проходной балл (%)"
    )
    max_attempts = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Максимум попыток",
        help_text="Оставьте пустым для неограниченного количества"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name="Публичный",
        help_text="Доступен всем пользователям"
    )
    total_attempts = models.PositiveIntegerField(
        default=0,
        verbose_name="Всего попыток"
    )
    average_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name="Средний балл"
    )

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
        ordering = ['level', 'category', 'name']
        indexes = [
            models.Index(fields=['level', 'category']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return f"{self.name} ({self.level.title} - {self.category.display_name})"

    @property
    def question_count(self):
        return self.questions.count()

    def update_statistics(self):
        from django.db.models import Avg
        attempts = self.attempts.all()
        self.total_attempts = attempts.count()
        self.average_score = attempts.aggregate(
            avg=Avg('percentage')
        )['avg'] or 0
        self.save(update_fields=['total_attempts', 'average_score'])