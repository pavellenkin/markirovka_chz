from django.shortcuts import render
from error_log.models import ErrorLog

def create_item_error_log(file_name, exc_type, exc_value, lineno):
    error_item = ErrorLog.objects.create(
        file_name=file_name,
        exc_type=exc_type,
        exc_value=exc_value,
        lineno=lineno)
    error_item.save()


