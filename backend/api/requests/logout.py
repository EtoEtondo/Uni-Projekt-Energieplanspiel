from django.http import JsonResponse, HttpResponse
from django.contrib.auth import logout

from ..models import *


def backend_logout(request):
    if request.method == "DELETE":
        logout(request)
        return JsonResponse(status=200, data={"Logout": True, "redirect-to": f"/"})
    return JsonResponse(staus=405, data={"Logout": False, "Error": "Methode nicht unterstützt!"})
