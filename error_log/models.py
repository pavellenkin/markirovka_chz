from django.db import models
from django.utils import timezone
import pytz

def time_now():
    now = timezone.now()
    moscow_tz = pytz.timezone('Europe/Moscow')
    moscow_time = now.astimezone(moscow_tz)
    return moscow_time

class  ErrorLog (models.Model):
    file_name = models.CharField(blank=False, default="None")
    exc_type = models.CharField(blank=False, default="None")
    exc_value = models.CharField(blank=False, default="None")
    lineno = models.CharField(blank=False, default="None")
    datetime_field = models.DateTimeField(default=time_now)

    def __str__(self):
        return f'{self.datetime_field} | {self.exc_type} | {self.file_name} | LINE: {self.lineno}'

