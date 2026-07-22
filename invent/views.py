import json
import os

from django.shortcuts import render
from django.views.decorators.cache import cache_control
from invent.models import InventoryCodes
from django.http import JsonResponse, HttpResponse
import sys
from error_log.views import create_item_error_log
import pandas as pd
from openpyxl import load_workbook

def all_keys_exist(dictionary, keys_list):
    for key in keys_list:
        if key not in dictionary:
            dictionary[key] = ""
    return dictionary


from datetime import datetime, timedelta


def update_excel_record(file_path, art, cis):
    """
    Обновляет существующую запись в Excel файле или добавляет новую
    Со статусом "overwrite" при обновлении существующей записи
    """
    try:
        # Получаем текущее время UTC+3
        moscow_time = datetime.utcnow() + timedelta(hours=3)
        time_str = moscow_time.strftime('%Y-%m-%d %H:%M:%S')

        # Проверяем существует ли файл
        if not os.path.exists(file_path):
            # Если файла нет, создаем новый (все столбцы как строки)
            df = pd.DataFrame({
                'art': [str(art)],
                'cis': [str(cis)],
                'time_record': [time_str],
                'status': ['item']
            })
            df.to_excel(file_path, index=False)
            print(f"Создан новый Excel файл с записью: артикул {art}, CIS {cis}, статус: item")
            return

        # Читаем существующий файл - ВАЖНО: все столбцы как строки
        df = pd.read_excel(file_path, dtype=str)  # <-- КЛЮЧЕВОЕ ИЗМЕНЕНИЕ

        # Проверяем наличие необходимых колонок
        if 'art' not in df.columns:
            df['art'] = ''
        if 'cis' not in df.columns:
            df['cis'] = ''
        if 'time_record' not in df.columns:
            df['time_record'] = ''
        if 'status' not in df.columns:
            df['status'] = ''

        # Приводим значения к строке для корректного сравнения
        df['cis'] = df['cis'].astype(str)
        df['art'] = df['art'].astype(str)

        # Ищем запись с таким CIS (теперь оба сравниваются как строки)
        mask = df['cis'] == str(cis)

        if mask.any():
            # Обновляем существующую запись (overwrite)
            df.loc[mask, 'art'] = str(art)
            df.loc[mask, 'time_record'] = time_str
            df.loc[mask, 'status'] = 'overwrite'
            print(f"Обновлена запись в Excel: CIS {cis}, новый артикул {art}, время {time_str}, статус: overwrite")
        else:
            # Добавляем новую запись
            new_row = pd.DataFrame({
                'art': [str(art)],
                'cis': [str(cis)],
                'time_record': [time_str],
                'status': ['item']
            })
            df = pd.concat([df, new_row], ignore_index=True)
            print(f"Добавлена новая запись в Excel: артикул {art}, CIS {cis}, статус: item")

        # Сохраняем файл
        df.to_excel(file_path, index=False)
        print(f"Excel файл успешно обновлен: {file_path}")

    except Exception as e:
        print(f"Ошибка при обновлении Excel файла: {str(e)}")
        raise e


from datetime import datetime
import pytz


def add_to_excel(file_name, article, code):
    """
    Добавляет запись в Excel файл с временем и статусом
    """
    # Получаем текущее время с часовым поясом +3
    tz = pytz.timezone('Europe/Moscow')  # Москва UTC+3
    current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    # Проверяем существует ли файл
    if os.path.exists(file_name):
        # Файл существует - читаем и добавляем
        df = pd.read_excel(file_name)

        # Проверяем наличие колонок, если нет - создаем
        if 'time_record' not in df.columns:
            df['time_record'] = None
        if 'status' not in df.columns:
            df['status'] = None

        new_row = pd.DataFrame({
            'art': [article],
            'cis': [code],
            'time_record': [current_time],
            'status': ['item']
        })
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        # Файла нет - создаем новый с данными
        df = pd.DataFrame({
            'art': [article],
            'cis': [code],
            'time_record': [current_time],
            'status': ['item']
        })
        print(f"Файл {file_name} не найден. Создан новый файл.")

    # Сохраняем файл
    df.to_excel(file_name, index=False)
    print(f"✓ Добавлено: {article} | {code} | {current_time} | item")


def remove_duplicates_keep_first(lst):
    """Удаляет дубликаты, оставляя первое вхождение"""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result

@cache_control(no_cache=True)
def invent(request):
    # Проверяем существование файла
    if os.path.exists('articles.xlsx'):
        # Файл существует - читаем
        df = pd.read_excel('articles.xlsx')
        articles_list = df.iloc[:, 0].dropna().astype(str).tolist()
        print(f"Загружено {len(articles_list)} артикулов из файла")
    else:
        # Файла нет - используем пустой список или список по умолчанию
        print("Файл articles.xlsx не найден!")
        articles_list = []  # или можно задать список по умолчанию

    # Создаем контекст
    context = {
        'articles': json.dumps(articles_list)
    }

    default_key_list = [
        "cis", "gtin", "productName", "applicationDate", "introducedDate", "manufacturerInn",
        "manufacturerName", "requestedCis", "tnVedEaes", "tnVedEaesGroup", "productGroupId",
        "productGroup", "brand", "producedDate", "emissionDate", "emissionType", "packageType",
        "generalPackageType", "ownerInn", "ownerName", "status", "statusEx", "producerInn",
        "producerName", "expirationDate", "child"
    ]

    if request.method == "POST":
        key_value = request.POST.get("key_value")
        art = request.POST.get("art")
        print(art, "  | ", key_value)

        # Обработка перезаписи
        if key_value == "overwrite":
            data_base = request.session.pop('data_base', [])
            print(data_base)
            if data_base:
                set_data = data_base[0]['cisInfo']
                result_check_dict = all_keys_exist(
                    dictionary=set_data,
                    keys_list=default_key_list
                )
                set_data = result_check_dict

                # Проверяем существует ли запись с таким cis
                if InventoryCodes.objects.filter(cis=set_data['cis']).exists():
                    try:
                        # Обновляем существующую запись
                        invent_item = InventoryCodes.objects.get(cis=set_data['cis'])

                        # Обновляем все поля
                        invent_item.art = art
                        invent_item.gtin = set_data['gtin']
                        invent_item.productName = set_data['productName']
                        invent_item.applicationDate = set_data['applicationDate']
                        invent_item.introducedDate = set_data['introducedDate']
                        invent_item.manufacturerInn = set_data['manufacturerInn']
                        invent_item.manufacturerName = set_data['manufacturerName']
                        invent_item.requestedCis = set_data['requestedCis']
                        invent_item.tnVedEaes = set_data['tnVedEaes']
                        invent_item.tnVedEaesGroup = set_data['tnVedEaesGroup']
                        invent_item.productGroupId = set_data['productGroupId']
                        invent_item.productGroup = set_data['productGroup']
                        invent_item.brand = set_data['brand']
                        invent_item.producedDate = set_data['producedDate']
                        invent_item.emissionDate = set_data['emissionDate']
                        invent_item.emissionType = set_data['emissionType']
                        invent_item.packageType = set_data['packageType']
                        invent_item.generalPackageType = set_data['generalPackageType']
                        invent_item.ownerInn = set_data['ownerInn']
                        invent_item.ownerName = set_data['ownerName']
                        invent_item.status = set_data['status']
                        invent_item.statusEx = set_data['statusEx']
                        invent_item.producerInn = set_data['producerInn']
                        invent_item.producerName = set_data['producerName']
                        invent_item.expirationDate = set_data['expirationDate']
                        invent_item.child = set_data['child']

                        invent_item.save()

                        # Обновляем запись в Excel файле
                        update_excel_record('TSD_smart.xlsx', art, set_data['cis'])

                        return JsonResponse({
                            "status": "success",
                            "message": f'<b>Запись перезаписана</b><br><b>Артикул:</b> {art}<br><b>КИ:</b> {set_data["cis"]}'
                        })

                    except Exception as e:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        frame = exc_traceback.tb_frame
                        lineno = exc_traceback.tb_lineno
                        create_item_error_log(
                            frame.f_code.co_filename, exc_type, exc_value, lineno
                        )
                        return JsonResponse({
                            "status": "error",
                            "message": f"Ошибка при перезаписи в базу<br>"
                                       f"{str(exc_type.__name__)} in {str(exc_value)} :line {lineno}<br>"
                                       f"{frame.f_code.co_filename}"
                        })
                else:
                    # Если записи нет, создаем новую
                    try:
                        invent_item = InventoryCodes.objects.create(
                            art=art,
                            cis=set_data['cis'],
                            gtin=set_data['gtin'],
                            productName=set_data['productName'],
                            applicationDate=set_data['applicationDate'],
                            introducedDate=set_data['introducedDate'],
                            manufacturerInn=set_data['manufacturerInn'],
                            manufacturerName=set_data['manufacturerName'],
                            requestedCis=set_data['requestedCis'],
                            tnVedEaes=set_data['tnVedEaes'],
                            tnVedEaesGroup=set_data['tnVedEaesGroup'],
                            productGroupId=set_data['productGroupId'],
                            productGroup=set_data['productGroup'],
                            brand=set_data['brand'],
                            producedDate=set_data['producedDate'],
                            emissionDate=set_data['emissionDate'],
                            emissionType=set_data['emissionType'],
                            packageType=set_data['packageType'],
                            generalPackageType=set_data['generalPackageType'],
                            ownerInn=set_data['ownerInn'],
                            ownerName=set_data['ownerName'],
                            status=set_data['status'],
                            statusEx=set_data['statusEx'],
                            producerInn=set_data['producerInn'],
                            producerName=set_data['producerName'],
                            expirationDate=set_data['expirationDate'],
                            child=set_data['child']
                        )
                        invent_item.save()

                        if invent_item.pk:
                            add_to_excel('TSD_smart.xlsx', art, set_data['cis'])
                            return JsonResponse({
                                "status": "success",
                                "message": f'<b>Запись сохранена</b><br><b>Артикул:</b> {art}<br><b>КИ:</b> {set_data["cis"]}'
                            })
                        else:
                            return JsonResponse({
                                "status": "error",
                                "message": "Запись не сохранена"
                            })

                    except Exception:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        frame = exc_traceback.tb_frame
                        lineno = exc_traceback.tb_lineno
                        create_item_error_log(
                            frame.f_code.co_filename, exc_type, exc_value, lineno
                        )
                        return JsonResponse({
                            "status": "error",
                            "message": f"Ошибка при записи в базу<br>"
                                       f"{str(exc_type.__name__)} in {str(exc_value)} :line {lineno}<br>"
                                       f"{frame.f_code.co_filename}"
                        })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Данные отсутствуют"
                })

        # Обработка успешного сохранения (key_value == "success")
        elif key_value == "success":
            data_base = request.session.pop('data_base', [])
            if data_base:
                set_data = data_base[0]['cisInfo']
                result_check_dict = all_keys_exist(
                    dictionary=set_data,
                    keys_list=default_key_list
                )
                set_data = result_check_dict

                if InventoryCodes.objects.filter(cis=set_data['cis']).exists():
                    request.session['data_base'] = data_base
                    request.session.save()  # Явно сохраняем сессию
                    return JsonResponse({
                        "status": "addon",
                        "message": "Запись уже существует",
                        "art": art,
                        "key_value": "overwrite"
                    })
                else:
                    try:
                        invent_item = InventoryCodes.objects.create(
                            art=art,
                            cis=set_data['cis'],
                            gtin=set_data['gtin'],
                            productName=set_data['productName'],
                            applicationDate=set_data['applicationDate'],
                            introducedDate=set_data['introducedDate'],
                            manufacturerInn=set_data['manufacturerInn'],
                            manufacturerName=set_data['manufacturerName'],
                            requestedCis=set_data['requestedCis'],
                            tnVedEaes=set_data['tnVedEaes'],
                            tnVedEaesGroup=set_data['tnVedEaesGroup'],
                            productGroupId=set_data['productGroupId'],
                            productGroup=set_data['productGroup'],
                            brand=set_data['brand'],
                            producedDate=set_data['producedDate'],
                            emissionDate=set_data['emissionDate'],
                            emissionType=set_data['emissionType'],
                            packageType=set_data['packageType'],
                            generalPackageType=set_data['generalPackageType'],
                            ownerInn=set_data['ownerInn'],
                            ownerName=set_data['ownerName'],
                            status=set_data['status'],
                            statusEx=set_data['statusEx'],
                            producerInn=set_data['producerInn'],
                            producerName=set_data['producerName'],
                            expirationDate=set_data['expirationDate'],
                            child=set_data['child']
                        )
                        invent_item.save()

                        if invent_item.pk:
                            add_to_excel('TSD_smart.xlsx', art, set_data['cis'])
                            return JsonResponse({
                                "status": "success",
                                "message": f'<b>Запись сохранена</b><br><b>Артикул:</b> {art}<br><b>КИ:</b> {set_data["cis"]}'
                            })
                        else:
                            return JsonResponse({
                                "status": "error",
                                "message": "Запись не сохранена"
                            })

                    except Exception:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        frame = exc_traceback.tb_frame
                        lineno = exc_traceback.tb_lineno
                        create_item_error_log(
                            frame.f_code.co_filename, exc_type, exc_value, lineno
                        )
                        return JsonResponse({
                            "status": "error",
                            "message": f"Ошибка при записи в базу<br>"
                                       f"{str(exc_type.__name__)} in {str(exc_value)} :line {lineno}<br>"
                                       f"{frame.f_code.co_filename}"
                        })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Данные отсутствуют"
                })
        elif key_value == "content":
            print(art, "  | ", key_value)
            codes_list = request.POST.get('codes_list')

            # Если codes_list пришел как строка JSON, парсим его
            if codes_list:
                try:
                    save_count = 0
                    update_count = 0
                    codes_list = json.loads(codes_list)
                    message_context = ""

                    cleaned = remove_duplicates_keep_first(codes_list)

                    print(cleaned)

                    for item in cleaned:
                        if "]" in item[:3]:
                            item = item[3:]
                        spl_string = item[:31]

                        if InventoryCodes.objects.filter(cis=spl_string).exists():
                            invent_item = InventoryCodes.objects.get(cis=spl_string)
                            invent_item.art = art
                            invent_item.save()
                            update_excel_record('TSD_smart.xlsx', art, spl_string)
                            update_count += 1
                        else:
                            invent_item = InventoryCodes.objects.create(
                                art=art,
                                cis=spl_string
                            )
                            invent_item.save()
                            if invent_item.pk:
                                add_to_excel('TSD_smart.xlsx', art, spl_string)
                                save_count += 1
                        if update_count > 0:
                            message_context = (f'<b>Запись сохранена</b><br><b>Артикул:</b> {art}<br>'
                                               f'<b>Добавлено КИ:</b> {save_count}<br>'
                                               f'<b>Обнавлено КИ:</b> {update_count}'
                                               )
                        else:
                            message_context = f'<b>Запись сохранена</b><br><b>Артикул:</b> {art}<br><b>Кол-во КИ:</b> {save_count}'

                    return JsonResponse(
                        {
                            'status': 'success',
                            "message": f'{message_context}'
                        })


                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)})





    return render(request, "invent.html", context=context)


