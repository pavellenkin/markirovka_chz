import requests
import json
from main.api.unified_authentication_true_api import auth, load_token


# Метод создания нового задания на выгрузку
# Получение списка КИ участника оборота товаров по заданному фильтру
def dispenser_task_init(data):
    while True:
        # загружаем сохраненный токен, если его нет, то получаем его
        status_load, token = load_token()
        if not status_load:
            status, token = auth()
            # если авторизация с ошибкой, то отдаем сообщение, возвращаем False
            if status is False:
                return False, token
            # информация о методах
            """
               url="https://markirovka.crpt.ru/api/v3/true-api/cises/aggregated/list - метод получения информации об агрегации

               https://markirovka.crpt.ru/api/v3/true-api/cises/info?pg= - метод получения информации КИ
            """
        url = "https://markirovka.crpt.ru/api/v3/true-api/dispenser/tasks"
        # заголовок авторизации
        header = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        }


        # POST запрос
        try:
            send = requests.post(url, headers=header, json=data, timeout=7)
            print("Status Code: ", send.status_code, "\n")
            print("Response: ", send.content.decode(), "\n")
            # проверка статуса запроса и получение сообщения от сервера
            if send.status_code == 200:
                print("RETURN OK CONTENT")
                return True, send.content.decode()
            elif send.status_code == 401:
                print("Exception: REBASE TOKEN")
                status, token = auth()
            elif send.status_code == 403:
                try:
                    error_message = json.loads(send.content.decode())[0]['errorMessage']
                    return False, error_message
                except:
                    return False, "Код идентификации не найден"
            else:
                return False, "Код идентификации не найден"
        except requests.exceptions.ConnectionError:
            return False, f"Error: Имя или услуга неизвестны"
        except requests.exceptions.Timeout:
            return False, f"TimeOut: Сервис не доступен"



# Метод получения статуса задания на выгрузку
def dispenser_task_status(taskid):
    while True:
        # загружаем сохраненный токен, если его нет, то получаем его
        status_load, token = load_token()
        if not status_load:
            status, token = auth()
            # если авторизация с ошибкой, то отдаем сообщение, возвращаем False
            if status is False:
                return False, token
        url = f"https://markirovka.crpt.ru/api/v3/true-api/dispenser/tasks/{taskid}?pg=43"
        # заголовок авторизации
        header = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        }
        # GET запрос
        try:
            send = requests.get(url, headers=header, timeout=7)
            print("Status Code: ", send.status_code, "\n")
            print("Response: ", send.content.decode(), "\n")
            # проверка статуса запроса и получение сообщения от сервера
            if send.status_code == 200:
                print("RETURN OK CONTENT")
                return True, send.content.decode()
            elif send.status_code == 401:
                print("Exception: REBASE TOKEN")
                status, token = auth()
            elif send.status_code == 403:
                try:
                    error_message = json.loads(send.content.decode())[0]['errorMessage']
                    return False, error_message
                except:
                    return False, "Код идентификации не найден"
            else:
                return False, "Код идентификации не найден"
        except requests.exceptions.ConnectionError:
            return False, f"Error: Имя или услуга неизвестны"
        except requests.exceptions.Timeout:
            return False, f"TimeOut: Сервис не доступен"


# Метод получения результирующих ID выгрузок данных
def dispenser_result_ids(taskid, pg):
    print("TASK: ", taskid)
    while True:
        # загружаем сохраненный токен, если его нет, то получаем его
        status_load, token = load_token()
        if not status_load:
            status, token = auth()
            # если авторизация с ошибкой, то отдаем сообщение, возвращаем False
            if status is False:
                return False, token
        url = f"https://markirovka.crpt.ru/api/v3/true-api/dispenser/results?page=0&pg={pg}&size=12"
        # заголовок авторизации
        header = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        }
        # GET запрос
        try:
            send = requests.get(url, headers=header, timeout=7)
            print("Status Code: ", send.status_code, "\n")
            print("Response: ", send.content.decode(), "\n")
            # проверка статуса запроса и получение сообщения от сервера
            if send.status_code == 200:
                print("RETURN OK CONTENT")
                ids_result = None
                json_data = json.loads(send.content.decode())
                print(json_data)
                if 'list' in json_data:
                    for item in json_data['list']:
                        if item['taskId'] == taskid:
                            ids_result = item['id']

                return True, ids_result
            elif send.status_code == 401:
                print("Exception: REBASE TOKEN")
                status, token = auth()
            elif send.status_code == 403:
                try:
                    error_message = json.loads(send.content.decode())[0]['errorMessage']
                    return False, error_message
                except:
                    return False, "Результирующих ID не найдено"
            else:
                return False, "Результирующих ID не найдено"
        except requests.exceptions.ConnectionError:
            return False, f"Error: Имя или услуга неизвестны"
        except requests.exceptions.Timeout:
            return False, f"TimeOut: Сервис не доступен"


# Метод получения ZIP-файла выгрузки
def dispenser_result(taskid, pg):
    while True:
        # загружаем сохраненный токен, если его нет, то получаем его
        status_load, token = load_token()
        if not status_load:
            status, token = auth()
            # если авторизация с ошибкой, то отдаем сообщение, возвращаем False
            if status is False:
                return False, token
        url = f"https://markirovka.crpt.ru/api/v3/true-api/dispenser/results/{taskid}/file?pg={pg}"
        # заголовок авторизации
        header = {
            "accept": "*/*",
            "Authorization": f"Bearer {token}",
        }
        # GET запрос

        try:
            send = requests.get(url, headers=header, timeout=7)
            print("Status Code: ", send.status_code, "\n")
            print("FILE Response: ", send.headers, "\n")
            # проверка статуса запроса и получение сообщения от сервера
            if send.status_code == 200:
                # Определяем имя файла из Content-Disposition или создаем свое
                content_disposition = send.headers.get('Content-Disposition')
                if content_disposition and 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[1].strip('"')
                else:
                    filename = f"report_{taskid}.csv"  # или .xlsx, .zip и т.д.

                # Сохраняем файл
                with open(filename, 'wb') as f:
                    f.write(send.content)

                print(f"Файл сохранен как: {filename}")
                return True, send.content.decode()
            elif send.status_code == 401:
                print("Exception: REBASE TOKEN")
                status, token = auth()
            elif send.status_code == 403:
                try:
                    error_message = json.loads(send.content.decode())[0]['errorMessage']
                    return False, error_message
                except:
                    return False, "Код идентификации не найден"
            else:
                return False, "Код идентификации не найден"
        except requests.exceptions.ConnectionError:
            return False, f"Error: Имя или услуга неизвестны"
        except requests.exceptions.Timeout:
            return False, f"TimeOut: Сервис не доступен"


