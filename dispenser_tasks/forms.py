from django import forms
from .models import Document


class DocumentFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'Все статусы'),
        ('EMITTED', 'Эмитирован'),
        ('APPLIED', 'Нанесён'),
        ('CIRCULATION', 'В обороте'),
        ('WRITTEN_OFF', 'Списан'),
        ('RETIRED', 'Выбыл'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    emission_date_from = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )

    emission_date_to = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )

    application_date_from = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )

    application_date_to = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )


class DocumentCreateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['doc_id', 'name', 'create_date', 'current_status', 'org_inn']
        widgets = {
            'create_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }