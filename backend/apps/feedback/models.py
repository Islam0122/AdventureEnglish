from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Feedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Пользователь')
    )
    email = models.EmailField(_('Email пользователя'), blank=True, null=True)
    subject = models.CharField(_('Тема'), max_length=255)
    message = models.TextField(_('Сообщение'))
    is_read = models.BooleanField(_('Прочитано'), default=False)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)

    class Meta:
        verbose_name = _('Обратная связь')
        verbose_name_plural = _('Обратная связь')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} от {self.user or self.email}'
