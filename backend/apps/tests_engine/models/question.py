from django.db import models
from django.core.exceptions import ValidationError
from .base import BaseModel
from ..constants import QuestionType


class Question(BaseModel):
    test = models.ForeignKey(
        'Test',
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Тест"
    )
    level = models.ForeignKey(
        'Level',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Уровень вопроса",
        help_text="Для Placement тестов"
    )

    text = models.TextField(
        verbose_name="Текст вопроса"
    )
    question_type = models.CharField(
        max_length=20,
        choices=QuestionType.choices,
        default=QuestionType.MCQ,
        verbose_name="Тип вопроса"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
        help_text="Порядок отображения в тесте"
    )

    # Варианты ответов (для MCQ)
    option_a = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Вариант A"
    )
    option_b = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Вариант B"
    )
    option_c = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Вариант C"
    )
    option_d = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Вариант D"
    )

    # Правильный ответ
    correct_answer = models.TextField(
        verbose_name="Правильный ответ",
        help_text="Для MCQ: A/B/C/D, для других - текст ответа"
    )

    # Дополнительно
    explanation = models.TextField(
        blank=True,
        verbose_name="Объяснение",
        help_text="Объяснение правильного ответа"
    )
    hint = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Подсказка"
    )
    points = models.PositiveIntegerField(
        default=1,
        verbose_name="Баллы за вопрос"
    )
    translation = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Перевод",
        help_text="Для вопросов на перевод"
    )

    # Медиа
    image = models.ImageField(
        upload_to='questions/images/',
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    audio_file = models.FileField(
        upload_to='questions/audio/',
        blank=True,
        null=True,
        verbose_name="Аудио файл"
    )

    # Статус
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['tests_engine', 'order', 'id']
        indexes = [
            models.Index(fields=['tests_engine', 'order']),
            models.Index(fields=['question_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.text[:50]}..."

    def clean(self):
        """Валидация вопроса"""
        super().clean()

        if self.question_type == QuestionType.MCQ:
            if not all([self.option_a, self.option_b, self.option_c, self.option_d]):
                raise ValidationError(
                    "Для MCQ необходимо заполнить все 4 варианта ответа"
                )
            if self.correct_answer.upper() not in ['A', 'B', 'C', 'D']:
                raise ValidationError(
                    "Для MCQ правильный ответ должен быть A, B, C или D"
                )

        if self.question_type == QuestionType.LISTENING and not self.audio_file:
            raise ValidationError(
                "Для Listening вопроса необходимо добавить аудио файл"
            )

    def is_correct(self, answer: str) -> bool:
        """Проверяет правильность ответа"""
        if not answer:
            return False

        answer = str(answer).strip()

        if self.question_type == QuestionType.MCQ:
            return self.correct_answer.upper() == answer.upper()

        if self.question_type == QuestionType.TRUE_FALSE:
            return self.correct_answer.lower() == answer.lower()

        return self.correct_answer.strip().lower() == answer.lower()

    @property
    def options(self):
        """Возвращает список опций для MCQ"""
        if self.question_type == QuestionType.MCQ:
            return {
                'A': self.option_a,
                'B': self.option_b,
                'C': self.option_c,
                'D': self.option_d,
            }
        return {}