from django.db import models
from django.contrib.auth.models import User
from toponyms.models import Toponym


class UserMap(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название карты')
    description = models.TextField(blank=True, verbose_name='Описание')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='maps',
        verbose_name='Владелец'
    )
    is_public = models.BooleanField(default=False, verbose_name='Публичная')
    toponyms = models.ManyToManyField(
        Toponym,
        blank=True,
        related_name='maps',
        verbose_name='Топонимы'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Карта пользователя'
        verbose_name_plural = 'Карты пользователей'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.owner.username})"