from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, StudentProfile
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'email',
        'full_name',
        'level',
        'points',
        'completed_tests',
        'is_verified_badge',
        'auth_type',
        'is_active_badge',
        'created_at'
    ]
    list_filter = [
        'level',
        'is_verified',
        'auth_type',
        'is_active',
        'is_staff',
        'created_at'
    ]
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Основная информация', {
            'fields': ('email', 'password')
        }),
        ('Личные данные', {
            'fields': ('first_name', 'last_name')
        }),
        ('Статистика обучения', {
            'fields': ('level', 'points', 'completed_tests')
        }),
        ('Статус', {
            'fields': ('is_verified', 'auth_type', 'is_active')
        }),
        ('Права доступа', {
            'fields': (
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
            'classes': ('collapse',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'level'
            ),
        }),
    )

    def is_verified_badge(self, obj):
        if obj.is_verified:
            return format_html(
                '<span style="color: green;">✓ Подтвержден</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Не подтвержден</span>'
        )

    is_verified_badge.short_description = 'Email'

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="color: green;">✓ Активен</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Неактивен</span>'
        )

    is_active_badge.short_description = 'Статус'


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user_email',
        'user_full_name',
        'phone_number',
        'has_avatar',
        'has_complete_profile_badge',
        'created_at'
    ]
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'phone_number'
    ]
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Контактная информация', {
            'fields': ('phone_number',)
        }),
        ('Дополнительная информация', {
            'fields': ('avatar', 'bio', 'birth_date')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def user_full_name(self, obj):
        return obj.user.full_name

    user_full_name.short_description = 'Полное имя'

    def has_avatar(self, obj):
        if obj.avatar:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')

    has_avatar.short_description = 'Аватар'

    def has_complete_profile_badge(self, obj):
        if obj.has_complete_profile:
            return format_html('<span style="color: green;">✓ Полный</span>')
        return format_html('<span style="color: orange;">⏳ Неполный</span>')

    has_complete_profile_badge.short_description = 'Профиль'


admin.site.unregister(Group)
admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)