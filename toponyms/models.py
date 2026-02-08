from django.db import models
from django.contrib.auth.models import User

class Toponym(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('moderation', 'На модерации'),
        ('published', 'Опубликовано'),
        ('disputed', 'Спорный'),
        ('rejected', 'Отклонено'),
    ]
    
    TYPE_CHOICES = [
        ('spring', 'Родник'),
        ('rock', 'Скала/Утёс'),
        ('mountain', 'Гора'),
        ('river', 'Река'),
        ('lake', 'Озеро'),
        ('forest', 'Лес/Роща'),
        ('field', 'Поле/Луг'),
        ('ravine', 'Овраг/Лог'),
        ('tract', 'Урочище'),
        ('other', 'Другое'),
    ]
    
    # Основные поля
    name_bash = models.CharField(max_length=200, verbose_name='Название на башкирском')
    name_rus = models.CharField(max_length=200, verbose_name='Название на русском')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='Тип объекта')
    
    # Координаты
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Долгота')
    
    # Описание
    description = models.TextField(blank=True, verbose_name='Описание/легенда')
    location_note = models.TextField(blank=True, verbose_name='Примечание к местоположению')
    
    # Административная привязка
    municipality = models.CharField(max_length=300, blank=True, verbose_name='Муниципальный район/поселение')
    
    # Медиа
    photo = models.ImageField(upload_to='toponyms/photos/', blank=True, verbose_name='Фотография')
    audio = models.FileField(upload_to='toponyms/audio/', blank=True, verbose_name='Аудиозапись')
    
    # Служебные данные из реестра
    reg_number = models.CharField(max_length=50, blank=True, verbose_name='Регистрационный номер (АГКГН)')
    map_nomenclature = models.CharField(max_length=50, blank=True, verbose_name='Номенклатура карты')
    
    # Внешние ссылки
    external_links = models.JSONField(default=dict, blank=True, verbose_name='Внешние ссылки')
    
    # Метаданные
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='moderation', verbose_name='Статус')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Кем добавлен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    # Для голосований/спорных
    votes_for = models.IntegerField(default=0, verbose_name='Голосов за')
    votes_against = models.IntegerField(default=0, verbose_name='Голосов против')
    disputed_alternatives = models.JSONField(default=list, blank=True, verbose_name='Альтернативные варианты названия')
    
    class Meta:
        verbose_name = 'Топоним'
        verbose_name_plural = 'Топонимы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'type']),
            models.Index(fields=['latitude', 'longitude']),
        ]
    
    def __str__(self):
        return f"{self.name_rus} ({self.name_bash})"
    
    @property
    def coordinate_string(self):
        """Координаты в формате для карты"""
        return f"{self.latitude},{self.longitude}"