from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LevelViewSet,
    TestCategoryViewSet,
    TestViewSet,
    QuestionViewSet,
    ResultsTestViewSet,
    PlacementTestViewSet,
    PlacementTestResultViewSet
)

app_name = 'tests_engine'

router = DefaultRouter()

router.register(r'levels', LevelViewSet, basename='level')
router.register(r'categories', TestCategoryViewSet, basename='category')
router.register(r'tests', TestViewSet, basename='tests_engine')
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'results', ResultsTestViewSet, basename='result')
router.register(r'placement-tests', PlacementTestViewSet, basename='placement-tests_engine')
router.register(r'placement-results', PlacementTestResultViewSet, basename='placement-result')

urlpatterns = [
    path('', include(router.urls)),
]