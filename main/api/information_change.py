from main.api.single_method_for_creating_documents import method_create_doc, check_status_document
import json
"""
Метод: POST
 /lk/documents/create
 POST <url стенда>/lk/documents/create?pg=beer
Authorization: Bearer <ТОКЕН>
Content-Type: application/json
{
   "document_format":"MANUAL",
   "product_document":"<Тело формируемого документа в base64>",
   "type":"CIS_INFORMATION_CHANGE",
   "signature":"<Откреплённая подпись для product_document в base64>"
}
тело документа 
{
   "participantInn":"string",
   "codes":[
      {
         "code":[
            "010463333333333321KnKNn4",
            "010463333333333321Kn5KNk"
         ],
         "productionDate":"string",
         "expirationDate":"string",
         "tnved":"string",
         "permitDocsOperation":0,
         "permitDocs":[
            {
               "permitDocNumber":"string",
               "permitDocDate":"01.01.2023",
               "permitDocType":2
            }
         ],
         "emissionType":2
      }
   ]
}

1. Тело документа закодировать в Base64
2. Подписать закодированное тело сертификатом.

Сначала нужно зашифровать тело документа в Base64, которое поместить в реквизит "product_document".
Затем нужно подписать зашифрованное тело документа в Base64 и поместить результат в реквизит "signature".

"""

def information_change(ki, production_date, expiration_date):
    type_doc = "CIS_INFORMATION_CHANGE"
    body_doc = {
        "participantInn": "7712035729",
        "codes": [
            {
                "code": [
                    ki[:31]
                ],
                "productionDate": production_date,
                "expirationDate": expiration_date,
            }
        ]
    }
    create_doc, message = method_create_doc(
        type_doc=type_doc,
        body_doc=body_doc,
        format_doc="MANUAL"
    )
    if create_doc is True:
        st, doc = check_status_document(message)
        if st is True:
            try:
                temp_doc = json.loads(doc)
                number_true_doc = temp_doc[0]['number']
            except:
                number_true_doc = "информация отсутствует"
            return True, number_true_doc
        else:
            return False, doc
    else:
        return False, message