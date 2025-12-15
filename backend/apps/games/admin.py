from django.contrib import admin
from .models import (
    Game, GameResult,
    HangmanWord, WordQuizQuestion,
    ListeningQuestion, GrammarQuestion
)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("title", "game_type", "level", "is_active", "created_at")
    list_filter = ("game_type", "level", "is_active")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "score", "max_score", "accuracy", "duration", "created_at")
    list_filter = ("game__game_type", "game__level", "created_at")
    search_fields = ("user__username", "game__title")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(HangmanWord)
class HangmanWordAdmin(admin.ModelAdmin):
    list_display = ("word", "hint", "level", "created_at")
    list_filter = ("level",)
    search_fields = ("word", "hint")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(WordQuizQuestion)
class WordQuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "correct_answer", "level", "created_at")
    list_filter = ("level",)
    search_fields = ("question", "correct_answer")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(ListeningQuestion)
class ListeningQuestionAdmin(admin.ModelAdmin):
    list_display = ("audio_file", "correct_answer", "level", "created_at")
    list_filter = ("level",)
    search_fields = ("audio_file", "correct_answer")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


@admin.register(GrammarQuestion)
class GrammarQuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "correct_answer", "level", "created_at")
    list_filter = ("level",)
    search_fields = ("question", "correct_answer")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
