from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class GameType(models.TextChoices):
    HANGMAN = "hangman", "Hangman"
    WORD_QUIZ = "word_quiz", "Word Quiz"
    LISTENING = "listening", "Listening"
    GRAMMAR = "grammar", "Grammar"


class Level(models.TextChoices):
    EASY = "easy", "Easy"
    MEDIUM = "medium", "Medium"
    HARD = "hard", "Hard"


class Game(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    game_type = models.CharField(max_length=30, choices=GameType.choices)
    level = models.CharField(max_length=10, choices=Level.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.game_type})"


class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_results")
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, related_name="results")
    score = models.PositiveIntegerField()
    max_score = models.PositiveIntegerField()
    accuracy = models.FloatField()
    duration = models.PositiveIntegerField()
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} | {self.game} | {self.score}/{self.max_score}"

# ----> game

class HangmanWord(models.Model):
    word = models.CharField(max_length=50)
    hint = models.CharField(max_length=200, blank=True)
    level = models.CharField(max_length=10, choices=Level.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Слово для Hangman"
        verbose_name_plural = "Слова для Hangman"

    def __str__(self):
        return self.word


class WordQuizQuestion(models.Model):
    question = models.CharField(max_length=200)
    options = models.JSONField()
    correct_answer = models.CharField(max_length=100)
    level = models.CharField(max_length=10, choices=Level.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Вопрос Word Quiz"
        verbose_name_plural = "Вопросы Word Quiz"

    def __str__(self):
        return self.question


class ListeningQuestion(models.Model):
    audio_file = models.FileField(upload_to="listening/")
    options = models.JSONField()
    correct_answer = models.CharField(max_length=100)
    level = models.CharField(max_length=10, choices=Level.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Вопрос Listening"
        verbose_name_plural = "Вопросы Listening"

    def __str__(self):
        return self.audio_file.name


class GrammarQuestion(models.Model):
    question = models.TextField()
    options = models.JSONField()
    correct_answer = models.CharField(max_length=100)
    level = models.CharField(max_length=10, choices=Level.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Вопрос Grammar"
        verbose_name_plural = "Вопросы Grammar"

    def __str__(self):
        return self.question


