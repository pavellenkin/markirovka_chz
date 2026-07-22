from main.api.unified_authentication_true_api import auth, load_token
import requests
import json
import base64
from main.api.cert import true_cert
"""
    CIS_NOTICE - Уведомление о состоянии кодов (JSON)
    MANUAL — формат * .json
    XML — формат * .xml
    CSV — формат * .csv
        "document_format":"MANUAL",
        "product_document":"<Тело формируемого документа в base64>",
        "type":"CIS_NOTICE",
        "signature":"<Откреплённая подпись для product_document в base64>"
"""

def base_crypt(body):
    str_body = json.dumps(body, separators=(',', ':'))
    result = str_body
    return result

"""
type_doc - тип документа
body_doc - тело документа
format_doc - формат документа (MANUAL - json)

"""

def check_status_document(number_doc):
    numb_attempts = 0
    while True:
        if numb_attempts >= 12:
            return False, "Документ не найден в ГИС МТ"
        numb_attempts += 1
        status_load, token = load_token()
        if not status_load:
            status, token = auth()
            if status is False:
                return False, token
        header = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        }
        url_check_doc = f"https://markirovka.crpt.ru/api/v4/true-api/doc/{number_doc}/info?pg=autofluids"
        try:
            send_check_doc = requests.get(url_check_doc, headers=header, verify=False, timeout=7)
            if send_check_doc.status_code == 200 or send_check_doc.status_code == 201:
                try:
                    send_check_doc_dict = json.loads(send_check_doc.content.decode())
                    status_document = send_check_doc_dict[0]['status']
                    if status_document == "CHECKED_OK":
                        return True, send_check_doc.content.decode()
                    else:
                        return False, f"{send_check_doc_dict[0]['errors'][0]}"
                except KeyError:
                    return False, "Error: Сервис не доступен"
                except TypeError:
                    return False, "Error: Сервис не доступен"
        except requests.exceptions.Timeout:
            return False, f"TimeOut: Сервис не доступен"
        except requests.exceptions.ConnectionError:
            return False, f"Error: Имя или услуга неизвестны"


def method_create_doc(type_doc, body_doc, format_doc):
    while True:
        status_load, token = load_token()
        if not status_load:
            status, token = auth()
            if status is False:
                return False, token
        url = "https://markirovka.crpt.ru/api/v3/true-api/lk/documents/create?pg=autofluids"
        header = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
        }
        body_base = base_crypt(body_doc)
        message_bytes = body_base.encode("utf-8")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("utf-8")

        valid_signature = true_cert(str(base64_message))

        request_s = {
                  "document_format":format_doc,
                  "product_document":str(base64_message),
                  "type":type_doc,
                  "signature":str(valid_signature)
        }
        try:
            create_doc = requests.post(url, headers=header, json=request_s, verify=False, timeout=7)
            if create_doc.status_code == 200 or create_doc.status_code == 201:
                return True, create_doc.content.decode()
            else:
                return False, f"{create_doc.status_code}: Сервис не доступен"
        except requests.exceptions.Timeout:
            return False, f"TimeOut: Сервис не доступен"
        except requests.exceptions.ConnectionError:
            return False, f"Error: Имя или услуга неизвестны"
