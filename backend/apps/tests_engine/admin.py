from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from .models import (
    Level, TestCategory, Test, Question,
    PlacementTest, PlacementTest_Question,
    ResultsTest, PlacementTestResult
)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['title', 'test_count', 'description_short', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _test_count=Count('tests_engine')
        )

    def test_count(self, obj):
        return obj._test_count

    test_count.short_description = 'Тестов'
    test_count.admin_order_field = '_test_count'

    def description_short(self, obj):
        return (obj.description[:100] + '...') if len(obj.description or '') > 100 else obj.description

    description_short.short_description = 'Описание'


@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'name', 'icon_preview', 'test_count', 'order', 'is_active_badge']
    list_filter = ['is_active', 'name']
    search_fields = ['display_name', 'description']
    ordering = ['order', 'display_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'display_name', 'description')
        }),
        ('Отображение', {
            'fields': ('icon', 'order', 'is_active')
        }),
        ('Системное', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _test_count=Count('tests')
        )

    def test_count(self, obj):
        return obj._test_count

    test_count.short_description = 'Тестов'
    test_count.admin_order_field = '_test_count'

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<span style="font-size: 24px;">{}</span>', obj.icon)
        return '-'

    icon_preview.short_description = 'Иконка'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Активна</span>')
        return format_html('<span style="color: red;">✗ Неактивна</span>')

    is_active_badge.short_description = 'Статус'


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    fields = ['text', 'question_type', 'correct_answer', 'points', 'is_active']
    readonly_fields = []
    show_change_link = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('level')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'level', 'category_badge', 'question_count',
        'avg_score', 'is_active_badge', 'created_at'
    ]
    list_filter = ['level', 'category', 'test_type', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['level', 'category', 'name']
    readonly_fields = ['created_at', 'updated_at', 'total_attempts', 'average_score']
    inlines = [QuestionInline]

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'description', 'level', 'category')
        }),
        ('Настройки', {
            'fields': (
                'test_type', 'duration_minutes', 'passing_score',
                'max_attempts', 'is_active', 'is_public'
            )
        }),
        ('Статистика', {
            'fields': ('total_attempts', 'average_score'),
            'classes': ('collapse',)
        }),
        ('Системное', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('level', 'category').annotate(
            _question_count=Count('questions'),
            _avg_score=Avg('results__percentage')
        )

    def question_count(self, obj):
        return obj._question_count

    question_count.short_description = 'Вопросов'
    question_count.admin_order_field = '_question_count'

    def avg_score(self, obj):
        if obj._avg_score:
            return f"{obj._avg_score:.1f}%"
        return "-"

    avg_score.short_description = 'Средний балл'
    avg_score.admin_order_field = '_avg_score'

    def category_badge(self, obj):
        if obj.category:
            return format_html(
                '<span style="background: #f0f0f0; padding: 3px 8px; border-radius: 3px;">{} {}</span>',
                obj.category.icon or '',
                obj.category.display_name
            )
        return '-'

    category_badge.short_description = 'Категория'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')

    is_active_badge.short_description = 'Активен'



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'text_short', 'tests_engine', 'question_type',
        'level', 'points', 'has_media', 'is_active'
    ]
    list_filter = ['question_type', 'test__level', 'is_active']
    search_fields = ['text', 'test__name']
    ordering = ['tests_engine', 'order']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Основное', {
            'fields': ('tests_engine', 'level', 'text', 'question_type', 'order')
        }),
        ('Варианты (MCQ)', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d'),
            'classes': ('collapse',)
        }),
        ('Ответ', {
            'fields': ('correct_answer', 'explanation', 'hint', 'points')
        }),
        ('Дополнительно', {
            'fields': ('translation', 'image', 'audio_file', 'is_active'),
            'classes': ('collapse',)
        }),
        ('Системное', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def text_short(self, obj):
        return obj.text[:80] + ('...' if len(obj.text) > 80 else '')

    text_short.short_description = 'Вопрос'

    def has_media(self, obj):
        media = []
        if obj.image:
            media.append('📷')
        if obj.audio_file:
            media.append('🔊')
        return ' '.join(media) if media else '-'

    has_media.short_description = 'Медиа'


@admin.register(ResultsTest)
class ResultsTestAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'tests_engine', 'percentage_badge',
        'correct_answers', 'has_certificate', 'created_at'
    ]
    list_filter = ['test__level', 'created_at']
    search_fields = ['name', 'email', 'test__name']
    ordering = ['-created_at']
    readonly_fields = ['percentage', 'certificate', 'created_at', 'updated_at']

    fieldsets = (
        ('Пользователь', {
            'fields': ('name', 'email')
        }),
        ('Тест', {
            'fields': ('tests_engine',)
        }),
        ('Результаты', {
            'fields': (
                'score', 'total_questions',
                'correct_answers', 'wrong_answers', 'percentage'
            )
        }),
        ('Сертификат', {
            'fields': ('certificate',)
        }),
        ('Системное', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def percentage_badge(self, obj):
        color = 'green' if obj.percentage >= 70 else 'orange' if obj.percentage >= 50 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color, obj.percentage
        )

    percentage_badge.short_description = 'Процент'
    percentage_badge.admin_order_field = 'percentage'

    def has_certificate(self, obj):
        if obj.certificate:
            return format_html('<a href="{}" target="_blank">📄 Открыть</a>', obj.certificate.url)
        return '-'

    has_certificate.short_description = 'Сертификат'



@admin.register(PlacementTest)
class PlacementTestAdmin(admin.ModelAdmin):
    list_display = ['name', 'question_count', 'result_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _question_count=Count('questions'),
            _result_count=Count('results')
        )

    def question_count(self, obj):
        return obj._question_count

    question_count.short_description = 'Вопросов'

    def result_count(self, obj):
        return obj._result_count

    result_count.short_description = 'Результатов'


@admin.register(PlacementTest_Question)
class PlacementTestQuestionAdmin(admin.ModelAdmin):
    list_display = ['text_short', 'tests_engine', 'level', 'question_type']
    list_filter = ['tests_engine', 'level', 'question_type']
    search_fields = ['text']
    ordering = ['tests_engine', 'level']

    def text_short(self, obj):
        return obj.text[:80] + ('...' if len(obj.text) > 80 else '')

    text_short.short_description = 'Вопрос'


@admin.register(PlacementTestResult)
class PlacementTestResultAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'tests_engine', 'level_badge',
        'percentage_badge', 'created_at'
    ]
    list_filter = ['tests_engine', 'level', 'created_at']
    search_fields = ['name', 'email']
    ordering = ['-created_at']
    readonly_fields = [
        'created_at', 'updated_at', 'percentage',
        'correct_answers', 'wrong_answers', 'score'
    ]

    def level_badge(self, obj):
        if obj.level:
            colors = {
                'A1': '#ff6b6b', 'A2': '#ffa06b',
                'B1': '#ffd56b', 'B2': '#a8e063',
                'C1': '#56ccf2', 'C2': '#8b5cf6'
            }
            color = colors.get(obj.level.title, '#gray')
            return format_html(
                '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
                color, obj.level.title
            )
        return '-'

    level_badge.short_description = 'Уровень'

    def percentage_badge(self, obj):
        color = 'green' if obj.percentage >= 70 else 'orange' if obj.percentage >= 50 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            color, obj.percentage
        )

    percentage_badge.short_description = 'Процент'