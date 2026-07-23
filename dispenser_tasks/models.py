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

    class Meta:
        ordering = ['-create_date']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return f"{self.name} - {self.doc_id}"