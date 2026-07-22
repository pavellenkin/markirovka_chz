from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['doc_id', 'name', 'create_date', 'current_status', 'org_inn']
    list_filter = ['current_status', 'create_date']
    search_fields = ['doc_id', 'name', 'org_inn']
    date_hierarchy = 'create_date'