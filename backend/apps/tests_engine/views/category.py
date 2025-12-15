from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from drf_spectacular.utils import extend_schema, extend_schema_view
from ..models import TestCategory
from ..serializers import (
    TestCategorySerializer,
    TestCategoryDetailSerializer,
    TestCategoryMinimalSerializer
)


@extend_schema_view(
    list=extend_schema(
        summary="Список категорий",
        description="Получить список всех активных категорий тестов",
        tags=['Categories']
    ),
    retrieve=extend_schema(
        summary="Детали категории",
        description="Получить детальную информацию о категории с тестами",
        tags=['Categories']
    )
)
class TestCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для просмотра категорий тестов

    list: Список всех категорий
    retrieve: Детали конкретной категории
    popular: Популярные категории
    """

    permission_classes = [AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'display_name', 'test_count']
    ordering = ['order']

    def get_queryset(self):
        """Оптимизированный queryset с подсчетом тестов"""
        return TestCategory.objects.filter(
            is_active=True
        ).annotate(
            test_count=Count('tests', filter=models.Q(tests__is_active=True))
        )

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия"""
        if self.action == 'retrieve':
            return TestCategoryDetailSerializer
        elif self.action == 'minimal':
            return TestCategoryMinimalSerializer
        return TestCategorySerializer

    @extend_schema(
        summary="Популярные категории",
        description="Получить категории с наибольшим количеством тестов",
        tags=['Categories']
    )
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Получить популярные категории"""
        categories = self.get_queryset().order_by('-test_count')[:5]
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Минимальный список категорий",
        description="Получить упрощенный список категорий (только id, name, icon)",
        tags=['Categories']
    )
    @action(detail=False, methods=['get'])
    def minimal(self, request):
        """Получить минимальный список категорий"""
        categories = self.get_queryset()
        serializer = TestCategoryMinimalSerializer(categories, many=True)
        return Response(serializer.data)