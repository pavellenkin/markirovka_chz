from django.db import models
from django.utils import timezone


class WriteOffAct(models.Model):
    """Модель акта списания"""
    act_number = models.CharField(max_length=50, unique=True, verbose_name="Номер акта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        db_table = 'write_off_acts'
        verbose_name = 'Акт списания'
        verbose_name_plural = 'Акты списания'
        ordering = ['-created_at']

    def __str__(self):
        return f"Акт №{self.act_number}"

    def get_codes_count(self):
        return self.codes.count()


class WriteOffCode(models.Model):
    """Модель кодов списания"""
    act = models.ForeignKey(WriteOffAct, on_delete=models.CASCADE, related_name='codes', verbose_name="Акт списания")
    code = models.CharField(max_length=255, verbose_name="Код идентификации")
    scanned_at = models.DateTimeField(auto_now_add=True, verbose_name="Время сканирования")
    is_overwritten = models.BooleanField(default=False, verbose_name="Перезаписан")
    overwritten_at = models.DateTimeField(null=True, blank=True, verbose_name="Время перезаписи")

    class Meta:
        db_table = 'write_off_codes'
        verbose_name = 'Код списания'
        verbose_name_plural = 'Коды списания'
        ordering = ['scanned_at']
        unique_together = ['act', 'code']  # Уникальность кода в рамках акта

    def __str__(self):
        return f"{self.act.act_number} - {self.code[:20]}..."