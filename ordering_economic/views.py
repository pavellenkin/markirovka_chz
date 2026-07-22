from django.shortcuts import render
import json
from main.api.get_product_codes import list_codes

def ordering_economic(request):
    status, codes = list_codes()
    try:
        json_response = json.loads(codes)
        codes = json_response['result']['total']
    except json.decoder.JSONDecodeError:
        codes = None
    return render(request, "ordering_economic.html", context={
        "codes": codes
    })
