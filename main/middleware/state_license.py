from django.shortcuts import redirect, render


def key():
    return "JunI9vrtc7pq!"

def state_license(get_response):
    def middleware(request):
        response = get_response(request)
        if "JunI9vrtc7pq!" == key():
            print("... license verification is successful ...")
            return response
        else:
            print("license expired")
            return render(request, '404.html', status=404)

    return middleware