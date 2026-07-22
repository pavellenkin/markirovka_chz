from main.api.unified_authentication_true_api import auth, load_token
import json
import base64
from main.api.cert import true_cert
import requests

"""

POST <url стенда>/api/v3/order?omsId={omsId}


26 Косметика, бытовая химия и товары
личной гигиены chemistry

36 Моторные масла autofluids

templateId:

46 | 01 GTIN + 21 SERIAL(6 chars) + 91(4 chars) + 92(44 chars) Косметика, бытовая химия и товары личной гигиены Строка (string)

60 | 01 GTIN + 21 SERIAL(13 chars) + 93(4 chars) Моторные масла Строка (string)

serialNumberType:

SELF_MADE | Самостоятельно Строка (string)
OPERATOR | Оператором ГИС МТ Строка (string)

{
  "productGroup": "autofluids",
  "products": [
     {
      "gtin":"04611111111111",          - Код товара (GTIN).Строковое значение
      "quantity":5,                     - Количество КМ.
      "serialNumberType":"OPERATOR",    - Способ генерации серийных номеров
      "templateId":60                   - Формат кода
      }
  ],
"""

def base_crypt(body):
    str_body = json.dumps(body, separators=(',', ':'))
    result = str_body
    return result


def order(gtin, quantity):
    # while True:
    status, token = auth_suzgrid()
    body = {
        "productGroup": "autofluids",
        "products": [
            {
                "gtin": "04650532210123",
                "quantity":2,
                "serialNumberType":"OPERATOR",
                "templateId": 60,
                "cisType":"UNIT"
            }
        ],
        "attributes": {
            "releaseMethodType": "REAPPLY",
            "createMethodType": "SELF_MADE",
            "paymentType": 1,
        }
    }
    body_base = base_crypt(body)
    # #
    message_bytes = body_base.encode("utf-8")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("utf-8")
    # #
    valid_signature = true_cert(str(base64_message))
    #
    # request = {
    #        "document_format":"MANUAL",
    #        "product_document":str(base64_message),
    #        "type":"CIS_INFORMATION_CHANGE",
    #        "signature":str(valid_signature)
    # }


    url = "https://suzgrid.crpt.ru/api/v3/order?omsId=7dafbede-4e3f-4673-9d63-78f15c490cf5"
    print(token)
    header = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": f"token {token}",
        "X-Signature": str(valid_signature)
        # #
        # "clientToken" : "a68f074f-ba9e-4e36-aadf-e18c1c9f2b4e"
    }

    send = requests.post(url, headers=header, json=body, verify=False)
    print("Status Code: ", send.status_code, "\n")
    print("ORDER")
    print("Response: ", send.content.decode(), "\n")
        # time.sleep(8)
        # numb_attempts = 0
        # while True:
        #     if numb_attempts >= 12:
        #         return False, "BadRequest"
        #     numb_attempts += 1
        #     print("ATTEMPTS: ", numb_attempts, "\n")
        #     try:
        #         url_check_doc = f"https://markirovka.crpt.ru/api/v4/true-api/doc/{send.content.decode()}/info?pg=autofluids"
        #         send_check_doc = requests.get(url_check_doc, headers=header, verify=False)
        #         send_check_doc_dict = json.loads(send_check_doc.content.decode())
        #         status_document = send_check_doc_dict[0]['status']
        #         print("Status send check document: ", send_check_doc.status_code)
        #         print("Status check document: ", send_check_doc.content.decode())
        #         if send.status_code==200 or send.status_code==201:
        #             if status_document == "CHECKED_OK":
        #                 return True, send.content.decode()
        #             else:
        #                 message_body = f"{send_check_doc_dict[0]['errors'][0]}"
        #                 print(message_body)
        #                 return False, message_body
        #
        #         elif send.status_code == 401:
        #             status, token = auth()
        #         else:
        #             return False, "BadRequest"
        #     except:
        #         # print("- - - ERROR - - -\n")
        #         pass