from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from .base import BaseModel
from .test import Test
from .level import Level

User = get_user_model()


class TestAttempt(BaseModel):
    """Попытка прохождения теста"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='test_attempts',
        null=True,
        blank=True,
        verbose_name="Пользователь",
        help_text="Null для анонимных пользователей"
    )

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name="Тест"
    )

    total_questions = models.PositiveIntegerField(
        verbose_name="Всего вопросов"
    )
    correct_answers = models.PositiveIntegerField(
        default=0,
        verbose_name="Правильных ответов"
    )
    wrong_answers = models.PositiveIntegerField(
        default=0,
        verbose_name="Неправильных ответов"
    )
    score = models.PositiveIntegerField(
        default=0,
        verbose_name="Набрано баллов"
    )
    max_score = models.PositiveIntegerField(
        verbose_name="Максимум баллов"
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Процент (%)"
    )

    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Начало теста"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Завершение теста"
    )
    time_spent_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Время (секунды)"
    )

    is_completed = models.BooleanField(
        default=False,
        verbose_name="Завершен"
    )
    is_passed = models.BooleanField(
        default=False,
        verbose_name="Пройден"
    )

    certificate = models.FileField(
        upload_to='certificates/',
        blank=True,
        null=True,
        verbose_name="Сертификат"
    )

    anonymous_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Имя (анонимный)"
    )
    anonymous_email = models.EmailField(
        blank=True,
        verbose_name="Email (анонимный)"
    )

    class Meta:
        verbose_name = "Попытка теста"
        verbose_name_plural = "Попытки тестов"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'test']),
            models.Index(fields=['is_completed', 'created_at']),
        ]

    def __str__(self):
        user_info = self.user.email if self.user else self.anonymous_email
        return f"{self.test.name} - {user_info} - {self.percentage}%"

    def save(self, *args, **kwargs):
        if self.total_questions > 0:
            self.percentage = round(
                (self.correct_answers / self.total_questions) * 100, 2
            )
        self.is_passed = self.percentage >= self.test.passing_score

        super().save(*args, **kwargs)

        if self.is_completed:
            self.test.update_statistics()