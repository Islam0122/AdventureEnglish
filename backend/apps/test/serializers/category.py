from rest_framework import serializers
from ..models import TestCategory


class TestCategorySerializer(serializers.ModelSerializer):
    test_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = TestCategory
        fields = [
            'id',
            'name',
            'display_name',
            'description',
            'icon',
            'order',
            'is_active',
            'test_count',
            'created_at',
        ]
        read_only_fields = ['id', 'test_count', 'created_at']


class TestCategoryDetailSerializer(serializers.ModelSerializer):
    test_count = serializers.IntegerField(read_only=True)
    tests = serializers.SerializerMethodField()

    class Meta:
        model = TestCategory
        fields = [
            'id',
            'name',
            'display_name',
            'description',
            'icon',
            'order',
            'is_active',
            'test_count',
            'tests',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'test_count', 'created_at', 'updated_at']

    def get_tests(self, obj):
        from .test import TestMinimalSerializer

        tests = obj.tests.filter(is_active=True).select_related('level')
        return TestMinimalSerializer(tests, many=True).data


class TestCategoryMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestCategory
        fields = ['id', 'name', 'display_name', 'icon']
        read_only_fields = fields