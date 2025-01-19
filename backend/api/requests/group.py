import json
from django.http import JsonResponse
from ..models import User, Schedule
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.utils import IntegrityError
from random import randint
import os
from datetime import datetime
from ..utility import *
from .. import globals


@login_required
def crud_group(request):
    if request.method == "POST":
        return create_a_group(request)
    elif request.method == "GET":
        return get_groups_by_schedule(request)
    elif request.method == "PUT":
        return edit_a_group(request)
    elif request.method == "DELETE":
        return delete_a_group(request)
    else:
        return JsonResponse(status=405, data={"Error": "Methode nicht unterstützt!"})


@login_required
@require_http_methods(["POST"])
def create_a_group(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)
    try:
        display_name = data["display_name"]
        username = f"{display_name}-{randint(0, 999_999):06}"
        password = data["password"]
        schedule = Schedule.objects.get(id=data["schedule"])
        if schedule == None:
            return JsonResponse(status=404, data={"Error": "Termin konnte nicht gefunden werden!"})
        if request.user.is_staff:
            if request.user.username != schedule.instructor.username:
                return JsonResponse(status=404, data={"Error": "Termin konnte nicht gefunden werden!"})
        if User.objects.filter(date=schedule, display_name=display_name).exists():
            return JsonResponse(status=409, data={"Error": "Gruppe existiert schon im Termin!"})

        new_group = User(
            username=username, display_name=display_name, date=schedule, enabled=schedule.instructor.enabled
        )
        new_group.set_password(password)
        if len(User.objects.filter(date=schedule).values()) >= 14:
            return JsonResponse(status=409, data={"Error": "Maximale Anzahl an Gruppen (14) wurde erreicht!"})
        try:
            new_group.save()
        except IntegrityError:
            return JsonResponse(
                status=409,
                data={"Error": "Bei der Vergabe des Login-Namens ist was schief gelaufen. Versuchen Sie es erneut!"},
            )
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})

    return JsonResponse(status=201, data={"Success": "Gruppe wurde erstellt!"})


@login_required
@require_http_methods(["DELETE"])
def delete_a_group(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)

    try:
        username = data["username"]
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})

    delete_group = User.objects.get(username=username)
    if delete_group == None:
        return JsonResponse(status=404, data={"Error": "Zu löschende Gruppe wurde nicht gefunden!"})

    # instructor darf nicht auf user eines anderen instructors zugreifen
    if request.user.is_staff:
        if request.user.username != delete_group.date.instructor.username:
            return JsonResponse(status=404, data={"Error": "Zu löschende Gruppe wurde nicht gefunden!"})

    delete_group.delete()

    return JsonResponse(status=200, data={"Success": "Gruppe wurde gelöscht!"})


@login_required
@require_http_methods(["PUT"])
def edit_a_group(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)
    edit_group = None
    try:
        username = data["username"]
        edit_group = User.objects.get(username=username)
        if edit_group == None:
            return JsonResponse(status=404, data={"Error": "Zu editierende Gruppe wurde nicht gefunden!"})
        if request.user.is_staff:
            if request.user.username != edit_group.date.instructor.username:
                return JsonResponse(status=404, data={"Error": "Zu editierende Gruppe wurde nicht gefunden!"})
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})
    if "password" in data and data["password"]:
        password = data["password"]
        edit_group.set_password(password)
    if "result_access" in data:
        result_access = data["result_access"]
        edit_group.result_access(result_access)
    edit_group.save()

    return JsonResponse(status=200, data={"Success": "Gruppe wurde editiert!"})


@login_required
@require_http_methods(["GET"])
def get_groups_by_schedule(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    try:
        schedule = Schedule.objects.get(id=request.GET.get("schedule", ""))
        instructor = schedule.instructor
        institution = instructor.institution
        if schedule == None:
            return JsonResponse(status=404, data={"Error": "Termin wurde nicht gefunden!"})
        if request.user.is_staff:
            if request.user.username != schedule.instructor.username:
                return JsonResponse(status=404, data={"Error": "Termin wurde nicht gefunden!"})

        date = datetime.strftime(schedule.timeslot, "%Y-%m-%d")
        path = os.path.abspath(f"./energieplanspiel/{institution.name}/{instructor.username}/{date}") + "/results/"

        calc_running = get_from_dict_by_path(globals.proc, [institution.name, instructor.username, date]) != {}
        if calc_running:
            calc_running = (
                get_from_dict_by_path(globals.proc, [institution.name, instructor.username, date]).poll() == None
            )
        results_exist = os.path.exists(path) and not calc_running

        # dabei soll beim getten der groups diese info mitgegeben werden
        return JsonResponse(
            status=200,
            data={
                u["id"]: {
                    "username": u["username"],
                    "display_name": u["display_name"],
                    "enabled": u["enabled"],
                    "has_submitted": u["has_submitted"],
                    "calc_running": calc_running,
                    "results_exist": results_exist,
                }
                for u in User.objects.filter(date=schedule).values()
            },
            safe=False,
        )
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})


@login_required
@require_http_methods(["PUT"])
def change_result_access_by_schedule(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)

    schedule = Schedule.objects.get(id=data["schedule"])

    User.objects.filter(date__in=Schedule.objects.filter(timeslot=schedule.timeslot)).update(
        result_access=data["result_access"]
    )

    return JsonResponse(
        status=200, data={"Success": "Die Gruppen des Termins können nun auf die Ergebnisse zugreifen!"}
    )
