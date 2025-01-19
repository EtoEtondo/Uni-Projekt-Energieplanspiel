import json
from django.http import JsonResponse
from ..models import User, Schedule
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from datetime import datetime


@login_required
def crud_schedule(request):
    if request.method == "POST":
        return create_a_schedule(request)
    elif request.method == "GET":
        return get_schedules_by_instructor(request)
    # elif request.method == "PUT":
    #     return edit_a_schedule(request)
    elif request.method == "DELETE":
        return delete_a_schedule(request)
    else:
        return JsonResponse(status=405, data={"Error": "Methode nicht unterstützt!"})


@login_required
@require_http_methods(["POST"])
def create_a_schedule(request):
    if not request.user.is_superuser:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)
    try:
        timeslot = datetime.strptime(data["timeslot"], "%Y-%m-%d")
        instructor = User.objects.get(username=data["username"])
        if instructor == None:
            return JsonResponse(status=404, data={"Error": "Instructor konnte nicht gefunden werden!"})
        if Schedule.objects.filter(instructor=instructor, timeslot=timeslot).exists():
            return JsonResponse(status=409, data={"Error": "Termin existiert schon für den Instruktor!"})

        new_schedule = Schedule(timeslot=timeslot, instructor=instructor)
        new_schedule.save()
    except (KeyError, ValueError):
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})

    return JsonResponse(status=201, data={"Success": "Termin wurde erstellt!"})


@login_required
@require_http_methods(["DELETE"])
def delete_a_schedule(request):
    if not request.user.is_superuser:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)

    try:
        # id des schedules
        schedule = data["schedule"]
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})

    delete_schedule = Schedule.objects.get(id=schedule)
    if delete_schedule == None:
        return JsonResponse(status=404, data={"Error": "Zu löschender Termin wurde nicht gefunden!"})

    delete_schedule.delete()

    return JsonResponse(status=200, data={"Success": "Termin wurde gelöscht!"})


@login_required
@require_http_methods(["PUT"])
def edit_a_schedule(request):
    if not request.user.is_superuser:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)
    edit_schedule = None
    try:
        edit_schedule = Schedule.objects.get(id=data["schedule"])
        if edit_schedule == None:
            return JsonResponse(status=404, data={"Error": "Zu editierender Termin wurde nicht gefunden!"})
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})
    if "timeslot" in data:
        timeslot = datetime.strptime(data["timeslot"], "%d.%m.%Y")
        if Schedule.objects.filter(timeslot=timeslot, instructor=edit_schedule.instructor).exists():
            return JsonResponse(status=409, data={"Error": "Termin existiert schon für den Instruktor!"})
        edit_schedule.timeslot = timeslot
    edit_schedule.save()

    return JsonResponse(status=200, data={"Success": "Termin wurde editiert!"})


@login_required
@require_http_methods(["GET"])
def get_schedules_by_instructor(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    try:
        instructor = User.objects.get(username=request.GET.get("username", ""))
        if instructor == None or not instructor.is_staff:
            return JsonResponse(status=404, data={"Error": "Instruktor wurde nicht gefunden!"})
        if request.user.is_staff:
            if request.user.username != instructor.username:
                return JsonResponse(status=404, data={"Error": "Instruktor wurde nicht gefunden!"})
        return JsonResponse(
            status=200,
            data={
                s["id"]: {"timeslot": s["timeslot"]} for s in Schedule.objects.filter(instructor=instructor.id).values()
            },
            safe=False,
        )
    except KeyError:
        return JsonResponse(status=400, data={"Error": "Einige essenzielle Informationen fehlen in der Anfrage!"})
