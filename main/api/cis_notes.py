from main.api.single_method_for_creating_documents import method_create_doc, check_status_document
from datetime import datetime
import requests

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

def cis_notes(code):
    date_now = datetime.now()
    type_doc = "CIS_NOTICE"
    body_doc = {
        "participantInn": "7712035729",
        "actionDate": str(date_now.date()),
        "action": "LOST_INVENTORY",
        "codes": [
            {
                "code": code
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
        print(st, doc)
    return create_doc, message