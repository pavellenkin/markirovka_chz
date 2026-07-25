import json
import re
import sys
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from main.api.guide_api import status_codes, types_of_packaging
from main.search import (
    get_nac_cat,
    send_link,
    search_inn,
    search_inn_to_file,
    search_inn_to_file_priority,
    search_inn_to_file_priority_gtin,
get_nac_cat_all,
get_nac_cat_all_tm,

# check_tnved, auth_nk
)
from main.api.cises_info import info_ki
from main.api.information_change import information_change

from main.api.code_validity import code_validity
from main.api.cis_notes import cis_notes


"""
]d2 - лидирубщий символ есть
]d1 - нет лидируешего символа
"""


def org_name_replace(name):
    qwery_org = (name.lower()
                 .replace("общество с ограниченной ответственностью", "")
                 .replace("филиал совместного общества с ограниченной ответственностью", "")
                 .replace("акционерное общество", "")
                 .replace("товарищество на вере", "")
                 .replace('"', '')
                 .strip()
                 )
    re_qwery_org = re.sub(r'\s+', ' ',qwery_org)
    return re_qwery_org


@cache_control(no_cache=True)
def header_mainapp(request):
     return render(request, "natcat.html", context={

     })


@cache_control(no_cache=True)
def post_input_code(request):

     if request.method == "POST":
         inn_priority=""
         inn_second_important = ""
         code = request.POST.get("code")
         setup_type = request.POST.get("type")
         print(setup_type)
         if code:
                  if setup_type == "tm":
                      data_list = get_nac_cat_all_tm(code)
                      print(data_list)
                      response_json = {
                          "status": "tm",
                          "list": data_list
                      }
                  else:


                      href, text = get_nac_cat(code)

                      if href is not None:

                            inn_priority_title = "✔ ИНН для заказа кодов маркировки: "
                            org, img, code_shk, identify_item = send_link(href)
                            print("ORG_SEND_LINK: ", org)

                            qwery_org = org_name_replace(org)
                            print("ORG_REPLACE: ", qwery_org)
                            name_company, inn_api = search_inn(qwery_org)
                            print(name_company)
                            priority = search_inn_to_file_priority(code_shk)
                            second_important = search_inn_to_file(
                                qwery_org.lower().replace('"', '')
                            )
                            print("second_important", second_important)
                            if second_important is not None:
                                inn_second_important = (str(second_important)
                                                        .replace("['", "")
                                                        .replace("']", "")
                                                        .replace("', '", "")
                                                        )
                            else:
                                second_important = search_inn_to_file(
                                    name_company.lower().replace('"', '')
                                )
                                inn_second_important = (str(second_important)
                                                        .replace("['", "")
                                                        .replace("']", "")
                                                        .replace("', '", "")
                                                        )
                            if second_important is None:
                                inn_second_important = inn_api


                            if priority is not None:
                                inn_priority = f"{priority}"
                            else:
                                inn_priority_title = "✔ ИНН для заказа кодов маркировки: "
                                inn_priority = "отсутствует"




                            if identify_item:
                                identification = identify_item
                            else:
                                identification = ""
                            response_json = {
                                 "status" : "success",
                                 "data" :{
                                      "code" : code_shk,
                                      "href": href,
                                      "text": text,
                                      "org": org,
                                        "org_title" : "Подписано цифровой подписью:",
                                      "img": img,
                                      "name_company": name_company,
                                      "inn_priority": str(inn_priority),
                                      "inn_priority_title": inn_priority_title,
                                      "inn_second_important": str(inn_second_important),

                                     "identification" : identification
                                 }
                            }
                      else:
                          if code[:1] == '0':
                              code = code[1:]
                          priority_non = search_inn_to_file_priority(code)
                          if priority_non is not None:
                              inn = f"{priority_non}"


                              response_json = {
                                  "status": "href_none",
                                  "data":{
                                      "code": code,
                                      "img": "/static/img/done.png",
                                      "identification": "",
                                      "org_title":"",
                                      "org": "",
                                     "text": "Есть в справочнике товаров 1С Контур.Маркировка",
                                "inn_priority": str(inn),
                                      "inn_second_important": "",
                                      "inn_priority_title": "✔ ИНН для заказа кодов маркировки: ",
                                }

                              }
                          else:
                              response_json = {
                                     "status": "По вашему запросу ничего не найдено",
                                }

         else:
              response_json = {
                        "status": "Пустой запрос",
                   }
         return JsonResponse(response_json)





     return render(request, "ps_in_code.html", context={

     })


@cache_control(no_cache=True)
def st(request):
    status_code, content = cis_notes('010461008041021521e1xEFmCC5qLt?')
    if content:
        # result_content = json.loads(content)
        # body = result_content['result']
        return HttpResponse(f"Status: {status_code}\n{content}" )
    #err, err_num, msg = pydmtx.decode("c:\\data\\hello_world.jpg")
    # if request.method == "GET":
    #     token_request = request.GET.get("request")
    #     if token_request == 'true':
    #         status_token, token = auth()
    #         if status_token is True:
    #             return JsonResponse({"status":"success","data":token})
    #         else:
    #             return JsonResponse({"status": "error"})
    #     else:
    #             return JsonResponse({"status": "BadRequest"})

    return render(request, "st.html", context={

    })

@cache_control(no_cache=True)
def change_date(request):
    if request.method == "POST":
        print("- - - C H A N G E   D A T E - - -")
        apply_request = request.POST.get("apply_request")
        ki = request.POST.get("ki")
        pr_date = request.POST.get("pr_date")
        exp_date = request.POST.get("exp_date")
        if apply_request == 'true':
            print(ki)
            print(pr_date)
            print(exp_date)

            status, result = information_change(ki, pr_date, exp_date)
            if status is True:
                print("information_change_status: ",status , " | ", result)
                result_info, info_mess = info_ki(ki)
                if result_info is True:
                    en_dict = json.loads(info_mess)
                    try:
                        old_produced_date = en_dict[0]['cisInfo']['producedDate'].split("T")[0]
                    except KeyError:
                        old_produced_date = "Отсутствует"
                    try:
                        old_expire_date = en_dict[0]['cisInfo']['expirationDate'].split("T")[0]
                    except KeyError:
                        old_expire_date = "Отсутствует"
                    if old_produced_date == pr_date:
                        change_pr_date = "Дата производства была изменена"
                    else:
                        change_pr_date = "Дата производства без изменений"
                    if old_expire_date == exp_date:
                        change_exp_date = "Срок годности был иземенен"
                    else:
                        change_exp_date = "Срок годности без изменений"

                    return JsonResponse({
                        "status" : "success",
                        "doc_num" : result.replace("Response: ",""),
                        "change_pr_date" : change_pr_date,
                        "change_exp_date" : change_exp_date
                    })
                else:
                    return JsonResponse({"status": "error",
                                         "doc_num" : result.replace("Response: ","")})
            else:

                print("information_change_status: ", status, " | ", result)
                return JsonResponse({"status": "error",
                                     "doc_num": result.replace("204: ","")})



        #     status_token, token = auth()
        #     if status_token is True:
        #         return JsonResponse({"status":"success","data":token})
        #     else:
        #         return JsonResponse({"status": "error"})
        # else:
        #         return JsonResponse({"status": "BadRequest"})
    return render(request, "change_date.html", context={

    })


def replace_separator(code):
    if "[CR]" in code:
        code = code.replace("[CR]","")
    if "[GS]" in code:
        code = code.replace("[GS]", "\x1d")
    if "©" in code:
        code = code.replace("©", "\x1d")
    if "]" in code:
        code = code.replace("]", "\x1d")

    return code



@cache_control(no_cache=True)
def check_code(request):
    if request.method == "POST":
        check_code_input = request.POST.get("check_code")
        if check_code_input:
            #print(check_code_input)
            print("INPUT CODE: ", check_code_input)
            # print(f"INPUT CODE ONE: |{check_code_input.encode("cp1252")}|")
            # print("INPUT CODE TYPE: ", type(check_code_input))
            print("INPUT CODE ENCODE: ", check_code_input.encode())
            print("INPUT CODE HEX: ", check_code_input.encode().hex())
            # print("INPUT CODE length: ", len(check_code_input))
            # print("INPUT CODE ENCODE length: ", len(check_code_input.encode()))
            print(check_code_input[31:37])


            if check_code_input[:3] == "]d2":
                print("Лидирующий символ НАЙДЕН")
                check_code_input = check_code_input.replace("]d2", "")
                check_code_input = replace_separator(check_code_input)
                leading_symbol_info = f'<span class="">Структура Datamatrix ✅ КОРРЕКТНАЯ</span><hr class="hr hr-blurry" />'
            elif check_code_input[:5] == "]C100":
                check_code_input = check_code_input.replace("]C100", "")
                leading_symbol_info = f'<span class="">Структура Datamatrix  🔴 # НЕИЗВЕСТНА #</span><hr class="hr hr-blurry" />'


            elif check_code_input[:3] == "]d1":
                check_code_input = check_code_input.replace("]d1", "")
                check_code_input = replace_separator(check_code_input)
                leading_symbol_info = f'<span class="">Структура Datamatrix ⚠️ НЕКОРРЕКТНАЯ</span><hr class="hr hr-blurry" />'



            else:
                check_code_input = check_code_input.replace("]d1", "")
                check_code_input = replace_separator(check_code_input)
                leading_symbol_info = f'<span class="">Структура Datamatrix  🔴 # НЕИЗВЕСТНА #</span><hr class="hr hr-blurry" />'

            response_validity, valid_text = code_validity(check_code_input)
            if response_validity is True:
                validity_info = f'<span class="">Проверка сервисом {valid_text}</span>'
            else:
                validity_info = f'<span class="">Проверка сервисом {valid_text}</span>'
            #print('\x1d'.join(check_code_input.split('\x1d')[:1]))

            try:
                spl_string ='\x1d'.join(check_code_input.split('\x1d')[:1])
            except:
                spl_string = check_code_input[:31]
            # item_code = spl_string[0]
            result, result_mess = info_ki(spl_string)
            print("Connect API: ", result)
            if result is True:
                en_dict = json.loads(result_mess)

                request.session['data_base'] = en_dict
                try:
                    general_package_type = en_dict[0]['cisInfo']['generalPackageType']
                    text_package_type = types_of_packaging(general_package_type)
                except KeyError:
                    general_package_type = ""
                    text_package_type = ""
                print(general_package_type)


                try:
                    # print(en_dict[0])
                    try:
                        product_name = en_dict[0]['cisInfo']['productName']
                    except KeyError:
                        product_name = ""
                    try:
                        product_gtin = en_dict[0]['cisInfo']['gtin']
                    except KeyError:
                        product_gtin = "Отсутствует"
                    try:
                        product_group = en_dict[0]['cisInfo']['productGroup']
                    except KeyError:
                        product_group = ""
                    try:
                        product_group_id = en_dict[0]['cisInfo']['productGroupId']
                    except KeyError:
                        product_group_id = ""
                    try:
                        producer_name_comp = en_dict[0]['cisInfo']['producerName']
                    except KeyError:
                        producer_name_comp = ""
                    try:
                        owner = en_dict[0]['cisInfo']['ownerName']
                    except KeyError:
                        owner = ""
                    try:
                        owner_inn = en_dict[0]['cisInfo']['ownerInn']
                    except KeyError:
                        owner_inn = ""
                    try:
                        status_mark = en_dict[0]['cisInfo']['status']
                    except KeyError:
                        status_mark = ""
                    try:
                        emission_date = en_dict[0]['cisInfo']['emissionDate'].split("T")[0]
                    except KeyError:
                        emission_date = ""
                    try:
                        introduced_date = en_dict[0]['cisInfo']['introducedDate'].split("T")[0]
                    except KeyError:
                        introduced_date = ""
                    try:
                        emission_type = en_dict[0]['cisInfo']['emissionType']
                    except KeyError:
                        emission_type = ""
                    try:
                        status_ex = en_dict[0]['cisInfo']['statusEx']
                    except KeyError:
                        status_ex = ""

                    child = en_dict[0]['cisInfo']['child']
                    if status_ex:
                        if status_ex != "EMPTY":
                            state_status_ex = "visible"
                            status_ex = status_codes(status_ex)
                        else:
                            state_status_ex = "invisible"
                    else:
                        state_status_ex = "invisible"
                    print(emission_type)
                    if emission_type == "FOREIGN" :
                        type_producer = "Импортер"
                    elif emission_type == "CROSSBORDER":
                        type_producer = "Импортер"
                    else:
                        type_producer = "Производитель"

                    message_status_codes = status_codes(status_mark)
                    if message_status_codes == "В обороте":
                        status_check = f'<hr class="hr hr-blurry" /><h2 class="fw-bold text-success">Товар введен в оборот</h2><hr class="hr hr-blurry" />'
                    else:
                        status_check = f'<hr class="hr hr-blurry" /><h2 class="fw-bold text-danger">{message_status_codes}</h2><hr class="hr hr-blurry" />'

                    audio = "error"
                    button_close = "visible"
                    try:
                        produced_date = en_dict[0]['cisInfo']['producedDate'].split("T")[0]
                    except KeyError:
                        produced_date = "Отсутствует"
                    try:
                        expire_date = en_dict[0]['cisInfo']['expirationDate'].split("T")[0]
                    except KeyError:
                        expire_date = "Отсутствует"
                    if general_package_type == "BOX":
                        return JsonResponse({
                            "status": "box",
                            "body": {
                                "text_package_type": text_package_type,
                                "owner": owner,
                                "owner_inn": owner_inn,
                                "status_check": status_check,
                                "emission_date" : emission_date,
                                "introduced_date": introduced_date,
                                "button_close": "visible",
                                "audio": "error",
                                "collapse_button":
                                    f'<div class="row justify-content-center align-items-center"><div class="col text-start">'
                                    f'{text_package_type}</div><div class="col text-end">'
                                    f'<a class="btn btn-sm btn-success" data-bs-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample">'
                                    f'Единиц внутри {len(child)} ⇓'
                                    f'</a>'
                                    f'</div></div>',
                                "collapse_content": f'{"\r\n".join(child)}',
                                "collapse" :


                                    f'<div class="collapse" id="collapseExample">'
                                    f'<div class="card card-body overflow-auto" style="height: 12rem; overflow-y: auto;">'
                                    f'<pre><div id="collapse_content" class="text-primary fw-bold"></div></pre>'
                                    f''
                                    f'</div>'
                                    f'</div>'
                                    f'<hr class="hr hr-blurry" />'

                            }
                        })
                    if general_package_type == "ATK":
                        return JsonResponse({
                            "status": "box",
                            "body": {
                                "text_package_type": text_package_type,
                                "owner": owner,
                                "owner_inn": owner_inn,
                                "status_check": status_check,
                                "emission_date" : emission_date,
                                "introduced_date": introduced_date,
                                "button_close": "visible",
                                "audio": "error",
                                "collapse_button":
                                    f'<div class="row justify-content-center align-items-center"><div class="col text-start">'
                                    f'{text_package_type}</div><div class="col text-end">'
                                    f'<a class="btn btn-sm btn-success" data-bs-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample">'
                                    f'Единиц внутри {len(child)} ⇓'
                                    f'</a>'
                                    f'</div></div>',
                                "collapse_content": f'{"\r\n".join(child)}',
                                "collapse" :


                                    f'<div class="collapse" id="collapseExample">'
                                    f'<div class="card card-body overflow-auto" style="height: 12rem; overflow-y: auto;">'
                                    f'<pre><div id="collapse_content" class="text-primary fw-bold"></div></pre>'
                                    f''
                                    f'</div>'
                                    f'</div>'
                                    f'<hr class="hr hr-blurry" />'

                            }
                        })
                    if general_package_type == "GROUP":
                        return JsonResponse({
                            "status": "set",
                            "body": {
                                "type_producer": type_producer,
                                "spl_string": spl_string,
                                "product_name": product_name,
                                "product_tnved": "",
                                "product_gtin": product_gtin,
                                "producer_name_comp": producer_name_comp,
                                "product_group": product_group,
                                "product_group_id": product_group_id,
                                "owner": owner,
                                "validity_info": validity_info,
                                "leading_symbol_info": leading_symbol_info,
                                "owner_inn": owner_inn,
                                "status_check": status_check,
                                "produced_date": produced_date,
                                "expire_date": expire_date,
                                "audio": audio,
                                "button_close": button_close,
                                "check_code_input":
                                    f'<pre id="ki_code" style="white-space: pre-wrap;"><hr class="hr hr-blurry" />'
                                    f'<a href="#" id="check_code_input" onclick="CopyToClipboardCode('
                                    f"'ki_code'"
                                    f');" title="Копировать" style="text-decoration: none; color: black"><div id="code_content" class="text-primary fw-bold"></div></a>'
                                    f'<hr class="hr hr-blurry" /></pre>',
                                "code_content": check_code_input,
                                "status_ex": status_ex,
                                "state_status_ex": state_status_ex,
                                "text_package_type": text_package_type,
                                "collapse_content": f'{"\r\n".join(child)}',
                                "collapse_button":
                                    f'<div class="row justify-content-center align-items-center"><div class="col text-start">'
                                    f'{text_package_type}</div><div class="col text-end">'
                                    f'<a class="btn btn-sm btn-success" data-bs-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample">'
                                    f'Единиц внутри {len(child)} ⇓'
                                    f'</a>'
                                    f'</div></div>',
                                "collapse":

                                    f''

                                    f'<div class="collapse" id="collapseExample">'
                                    f'<div class="card card-body overflow-auto" style="height: 8rem; overflow-y: auto;">'
                                    f'<pre><div id="collapse_content" class="text-primary fw-bold"></div></pre>'
                                    f''
                                    f'</div>'
                                    f'</div>'
                                    f''

                            }
                        })
                    if general_package_type == "SET":
                        return JsonResponse({
                            "status": "set",
                            "body": {
                                "type_producer": type_producer,
                                "spl_string": spl_string,
                                "product_name": product_name,
                                "product_tnved": "",
                                "product_gtin": product_gtin,
                                "producer_name_comp": producer_name_comp,
                                "product_group": product_group,
                                "product_group_id": product_group_id,
                                "owner": owner,
                                "validity_info": validity_info,
                                "leading_symbol_info": leading_symbol_info,
                                "owner_inn": owner_inn,
                                "status_check": status_check,
                                "produced_date": produced_date,
                                "expire_date": expire_date,
                                "audio": audio,
                                "button_close": button_close,
                                "check_code_input":
                                    f'<pre id="ki_code" style="white-space: pre-wrap;"><hr class="hr hr-blurry" />'
                                    f'<a href="#" id="check_code_input" onclick="CopyToClipboardCode('
                                    f"'ki_code'"
                                    f');" title="Копировать" style="text-decoration: none; color: black"><div id="code_content" class="text-primary fw-bold"></div></a>'
                                    f'<hr class="hr hr-blurry" /></pre>',
                                "code_content": check_code_input,
                                "status_ex": status_ex,
                                "state_status_ex": state_status_ex,
                                "text_package_type": text_package_type,
                                "collapse_content": f'{"\r\n".join(child)}',
                                "collapse_button":
                                    f'<div class="row justify-content-center align-items-center"><div class="col text-start">'
                                    f'{text_package_type}</div><div class="col text-end">'
                                    f'<a class="btn btn-sm btn-success" data-bs-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample">'
                                    f'Единиц внутри {len(child)} ⇓'
                                    f'</a>'
                                    f'</div></div>',
                                "collapse":

                                    f''

                                    f'<div class="collapse" id="collapseExample">'
                                    f'<div class="card card-body overflow-auto" style="height: 8rem; overflow-y: auto;">'
                                    f'<pre><div id="collapse_content" class="text-primary fw-bold"></div></pre>'
                                    f''
                                    f'</div>'
                                    f'</div>'
                                    f''

                            }
                        })
                    if general_package_type == "UNIT":
                        return JsonResponse({
                            "status": "success",
                            "body": {
                                "type_producer": type_producer,
                                "spl_string": spl_string,
                                "product_name": product_name,
                                "product_tnved": "",
                                "product_gtin": product_gtin,
                                "producer_name_comp": producer_name_comp,
                                "product_group": product_group,
                                "product_group_id": product_group_id,
                                "owner": owner,
                                "validity_info": validity_info,
                                "leading_symbol_info": leading_symbol_info,
                                "owner_inn": owner_inn,
                                "status_check": status_check,
                                "produced_date": produced_date,
                                "expire_date": expire_date,
                                "audio": audio,
                                "button_close": button_close,
                                "check_code_input":
                                    f'<pre id="ki_code" style="white-space: pre-wrap;"><hr class="hr hr-blurry" />'
                                    f'<a href="#" id="check_code_input" onclick="CopyToClipboardCode('
                                    f"'ki_code'"
                                    f');" title="Копировать" style="text-decoration: none; color: black"><div id="code_content" class="text-primary fw-bold"></div></a>'
                                    f'<hr class="hr hr-blurry" /></pre>',
                                "code_content": check_code_input,
                                "status_ex": status_ex,
                                "state_status_ex": state_status_ex,
                                "text_package_type": text_package_type

                            }
                        })



                except Exception:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    frame = exc_traceback.tb_frame
                    lineno = exc_traceback.tb_lineno

                    # print(f"Исключение типа: {exc_type.__name__}")
                    # print(f"Сообщение: {exc_value}")
                    # print(f"Строка ошибки: {lineno}")
                    # print(f"Файл: {frame.f_code.co_filename}")
                    # print("КИ не найден KEY ERROR")
                    return JsonResponse({
                        "status": "error",
                        "errorMessage": f"{str(exc_type.__name__)} in {str(exc_value)} :line {lineno}<br>"
                                        f"{frame.f_code.co_filename}"
                    })


            else:
                return JsonResponse({"status": "error", "errorMessage": result_mess})

        # else:
        #     return JsonResponse({"status": "error", "errorMessage": ""})
    return render(request, "check_code.html", context={})

@cache_control(no_cache=True)
def read_code(request):
    if request.method == "POST":
        query = request.POST.get("query")
        if query:

            list_resp = get_nac_cat_all(query)

            return JsonResponse({
                "list":list_resp
            })


    return render(request, "read_code.html", context={

    })

@cache_control(no_cache=True)
def nc_find(request):
    if request.method == "POST":
        query = request.POST.get("query")
        if query:

            list_resp = get_nac_cat_all(query)

            return JsonResponse({
                "list":list_resp
            })


    return render(request, "nc_find.html", context={

    })

@cache_control(no_cache=True)
def main_menu(request):
    return render(request, "main.html", context={})

@cache_control(no_cache=True)
def error_server(request):
    return render(request, "500.html", context={})

@cache_control(no_cache=True)
def error_not_found(request):
    return render(request, "404.html", context={})
