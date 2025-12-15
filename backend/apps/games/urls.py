from rest_framework.routers import DefaultRouter
from .views import (
    GameViewSet, GameResultViewSet,
    HangmanWordViewSet, WordQuizQuestionViewSet,
    ListeningQuestionViewSet, GrammarQuestionViewSet
)

router = DefaultRouter()
router.register(r"games", GameViewSet, basename="games")
router.register(r"game-results", GameResultViewSet, basename="game-results")
router.register(r"hangman-words", HangmanWordViewSet, basename="hangman-words")
router.register(r"word-quiz", WordQuizQuestionViewSet, basename="word-quiz")
router.register(r"listening", ListeningQuestionViewSet, basename="listening")
router.register(r"grammar", GrammarQuestionViewSet, basename="grammar")

urlpatterns = router.urls
