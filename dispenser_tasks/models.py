from django.db import models
from django.utils import timezone


class Document(models.Model):
    STATUS_CHOICES = [
        ('PREPARATION', 'Подготовка'),
        ('COMPLETED', 'Выполнено'),
        ('CANCELED', 'Отменено'),
        ('ARCHIVE', 'Архив'),
        ('FAILED', 'Ошибка'),
    ]

    doc_id = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField()
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    org_inn = models.CharField(max_length=20, db_index=True)
    pg = models.IntegerField(blank=True, null=True)
    file_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    filters = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Параметры фильтрации',
        help_text='JSON с параметрами фильтрации для создания документа'
    )

    class Meta:
        ordering = ['-create_date']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return f"{self.name} - {self.doc_id}"

    def get_filters_display(self):
        """Возвращает читаемое представление фильтров"""
        if not self.filters:
            return "Фильтры не заданы"

        filter_labels = {
            'status': 'Статус кодов',
            'participant_inn': 'ИНН организации',
            'include_gtin': 'GTIN товара',
            'package_type': 'Тип упаковки',
            'emission_types': 'Типы эмиссии',
            'product_group_code': 'Товарная группа',
            'emission_period_start': 'Эмиссия (от)',
            'emission_period_end': 'Эмиссия (до)',
            'applied_period_start': 'Нанесение (от)',
            'applied_period_end': 'Нанесение (до)',
        }

        display_parts = []
        for key, label in filter_labels.items():
            value = self.filters.get(key)
            if value:
                display_parts.append(f"{label}: {value}")

        return "; ".join(display_parts) if display_parts else "Фильтры не заданы"