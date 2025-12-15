from django.db import models


class QuestionType(models.TextChoices):
    MCQ = 'mcq', 'Multiple Choice'
    FILL_BLANK = 'fill_blank', 'Fill in the Blank'
    TRUE_FALSE = 'true_false', 'True/False'
    LISTENING = 'listening', 'Listening'
    READING = 'reading', 'Reading Comprehension'
    TRANSLATE = 'translate', 'Translation'


class TestType(models.TextChoices):
    REGULAR = 'regular', 'Regular Test'
    PLACEMENT = 'placement', 'Placement Test'
    PRACTICE = 'practice', 'Practice Test'
    MOCK_EXAM = 'mock_exam', 'Mock Exam'


class DifficultyLevel(models.TextChoices):
    A1 = 'A1', 'Beginner (A1)'
    A2 = 'A2', 'Elementary (A2)'
    B1 = 'B1', 'Intermediate (B1)'
    B2 = 'B2', 'Upper-Intermediate (B2)'
    C1 = 'C1', 'Advanced (C1)'
    C2 = 'C2', 'Proficiency (C2)'


class TestCategoryType(models.TextChoices):
    GRAMMAR = 'grammar', 'Grammar'
    VOCABULARY = 'vocabulary', 'Vocabulary'
    LISTENING = 'listening', 'Listening'
    READING = 'reading', 'Reading'
    WRITING = 'writing', 'Writing'
    SPEAKING = 'speaking', 'Speaking'
    MIXED = 'mixed', 'Mixed Skills'


TEST_SETTINGS = {
    'DEFAULT_PASSING_SCORE': 70,  # Процент для прохождения
    'DEFAULT_TIME_LIMIT': 60,  # Минуты
    'QUESTIONS_PER_LEVEL': 5,  # Для Placement теста
    'MAX_ATTEMPTS': None,  # Неограниченно
}

LEVEL_WEIGHTS = {
    'A1': 2.0,
    'A2': 2.5,
    'B1': 3.0,
    'B2': 3.5,
    'C1': 4.0,
    'C2': 4.5,
}

LEVEL_THRESHOLDS = {
    'C2': 90,
    'C1': 75,
    'B2': 60,
    'B1': 45,
    'A2': 30,
    'A1': 0,
}