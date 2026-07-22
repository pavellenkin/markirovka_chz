from django.shortcuts import render
from main.api.dispenser_task import dispenser_task_init, dispenser_task_status
from main.api.participants import get_participants
from main.api.mods_info import mods_info
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
import requests
import json
from datetime import datetime
from .models import Document
from .forms import DocumentFilterForm, DocumentCreateForm
from django.conf import settings

# def dispenser_tasks(request):
#
#     # dispenser = dispenser_task_init()
#     # print(dispenser)
#     taskid='8fc39d82-5d32-49fa-9bcd-fa1bfe3e78f9'
#     task_status = dispenser_task_status(taskid)
#     inn = '7712035729'
#     get_part_status, get_part_info = get_participants(inn)
#     print(get_part_info['productGroups'])
#
#
#     return render(request, 'dispenser-tasks.html')





def document_list(request):
    status_mods, data_mods = mods_info()
    if status_mods and 'result' in data_mods:
        inn = data_mods['result'][0]['inn']
        get_part_status, get_part_info = get_participants(inn)
        print(get_part_info['productGroups'])
    else:
        inn = None


    documents = Document.objects.all()
    form = DocumentFilterForm(request.GET or None)

    # Применяем фильтры
    if form.is_valid():
        if form.cleaned_data.get('status'):
            documents = documents.filter(current_status=form.cleaned_data['status'])

        if form.cleaned_data.get('emission_date_from'):
            documents = documents.filter(emission_date_from__gte=form.cleaned_data['emission_date_from'])

        if form.cleaned_data.get('emission_date_to'):
            documents = documents.filter(emission_date_to__lte=form.cleaned_data['emission_date_to'])

        if form.cleaned_data.get('application_date_from'):
            documents = documents.filter(application_date_from__gte=form.cleaned_data['application_date_from'])

        if form.cleaned_data.get('application_date_to'):
            documents = documents.filter(application_date_to__lte=form.cleaned_data['application_date_to'])

    # Пагинация
    paginator = Paginator(documents, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'documents': page_obj,
        'form': form,
        'inn' : inn
    }
    return render(request, 'dispenser-tasks.html', context)


def create_document_task(request):
    if request.method == 'POST':
        form = DocumentCreateForm(request.POST)
        if form.is_valid():
            # Здесь вызываем API Честного знака
            try:
                # Пример вызова API
                api_response = call_crpt_api(form.cleaned_data)

                if api_response.get('success'):
                    document = form.save()
                    messages.success(request, 'Документ успешно создан!')
                    return redirect('document_list')
                else:
                    messages.error(request,
                                   f'Ошибка при создании документа: {api_response.get("error", "Неизвестная ошибка")}')
            except Exception as e:
                messages.error(request, f'Ошибка при вызове API: {str(e)}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')

    return redirect('document_list')


def call_crpt_api(data):
    """
    Функция для вызова API Честного знака
    """
    # Настройки API (замените на свои)
    API_URL = settings.CRPT_API_URL
    API_KEY = settings.CRPT_API_KEY

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'name': data.get('name'),
        'status': data.get('current_status'),
        'org_inn': data.get('org_inn'),
        'date_from': data.get('emission_date_from'),
        'date_to': data.get('emission_date_to'),
        # Добавьте другие параметры согласно документации API
    }

    try:
        response = requests.post(
            f'{API_URL}/documents/create',
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': str(e)}


def get_document_status(request, doc_id):
    """
    Получение статуса документа из API Честного знака
    """
    try:
        # Здесь код для получения статуса из API
        # ...
        return JsonResponse({'status': 'success', 'data': {}})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
