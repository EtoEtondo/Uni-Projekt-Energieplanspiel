import yaml
import subprocess
import json
from django.http import JsonResponse
from ..models import User, Schedule
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import os
from datetime import datetime
from .. import globals
from threading import Thread
from queue import Queue, Empty
from ..utility import *


@login_required
@require_http_methods(["POST"])
def calculate_for_schedule(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    data = json.loads(request.body)

    schedule = Schedule.objects.get(id=data["schedule"])
    instructor = schedule.instructor
    institution = instructor.institution

    date = datetime.strftime(schedule.timeslot, "%Y-%m-%d")

    if not all([u["has_submitted"] for u in User.objects.filter(date=schedule).values()]):
        return JsonResponse(status=409, data={"Error": "Nicht jeder Teilnehmer hat abgegeben!"})

    # Ordnerstruktur
    dirs = f"{institution.name}/{instructor.username}/{date}"
    path = os.path.abspath(f"./energieplanspiel/{dirs}") + "/"

    energieplanspiel_script = os.path.abspath(f"./energieplanspiel/src") + "/"

    all_group_names = [u["username"] for u in User.objects.filter(date=schedule).values()]
    param_file_names = [f"parameters_Team_{groupname}.csv" for groupname in all_group_names]

    # erstellung der yml aus standard yml
    with open("./energieplanspiel/config.yml", encoding="utf-8") as default_config:
        yaml_config = yaml.safe_load(default_config)

        yaml_config["schedule"] = datetime.strftime(schedule.timeslot, "%Y-%m-%d")
        yaml_config["instructor"] = instructor.username
        yaml_config["institution"] = institution.name
        yaml_config["team_names"] = all_group_names
        yaml_config["design_parameters_file_name"] = param_file_names
        yaml_config["number_of_teams"] = len(all_group_names)

        with open(path + "config.yml", "w", encoding="utf-8") as config:
            yaml.safe_dump(yaml_config, config)

        # erstellen und setzen des prozesses/outputs
        if (
            date not in get_from_dict_by_path(globals.proc, [institution.name, instructor.username])
            or get_from_dict_by_path(globals.proc, [institution.name, instructor.username, date]).poll() != None
        ):
            set_in_dict_by_path(globals.output, [institution.name, instructor.username, date], [])
            set_in_dict_by_path(
                globals.proc,
                [institution.name, instructor.username, date],
                subprocess.Popen(
                    ["python3.7", "-W", "ignore", "main.py", f"{dirs}"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=energieplanspiel_script,
                    # im docker container auskommentieren, dann
                    # shell=True,
                ),
            )

        return JsonResponse(status=200, data={"Success": "Berechnung gestartet!"})


@login_required
@require_http_methods(["GET"])
def get_calculate_progress_for_schedule(request):
    if not request.user.is_superuser and not request.user.is_staff:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    # funktion für den thread, welcher in globals.output die stdout zeilen von globals.proc schreibt
    def read_output_lines(out, queue, terminate):
        line = out.readline()
        while line:
            queue.put(line)
            if terminate():
                return
            line = out.readline()
        return

    schedule = Schedule.objects.get(id=request.GET.get("schedule", ""))
    instructor = schedule.instructor
    institution = instructor.institution

    date = datetime.strftime(schedule.timeslot, "%Y-%m-%d")

    dirs = f"{institution.name}/{instructor.username}/{date}"
    path = os.path.abspath(f"./energieplanspiel/{dirs}") + "/"

    # anzahl von gruppen auslesen aus der config
    groups = 0
    with open(path + "config.yml", encoding="utf-8") as config:
        yaml_config = yaml.safe_load(config)
        groups = yaml_config["number_of_teams"]

    if date not in get_from_dict_by_path(globals.proc, [institution.name, instructor.username]):
        return JsonResponse(status=409, data={"Error": "Es läuft derzeit keine Berechnung!"})

    # hardcoded anzahl an Zeilen die für X gruppen ausgegeben werden für das main.py skript
    line_numbers = groups * 22 + 4
    proc = get_from_dict_by_path(globals.proc, [institution.name, instructor.username, date])
    output = get_from_dict_by_path(globals.output, [institution.name, instructor.username, date])

    # thread erstellen und nötigen variablen erstellen für den thread
    q = Queue()
    terminate_thread = False
    t = Thread(target=read_output_lines, args=(proc.stdout, q, lambda: terminate_thread))
    # thread starten, schließen und auf beendigung warten
    t.start()
    terminate_thread = True
    t.join()

    # Zeilen nach output schreiben, solange nicht leer ist
    try:
        while True:
            output.append(q.get_nowait())
    except Empty:
        pass

    # programm fortschritt
    progress = round(len(output) / line_numbers, 2)

    # entfernen von "unnötigen" keys und values
    if proc.poll() != None or progress == 1:
        try:
            remove_from_dict_by_path(globals.proc, [institution.name, instructor.username, date])
            remove_from_dict_by_path(globals.output, [institution.name, instructor.username, date])
            remove_empty_pair_from_dict_by_path(globals.proc, [institution.name, instructor.username])
            remove_empty_pair_from_dict_by_path(globals.output, [institution.name, instructor.username])
        except KeyError:
            pass
    return JsonResponse(status=200, data={"progress": progress})
