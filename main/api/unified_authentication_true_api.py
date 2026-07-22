import requests
import json
from main.api.cert import load_cert


"""
https://markirovka.crpt.ru/api/v3/true-api

https://markirovka.crpt.ru/api/v4/true-api
"""

def auth():
    oms_key = "a68f074f-ba9e-4e36-aadf-e18c1c9f2b4e"
    url_key = f"https://markirovka.crpt.ru/api/v3/true-api/auth/key"
    header = {
        "accept": "application/json"
    }
    get_api = requests.get(url_key, headers=header)
    response_dict = json.loads(get_api.content.decode())
    uuid = response_dict['uuid']
    data = response_dict['data']
    # print("UUID: ", uuid)
    # print("DATA: ", data)
    status_signature, signed, error_message = load_cert(data)
    if status_signature is False:
        return False, error_message
    # print("OMS_KEY: ", oms_key, "\n")
    url_auth = f"https://markirovka.crpt.ru/api/v3/true-api/auth/simpleSignIn"
    header_post = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    body_post = {
        "uuid" : uuid,
        "data" : signed
    }
    post_auth_api = requests.post(
        url=url_auth,
        headers=header_post,
        json=body_post
    )
    if post_auth_api.status_code == 200:
        try:
            token_dict = json.loads(post_auth_api.content.decode())
            with open('temp.cfg', 'w') as file:
                file.write(token_dict['token'])
                print("SAVE TOKEN")
            return True, token_dict['token']
        except Exception:
            import sys
            from error_log.views import create_item_error_log
            exc_type, exc_value, exc_traceback = sys.exc_info()
            frame = exc_traceback.tb_frame
            lineno = exc_traceback.tb_lineno
            create_item_error_log(
                frame.f_code.co_filename, exc_type, exc_value, lineno
            )
            return False, ""
    else:
        return False, ""


# метод загрузки токена авторизации из файла
def load_token():
    try:
        with open('temp.cfg', 'r') as file:
            content = file.read()
            print("LOAD TOKEN")
        return True, content.replace("\n","").replace("\t", "")
    except Exception:
        import sys
        from error_log.views import create_item_error_log
        exc_type, exc_value, exc_traceback = sys.exc_info()
        frame = exc_traceback.tb_frame
        lineno = exc_traceback.tb_lineno
        create_item_error_log(
            frame.f_code.co_filename, exc_type, exc_value, lineno
        )
        return False, ""