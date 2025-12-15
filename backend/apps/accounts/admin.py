from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, StudentProfile
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    readonly_fields = ('created_at', 'updated_at')
    extra = 0

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [StudentProfileInline]

    list_display = [
        'email', 'full_name', 'level', 'points',
        'is_verified_badge', 'is_active_badge', 'created_at'
    ]
    list_filter = ['level', 'is_verified', 'auth_type', 'is_active', 'is_staff', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Основная информация', {'fields': ('email', 'password')}),
        ('Личные данные', {'fields': ('first_name', 'last_name')}),
        ('Статистика', {'fields': ('level', 'points', 'completed_tests')}),
        ('Статус', {'fields': ('is_verified', 'auth_type', 'is_active', 'is_staff', 'is_superuser')}),
        ('Права доступа', {'fields': ('groups', 'user_permissions'), 'classes': ('collapse',)}),
        ('Временные метки', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'level'),
        }),
    )

    def is_verified_badge(self, obj):
        return format_html('<span style="color: {};">{} {}</span>',
                           'green' if obj.is_verified else 'red',
                           '✓' if obj.is_verified else '✗',
                           'Подтвержден' if obj.is_verified else 'Не подтвержден')
    is_verified_badge.short_description = 'Email'

    def is_active_badge(self, obj):
        return format_html('<span style="color: {};">{} {}</span>',
                           'green' if obj.is_active else 'red',
                           '✓' if obj.is_active else '✗',
                           'Активен' if obj.is_active else 'Неактивен')
    is_active_badge.short_description = 'Статус'

admin.site.unregister(Group)
admin.site.unregister(OutstandingToken)
admin.site.unregister(BlacklistedToken)