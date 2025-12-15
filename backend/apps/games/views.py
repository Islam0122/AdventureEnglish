from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import Game, GameResult, HangmanWord, WordQuizQuestion, ListeningQuestion, GrammarQuestion
from .serializers import (
    GameSerializer, GameResultSerializer,
    HangmanWordSerializer, WordQuizQuestionSerializer,
    ListeningQuestionSerializer, GrammarQuestionSerializer
)


class GameViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Game.objects.filter(is_active=True)
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]


class GameResultViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = GameResultSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GameResult.objects.filter(user=self.request.user).select_related("game")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HangmanWordViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = HangmanWord.objects.all()
    serializer_class = HangmanWordSerializer
    # permission_classes = [IsAuthenticated]


class WordQuizQuestionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = WordQuizQuestion.objects.all()
    serializer_class = WordQuizQuestionSerializer
    permission_classes = [IsAuthenticated]


class ListeningQuestionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ListeningQuestion.objects.all()
    serializer_class = ListeningQuestionSerializer
    permission_classes = [IsAuthenticated]


class GrammarQuestionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GrammarQuestion.objects.all()
    serializer_class = GrammarQuestionSerializer
    permission_classes = [IsAuthenticated]
