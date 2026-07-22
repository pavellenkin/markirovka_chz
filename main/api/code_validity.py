import json
from csv import excel
from unicodedata import normalize
from main.api.unified_authentication_true_api import auth, load_token
import requests
from textwrap import wrap

"""
{FNC1}010461008041021521e'?xOJHdNYNFl\u001D91EE11\u001D92T5OX4wpd5QPymkC3U/aJZQrishzxCOeJUi/grI7GxIo=

0104607075783508215vrC:QssM"A*'91EE11923OkyjJhugj/ZcU69pvRK5qyZw1ttEANE5tu8/sVhiP0=

010461008041021521e1xEFmCC5qLt?91EE1192pZoneacYBzdoe2sHu8Wc7UPKI91sVKuEPyvOuzXlq+E=
010461008041021521e1xEFmCC5qLt?91EE1192pZoneacYBzdoe2sHu8Wc7UPKI91sVKuEPyvOuzXlq+E=
010461008041021521e,s;r!t%BroGd\x1d91EE11\x1d929GkndNAXaeC4gMRT4LHKh/EkGRn4+gUPdrWMpbtkejw=

010461008041021521e,s;r!t%BroGd91EE11929GkndNAXaeC4gMRT4LHKh/EkGRn4+gUPdrWMpbtkejw=
010461008041021521e,s;r!t%BroGd91EE11929GkndNAXaeC4gMRT4LHKh/EkGRn4+gUPdrWMpbtkejw=
b']d2010461008041021521e,s;r!t%BroGd\x1d91EE11\x1d929GkndNAXaeC4gMRT4LHKh/EkGRn4+gUPdrWMpbtkejw='


"""

def format_code(code):
    print(code)
    code = f"{code[:31]}\u001D{code[31:37]}\u001D{code[37:]}"
    return code

def code_validity(code):

    numb_attempts = 0
    while True:
        if numb_attempts >= 12:
            return False, "🐛 # ОШИБКА #"
        numb_attempts += 1
        try:
            status_load, token = load_token()
            if not status_load:
                status, token = auth()
            url = "https://markirovka.crpt.ru/api/v3/true-api/cises/check"
            #code = code.replace('\x1d', '')
            print("VALIDITY_CODE: ", code)
            request = {
                "codes":[f"{code}"]
            }
            header = {
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
            }
            send = requests.post(url, headers=header, json=request, verify=False)
            print("Status Code: ", send.status_code, "\n")
            print("VALIDITY")
            print("Response: ", send.content.decode(), "\n")
            response_result = json.loads(send.content.decode())['result']
            print(response_result)
            if response_result is True:
                return True, "✅ КМ валиден"
            else:
                return False, "⚠️ КМ не валиден"
        except Exception:
            import sys
            from error_log.views import create_item_error_log
            exc_type, exc_value, exc_traceback = sys.exc_info()
            frame = exc_traceback.tb_frame
            lineno = exc_traceback.tb_lineno
            create_item_error_log(
                frame.f_code.co_filename, exc_type, exc_value, lineno
                        )
            return False, "🐛 # ОШИБКА #"