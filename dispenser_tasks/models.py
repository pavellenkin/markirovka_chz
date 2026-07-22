from django.db import models
from django.utils import timezone


class Document(models.Model):
    STATUS_CHOICES = [
        ('EMITTED', 'Эмитирован'),
        ('APPLIED', 'Нанесён'),
        ('CIRCULATION', 'В обороте'),
        ('WRITTEN_OFF', 'Списан'),
        ('RETIRED', 'Выбыл'),
    ]

    doc_id = models.CharField(max_length=100, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    create_date = models.DateTimeField()
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    org_inn = models.CharField(max_length=20, db_index=True)

    # Дополнительные поля для фильтрации
    emission_date_from = models.DateTimeField(null=True, blank=True)
    emission_date_to = models.DateTimeField(null=True, blank=True)
    application_date_from = models.DateTimeField(null=True, blank=True)
    application_date_to = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-create_date']
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return f"{self.name} - {self.doc_id}"