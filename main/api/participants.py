import requests
import json
from main.api.unified_authentication_true_api import auth, load_token


# Метод проверки регистрации участников оборота товаров по ИНН в ГИС МТ
def get_participants(inn):
    while True:
        # загружаем сохраненный токен, если его нет, то получаем его
        status_load, token = load_token()
        if not status_load:
            status, token = auth()
            # если авторизация с ошибкой, то отдаем сообщение, возвращаем False
            if status is False:
                return False, token

        url = f"https://markirovka.crpt.ru/api/v3/true-api/participants?inns={inn}"
        # заголовок авторизации
        header = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        }

        try:
            send = requests.get(url, headers=header, timeout=7)
            print("Status Code: ", send.status_code, "\n")
            print("Response: ", send.content.decode(), "\n")
            # проверка статуса запроса и получение сообщения от сервера
            if send.status_code == 200:
                print("RETURN OK CONTENT")
                return True, json.loads(send.content.decode())[0]
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