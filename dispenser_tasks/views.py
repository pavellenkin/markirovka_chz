from django.shortcuts import render
from django.views.decorators.http import require_GET

from main.api.dispenser_task import dispenser_task_init, dispenser_task_status, dispenser_result, dispenser_result_ids
from main.api.participants import get_participants
from main.api.mods_info import mods_info
from main.api.guide_api import product_groups
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
import requests
import json
from datetime import datetime
from .forms import DocumentFilterForm, DocumentCreateForm
from django.conf import settings
from .models import Document

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
        product_groups_list = []
        items_part_info = get_part_info['productGroups']
        try:
            for item in items_part_info:
                guide_item = product_groups(item)
                product_groups_list.append({
                    'name': item,
                    'id': guide_item['id'],
                    'description': guide_item['description'],
                })
        except KeyError:
            product_groups_list = None
    else:
        inn = None
        product_groups_list = None

    date_now = datetime.now()
    name_doc = f"Список кодов от {date_now.strftime('%d-%m-%Y')}"


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
        'inn' : inn,
        'product_groups_list' : product_groups_list,
        'name_doc': name_doc
    }
    return render(request, 'dispenser-tasks.html', context)


def prepare_filters_from_form(form_data):
    """
    Преобразует данные формы в JSON для сохранения
    """
    filters = {}

    # Поля, которые нужно сохранить
    filter_fields = [
        'status',
        'participant_inn',
        'include_gtin',
        'package_type',
        'emission_types',
        'product_group_code',
        'emission_period_start',
        'emission_period_end',
        'applied_period_start',
        'applied_period_end'
    ]

    for field in filter_fields:
        value = form_data.get(field)
        # Сохраняем только непустые значения
        if value and value != '':
            filters[field] = value

    return filters


@require_GET
def document_api(request, doc_id):
    try:
        doc = Document.objects.get(doc_id=doc_id)
        data = {
            'doc_id': doc.doc_id,
            'name': doc.name,
            'create_date': doc.create_date.strftime('%d.%m.%Y %H:%M'),
            'status': doc.current_status,
            'org_inn': doc.org_inn,
            'file_url': doc.file_url,
            'filters': doc.filters,  # JSON поле с фильтрами
        }
        return JsonResponse(data)
    except Document.DoesNotExist:
        return JsonResponse({'error': 'Document not found'}, status=404)

def create_document_task(request):
    if request.method == 'POST':


        filters = prepare_filters_from_form(request.POST)

        json_params = {}

        json_params["participantInn"] = str(request.POST.get('participant_inn'))
        json_params["packageType"] = [str(request.POST.get('package_type'))]
        json_params["status"] =  str(request.POST.get('status'))

        if request.POST.get('emission_types'):
            json_params['emissionTypes'] = [str(request.POST.get('emission_types'))]

        if request.POST.get('include_gtin'):
            json_params['includeGtin'] = [str(request.POST.get('include_gtin'))]

        if request.POST.get('applied_period_start') and request.POST.get('applied_period_end'):
            json_params['appliedPeriod'] = {
                    "start": str(request.POST.get('applied_period_start'))+":00.000Z",
                    "end": str(request.POST.get('applied_period_end'))+":00.000Z",
                }

        if request.POST.get('emission_period_start') and request.POST.get('emission_period_end'):
            json_params['emissionPeriod'] = {
                    "start": str(request.POST.get('emission_period_start'))+":00.000Z",
                    "end": str(request.POST.get('emission_period_end'))+":00.000Z",
                }

        data_to_api = {
            "format": "CSV",
            "name": "FILTERED_CIS_REPORT",
            "periodicity": "SINGLE",
            "productGroupCode": str(request.POST.get('product_group_code')),
            "params": json.dumps(json_params)
        }






        dispenser_stat, dispenser_data = dispenser_task_init(data_to_api)

        if dispenser_stat:
            json_data = json.loads(dispenser_data)
            new_record = Document.objects.create(
                doc_id=json_data['id'],
                name=str(request.POST.get('name_doc')),
                current_status=json_data['currentStatus'],
                create_date=json_data['createDate'],
                org_inn=json_data['orgInn'],
                pg=json_data['productGroupCode'],
                filters=filters
            )
            if new_record:
                messages.success(request, 'Документ успешно создан!')
        else:
            messages.error(
                request,
                dispenser_data)
        # form = DocumentCreateForm(request.POST)
        # if form.is_valid():
        # form = DocumentCreateForm(request.POST)
        # if form.is_valid():
        #     # Здесь вызываем API Честного знака
        #     try:
        #         print(form.cleaned_data)
        #         # Пример вызова API
        #         # api_response = call_crpt_api(form.cleaned_data)
        #
        #         # if api_response.get('success'):
        #         #     document = form.save()
        #         messages.success(request, 'Документ успешно создан!')
        #         return redirect('document_list')
        #         # else:
        #             # messages.error(request,
        #             #                f'Ошибка при создании документа: {api_response.get("error", "Неизвестная ошибка")}')
        #     except Exception as e:
        #         messages.error(request, f'Ошибка при вызове API: {str(e)}')
        # else:
        #     messages.error(request, 'Пожалуйста, исправьте ошибки в форме')

    return redirect('document_list')




def get_document_status(request, doc_id):
    """
    Получение статуса документа из API Честного знака
    """
    try:
        task_status, task_data = dispenser_task_status(doc_id)

        if task_status:
            json_data = json.loads(task_data)
            update = Document.objects.get(doc_id=doc_id)
            update.current_status = json_data['currentStatus']
            update.save()
            messages.success(request, f"Статус документа '{doc_id}' обновлен ")
            return redirect('document_list')
        else:
            messages.error(request, task_data)
            return redirect('document_list')

    except Exception as e:
        messages.error(request,str(e))
        return redirect('document_list')

def get_document_failed(request, doc_id):
    """
    Получение статуса документа из API Честного знака
    """
    try:
        task_status, task_data = dispenser_task_status(doc_id)
        json_data = json.loads(task_data)
        if task_status:
            update = Document.objects.get(doc_id=doc_id)
            update.current_status = json_data['currentStatus']
            update.save()
        # ...
        messages.success(request, task_data)
        return redirect('document_list')

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def download_document(request, doc_id):
    """
    Скачивание документа из API Честного знака
    """

    try:
        task_status, task_data = dispenser_task_status(doc_id)

        if task_status:
            json_data = json.loads(task_data)
            download = Document.objects.get(doc_id=doc_id)

            print(json_data['currentStatus'])
            if json_data['currentStatus'] == 'COMPLETED':
                result_status_ids, result_data_ids = dispenser_result_ids(
                    taskid=doc_id,
                    pg=download.pg
                )
                print("IDS: ", result_data_ids)
                if result_status_ids:


                    result_status, result_data, filename, headers = dispenser_result(
                        taskid=result_data_ids,
                        pg=download.pg,
                        max_retries=3,
                        timeout=60
                    )

                    if result_status:
                        # Успешно скачан
                        http_response = HttpResponse(
                            result_data,
                            content_type=headers.get('Content-Type', 'application/octet-stream')
                        )
                        http_response['Content-Disposition'] = f'attachment; filename="{filename}"'
                        return http_response
                    else:
                        # Ошибка
                        messages.error(request, f"Ошибка скачивания: {result_data}")
                        return redirect('document_list')

                return redirect('document_list')
            return redirect('document_list')
        else:
            messages.error(request, task_data)
        return redirect('document_list')

    except requests.exceptions.Timeout:
        messages.error(request, 'Превышено время ожидания ответа от API')
    except requests.exceptions.RequestException as e:
        messages.error(request, f'Ошибка при загрузке файла: {str(e)}')
    except Exception as e:
        messages.error(request, f'Произошла ошибка: {str(e)}')



def delete_document(request, doc_id):
    """
    Получение статуса документа из API Честного знака
    """

    try:
        delete_doc = Document.objects.get(doc_id=doc_id)
        delete_doc.delete()
        messages.success(request, f"Документ '{doc_id}' удален ")
        return redirect('document_list')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('document_list')
