from django.shortcuts import render
from main.api.ordering_codes import order

def remark(request):
    # order("", "")
    return render(request, "remark.html", context={})
