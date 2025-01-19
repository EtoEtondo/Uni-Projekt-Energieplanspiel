import json
from django.http import JsonResponse
from ..models import Institution
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


@login_required
def crud_institution(request):
    if request.method == "POST":
        return create_an_institution(request)
    elif request.method == "GET":
        return get_institutions(request)
    # elif request.method == "PUT":
    #     return edit_an_institution(request)
    elif request.method == "DELETE":
        return delete_an_institution(request)
    else:
        return JsonResponse(status=405, data={"Error": "Methode nicht unterstützt!"})


@login_required
@require_http_methods(["POST"])
def create_an_institution(request):
    if not request.user.is_superuser:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)
    try:
        name = data["name"]
        new_institution = Institution(name=name)
        new_institution.save()
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})

    return JsonResponse(status=201, data={"Success": "Institution wurde erstellt!"})


@login_required
@require_http_methods(["DELETE"])
def delete_an_institution(request):
    if not request.user.is_superuser:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)

    try:
        # id der institutions
        institution = data["institution"]
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})

    delete_institution = Institution.objects.get(id=institution)
    if delete_institution == None:
        return JsonResponse(status=404, data={"Error": "Zu löschende Institution wurde nicht gefunden!"})

    delete_institution.delete()

    return JsonResponse(status=200, data={"Success": "Institution wurde gelöscht!"})


@login_required
@require_http_methods(["PUT"])
def edit_an_institution(request):
    if not request.user.is_superuser:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)
    edit_institution = None
    try:
        edit_institution = Institution.objects.get(id=data["institution"])
        if edit_institution == None:
            return JsonResponse(status=404, data={"Error": "Zu editierende Institution wurde nicht gefunden!"})
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})
    if "name" in data:
        name = data["name"]
        edit_institution.name = name
    edit_institution.save()

    return JsonResponse(status=200, data={"Success": "Institution wurde editiert!"})


@login_required
@require_http_methods(["GET"])
def get_institutions(request):
    if not request.user.is_superuser:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    return JsonResponse(
        status=200, data={i["id"]: {"name": i["name"]} for i in Institution.objects.all().values()}, safe=False
    )
