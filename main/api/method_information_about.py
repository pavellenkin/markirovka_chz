from main.api.unified_authentication_true_api import auth, load_token
import requests

def method_cises_search():
    status_load, token = load_token()
    if not status_load:
        status, token = auth()
    url = "https://markirovka.crpt.ru/api/v4/true-api/cises/search"
    header = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    request_s = {
        "filter": {
            "productGroups":["autofluids"]},
            "pagination": {
            "perPage":999
            }



    }
    send = requests.post(url, headers=header, json=request_s, verify=False)
    print("Status Code create document: ", send.status_code, "\n")
    # print("Response Body: ", send.content.decode(), "\n")
    return send.status_code, send.content.decode()