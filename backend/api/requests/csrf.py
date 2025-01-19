from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def backend_csrf(request):
    return JsonResponse(status=200, data={"detail": "CSRF cookie set"})
