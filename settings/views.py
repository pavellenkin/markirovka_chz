from datetime import datetime
import os
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods
from main.api.cert import about_cert
from django.core.files.storage import FileSystemStorage
from settings.console.run_process import process

@cache_control(no_cache=True)
@login_required
def settings(request):

    return render(request, "settings.html", context={})





@cache_control(no_cache=True)
@login_required
def set_active_cert(request):
    if request.method == 'POST':
        cert_number = request.POST.get('active_cert')
        if cert_number:
            # Сохраняем номер активного сертификата в сессию
            request.session['active_cert'] = cert_number

            # Сохраняем в файл
            with open('active_cert.txt', 'w') as f:
                f.write(cert_number)

            # Удаляем файл temp.cfg если он существует
            temp_cfg_path = 'temp.cfg'
            if os.path.exists(temp_cfg_path):
                try:
                    os.remove(temp_cfg_path)
                    print(f"Файл {temp_cfg_path} удален")
                except OSError as e:
                    print(f"Ошибка при удалении {temp_cfg_path}: {e}")


    return redirect('certs')  # или ваш URL для страницы сертификатов



from invent.models import InventoryCodes


@cache_control(no_cache=True)
@login_required
@csrf_exempt
def clear_tsd_file(request):
    """Очищает файл TSD_smart.xlsx"""
    file_path = 'TSD_smart.xlsx'
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            InventoryCodes.objects.all().delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Файл TSD_smart.xlsx успешно удален'
            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'message': 'Файл TSD_smart.xlsx не найден'
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Ошибка при удалении файла: {str(e)}'
        }, status=500)


@cache_control(no_cache=True)
@login_required
def check_tsd_file(request):
    """Проверяет существование файла TSD_smart.xlsx"""
    file_path = 'TSD_smart.xlsx'
    exists = os.path.exists(file_path)
    size = None
    if exists:
        try:
            size_bytes = os.path.getsize(file_path)
            if size_bytes < 1024:
                size = f'{size_bytes} B'
            elif size_bytes < 1024 * 1024:
                size = f'{size_bytes / 1024:.2f} KB'
            else:
                size = f'{size_bytes / (1024 * 1024):.2f} MB'
        except:
            size = 'Неизвестно'

    return JsonResponse({
        'exists': exists,
        'size': size
    })


@cache_control(no_cache=True)
@login_required
def certs(request):

    if request.method == 'POST' and request.FILES.get('myfile'):
        pass_fix = request.POST.get("pass")
        print(pass_fix)
        myfile = request.FILES['myfile']
        # Сохранение в MEDIA_ROOT (рекомендуемый способ)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        file_url = fs.url(filename)
        print(file_url[1:])
        # проверяем установку CERTMGR (manager CryptoPro)
        command = 'find /opt/cprocsp/bin -name "*certmgr*"'
        command_inst = f"/opt/cprocsp/bin/amd64/certmgr -inst -store uMy -pfx -silent -keep_exportable -pin {pass_fix} -file {file_url[1:]}"
        process_q = process(command)

        if process_q['success'] is True and process_q['stdout'] and 'certmgr' in process_q['stdout']:
            print("OK")
            process_q_inst = process(command_inst)
            if process_q_inst['success'] is True and process_q_inst['stdout']:
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error"})
        else:
            return JsonResponse({"status": "error"})


    store, count = "", ""
    items = []
    about = about_cert()
    if about:
        store = about['store']
        count = about['count']
        items = about['data']
    else:
        store = ": отсутствует"
        count = "0"
        items = ""

    print(items)

    active_cert = None
    try:
        with open('active_cert.txt', 'r') as f:
            cert_number = f.read().strip()
            if cert_number:  # Проверяем что файл не пустой
                # Ищем сертификат с таким номером
                for item in items:
                    if str(item['item_number']) == cert_number:
                        active_cert = item
                        break
    except (FileNotFoundError, ValueError):
        # Файл не найден или пустой
        active_cert = None

    return render(request, "certs.html", context={
        "store": store,
        "count": count,
        "items": items,
        'active_cert': active_cert,
    })


@cache_control(no_cache=True)
@login_required
def models(request):

    return render(request, "models.html", context={

    })

@cache_control(no_cache=True)
@login_required
def service(request):

    return render(request, "service.html", context={

    })

@cache_control(no_cache=True)
@login_required
def export(request):

    return render(request, "export.html", context={

    })


@require_http_methods(['GET'])
def safe_download_tsd_file(request):
    """
    View с расширенной обработкой ошибок, логированием и датой/временем в имени файла
    """
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        TSD_FILE_PATH = os.path.join(BASE_DIR, 'TSD_smart.xlsx')
        file_path = TSD_FILE_PATH
        print(f"Путь к файлу: {file_path}")

        # Проверка существования файла
        if not os.path.exists(file_path):
            return JsonResponse(
                {'error': 'Файл не найден'},
                status=404
            )

        # Проверка прав доступа
        if not os.access(file_path, os.R_OK):
            return JsonResponse(
                {'error': 'Нет доступа к файлу'},
                status=403
            )

        # Получаем текущую дату и время
        now = datetime.now()

        # Форматируем дату
        timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
        filename_with_date = f'TSD_smart_{timestamp}.xlsx'

        print(f"Имя файла для скачивания: {filename_with_date}")

        # Читаем файл
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Создаем ответ
        response = HttpResponse(
            file_data,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        # Пробуем разные варианты заголовка
        response['Content-Disposition'] = f'attachment; filename="{filename_with_date}"'

        # Дополнительный заголовок для совместимости
        response['Content-Type'] = 'application/octet-stream'
        response['X-Filename'] = filename_with_date  # Отладочный заголовок

        print(f"Установлен заголовок: attachment; filename=\"{filename_with_date}\"")

        return response

    except Exception as e:
        print(f"Ошибка при скачивании файла: {str(e)}")
        return JsonResponse(
            {'error': 'Внутренняя ошибка сервера'},
            status=500
        )


# Путь к корню проекта
BASE_DIR = Path(__file__).resolve().parent.parent
ARTICLES_FILE_PATH = os.path.join(BASE_DIR, 'articles.xlsx')
TEMPLATE_FILE_PATH = os.path.join(BASE_DIR, 'articles_template.xlsx')


def articles_page(request):
    """
    Страница для работы с файлом артикулов
    """
    # Проверяем существует ли файл
    file_exists = os.path.exists(ARTICLES_FILE_PATH)

    # Получаем информацию о файле если он существует
    file_info = None
    if file_exists:
        stat = os.stat(ARTICLES_FILE_PATH)
        file_info = {
            'size': stat.st_size,
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }

    context = {
        'file_exists': file_exists,
        'file_info': file_info,
        'page_title': 'Управление файлом артикулов'
    }

    return render(request, 'articles_page.html', context)


@require_http_methods(['POST'])
def upload_articles_file(request):
    """
    Загрузка файла артикулов на сервер
    """
    try:
        # Проверяем, есть ли файл в запросе
        if 'articles_file' not in request.FILES:
            return JsonResponse(
                {'error': 'Файл не найден в запросе'},
                status=400
            )

        uploaded_file = request.FILES['articles_file']

        # Проверяем расширение файла
        if not uploaded_file.name.endswith('.xlsx'):
            return JsonResponse(
                {'error': 'Неверный формат файла. Ожидается файл с расширением .xlsx'},
                status=400
            )

        # ПРАВИЛЬНАЯ проверка имени файла
        # Получаем имя файла без расширения
        file_name_without_ext = uploaded_file.name.replace('.xlsx', '')

        # Вариант 1: Проверка на точное совпадение имени
        if file_name_without_ext != 'articles':
            return JsonResponse(
                {
                    'error': f'Неверное имя файла. Ожидается файл с именем "articles.xlsx", получено "{uploaded_file.name}"'},
                status=400
            )

        # Вариант 2: Проверка с игнорированием регистра
        # if file_name_without_ext.lower() != 'articles':
        #     return JsonResponse(
        #         {'error': f'Неверное имя файла. Ожидается файл с именем "articles.xlsx"'},
        #         status=400
        #     )

        # Вариант 3: Проверка что имя начинается с "articles"
        # if not file_name_without_ext.startswith('articles'):
        #     return JsonResponse(
        #         {'error': f'Неверное имя файла. Имя должно начинаться с "articles", получено "{uploaded_file.name}"'},
        #         status=400
        #     )

        # Проверяем размер файла (не более 10MB)
        if uploaded_file.size > 10 * 1024 * 1024:
            return JsonResponse(
                {'error': 'Файл слишком большой. Максимальный размер 10MB'},
                status=400
            )

        # Сохраняем файл (перезаписываем если существует)
        with open(ARTICLES_FILE_PATH, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        # Получаем информацию о сохраненном файле
        file_size = os.path.getsize(ARTICLES_FILE_PATH)
        file_modified = datetime.fromtimestamp(os.path.getmtime(ARTICLES_FILE_PATH))

        return JsonResponse({
            'success': True,
            'message': 'Файл успешно загружен',
            'filename': 'articles.xlsx',
            'size': file_size,
            'modified': file_modified.strftime('%Y-%m-%d %H:%M:%S')
        })

    except Exception as e:
        return JsonResponse(
            {'error': f'Ошибка при загрузке файла: {str(e)}'},
            status=500
        )


@require_http_methods(['GET'])
def download_articles_file(request):
    """
    Скачивание файла артикулов
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(ARTICLES_FILE_PATH):
            return JsonResponse(
                {'error': 'Файл артикулов не найден'},
                status=404
            )

        # Добавляем дату к имени файла
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
        filename_with_date = f'articles_{timestamp}.xlsx'

        # Читаем файл
        with open(ARTICLES_FILE_PATH, 'rb') as f:
            file_data = f.read()

        # Создаем ответ
        response = HttpResponse(
            file_data,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        response['Content-Disposition'] = f'attachment; filename="{filename_with_date}"'
        response['Content-Length'] = len(file_data)

        return response

    except Exception as e:
        return JsonResponse(
            {'error': f'Ошибка при скачивании файла: {str(e)}'},
            status=500
        )


@require_http_methods(['GET'])
def download_articles_template(request):
    """
    Скачивание шаблона для артикулов
    """
    try:
        # Проверяем существование файла шаблона
        if not os.path.exists(TEMPLATE_FILE_PATH):
            return JsonResponse(
                {'error': 'Файл шаблона не найден'},
                status=404
            )

        # Скачиваем с датой
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d_%H-%M-%S')
        filename_with_date = f'articles_template_{timestamp}.xlsx'

        # Читаем файл шаблона
        with open(TEMPLATE_FILE_PATH, 'rb') as f:
            file_data = f.read()

        # Создаем ответ
        response = HttpResponse(
            file_data,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        response['Content-Disposition'] = f'attachment; filename="{filename_with_date}"'
        response['Content-Length'] = len(file_data)

        return response

    except Exception as e:
        return JsonResponse(
            {'error': f'Ошибка при скачивании шаблона: {str(e)}'},
            status=500
        )



