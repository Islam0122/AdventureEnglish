from rest_framework import serializers
from .models import Game, GameResult, HangmanWord, WordQuizQuestion, ListeningQuestion, GrammarQuestion


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "title", "description", "game_type", "level", "is_active"]


class GameResultSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    game = GameSerializer(read_only=True)
    game_id = serializers.PrimaryKeyRelatedField(queryset=Game.objects.filter(is_active=True), source="game", write_only=True)

    class Meta:
        model = GameResult
        fields = ["id", "user", "game", "game_id", "score", "max_score", "accuracy", "duration", "meta", "created_at"]
        read_only_fields = ["id", "user", "game", "created_at"]


class HangmanWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HangmanWord
        fields = ["id", "word", "hint", "level"]


class WordQuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordQuizQuestion
        fields = ["id", "question", "options", "correct_answer", "level"]


class ListeningQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningQuestion
        fields = ["id", "audio_file", "options", "correct_answer", "level"]


class GrammarQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrammarQuestion
        fields = ["id", "question", "options", "correct_answer", "level"]
