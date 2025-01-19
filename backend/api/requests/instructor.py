import json
from django.http import JsonResponse
from ..models import User, Institution, Schedule
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.utils import IntegrityError
from random import randint


@login_required
def crud_instructor(request):
    if request.method == "POST":
        return create_an_instructor(request)
    elif request.method == "GET":
        return get_instructors_by_institution(request)
    elif request.method == "PUT":
        return edit_an_instructor(request)
    elif request.method == "DELETE":
        return delete_an_instructor(request)
    else:
        return JsonResponse(status=405, data={"Error": "Methode nicht unterstützt!"})


@login_required
@require_http_methods(["POST"])
def create_an_instructor(request):
    if not request.user.is_superuser:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)
    try:
        display_name = data["display_name"]
        username = f"{display_name}-{randint(0, 999_999):06}"
        password = data["password"]
        institution = Institution.objects.get(id=data["institution"])
        if institution == None:
            return JsonResponse(status=404, data={"Error": "Institution konnte nicht gefunden werden!"})

        new_instructor = User(username=username, display_name=display_name, institution=institution, is_staff=True)
        new_instructor.set_password(password)
        try:
            new_instructor.save()
        except IntegrityError:
            return JsonResponse(
                status=409,
                data={"Error": "Bei der Vergabe des Login-Namens ist was schief gelaufen. Versuchen Sie es erneut!"},
            )
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})

    return JsonResponse(status=201, data={"Success": "Instruktor wurde erstellt!"})


@login_required
@require_http_methods(["DELETE"])
def delete_an_instructor(request):
    if not request.user.is_superuser:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)

    try:
        username = data["username"]
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})

    delete_instructor = User.objects.get(username=username)
    if delete_instructor == None:
        return JsonResponse(status=404, data={"Error": "Zu löschender Instruktor wurde nicht gefunden!"})

    delete_instructor.delete()

    return JsonResponse(status=200, data={"Success": "Instruktor wurde gelöscht!"})


@login_required
@require_http_methods(["PUT"])
def edit_an_instructor(request):
    if not request.user.is_superuser:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)
    edit_instructor = None
    try:
        username = data["username"]
        edit_instructor = User.objects.get(username=username)
        if edit_instructor == None:
            return JsonResponse(status=404, data={"Error": "Zu editierender Instruktor wurde nicht gefunden!"})
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})
    if "password" in data and data["password"]:
        password = data["password"]
        edit_instructor.set_password(password)
    if "enabled" in data:
        edit_instructor.enabled = data["enabled"]
        User.objects.filter(date__in=Schedule.objects.filter(instructor=edit_instructor.id)).update(
            enabled=edit_instructor.enabled
        )

    edit_instructor.save()

    return JsonResponse(status=200, data={"Success": "Instruktor wurde editiert!"})


@login_required
@require_http_methods(["GET"])
def get_instructors_by_institution(request):
    if not request.user.is_superuser:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    try:
        institution = Institution.objects.get(id=request.GET.get("institution", ""))
        if institution == None:
            return JsonResponse(status=404, data={"Error": "Institution wurde nicht gefunden!"})

        return JsonResponse(
            status=200,
            data={
                u["id"]: {"username": u["username"], "display_name": u["display_name"], "enabled": u["enabled"]}
                for u in User.objects.filter(institution=institution).values()
            },
            safe=False,
        )
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})
