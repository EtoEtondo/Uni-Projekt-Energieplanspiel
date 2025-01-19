import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import pandas as pd
import os
from datetime import datetime


@login_required
@require_http_methods(["POST"])
def handle_input(request):
    if request.user.is_superuser:
        return admin_config_file_upload(request)
    elif not request.user.is_staff:
        return group_input(request)


@login_required
def admin_config_file_upload(request):
    path = os.path.abspath("./energieplanspiel") + "/"
    files = request.FILES.getlist("file")
    for file in files:
        if file.name.lower() not in ["config.yml", "dat_energie-workshop.csv", "general_parameters.csv"]:
            continue
        with open(f"{path}{file.name}", "wb+") as overwrite_file:
            for chunk in file.chunks():
                overwrite_file.write(chunk)

    return JsonResponse(
        status=200, data={"Success": "Hochgeladenen Dateien wurden auf dem Server gespeichert/überschrieben!"}
    )


@login_required
def group_input(request):
    if request.user.has_submitted:
        return JsonResponse(status=405, data={"Error": "Methode nicht unterstützt!"})

    schedule = request.user.date
    instructor = schedule.instructor
    institution = instructor.institution

    path = (
        os.path.abspath(
            f"./energieplanspiel/{institution.name}/{instructor.username}/{datetime.strftime(schedule.timeslot, '%Y-%m-%d')}"
        )
        + "/data/"
    )
    os.makedirs(path, exist_ok=True)

    data = json.loads(request.body)

    number_of_windturbines = data["number_of_windturbines"]
    number_of_chps = data["number_of_chps"]
    number_of_boilers = data["number_of_boilers"]
    number_of_PV_pp = data["number_of_PV_pp"]
    number_of_heat_pumps = data["number_of_heat_pumps"]
    area_PV = data["area_PV"]
    area_solar_th = data["area_solar_th"]
    capacity_electr_storage = data["capacity_electr_storage"]
    capacity_thermal_storage = data["capacity_thermal_storage"]
    feature_building_retrofit = data["feature_building_retrofit"]
    percentage_of_bev = data["percentage_of_bev"]

    row_1 = [1, "number_of_windturbines", number_of_windturbines, "1", None, None, None, None, "wind_turb"]
    row_2 = [2, "number_of_chps", number_of_chps, "1", None, None, None, None, "chp"]
    row_3 = [3, "number_of_boilers", number_of_boilers, "1", None, None, None, None, "boiler"]
    row_4 = [4, "number_of_PV_pp", number_of_PV_pp, "1", None, None, None, None, "PV_pp"]
    row_5 = [5, "number_of_heat_pumps", number_of_heat_pumps, "1", None, None, None, None, "heat_pump"]
    row_6 = [6, "area_PV", area_PV, "ha", None, None, None, None, "PV"]
    row_7 = [7, "area_solar_th", area_solar_th, "ha", None, None, None, None, "solart_th"]
    row_8 = [
        8,
        "capacity_electr_storage",
        capacity_electr_storage,
        "daily_demand",
        None,
        None,
        None,
        "capacity",
        "storage_el",
    ]
    row_9 = [
        9,
        "capacity_thermal_storage",
        capacity_thermal_storage,
        "daily_demand",
        None,
        None,
        None,
        "capacity",
        "storage_th",
    ]
    row_10 = [
        10,
        "feature_building_retrofit",
        feature_building_retrofit,
        "1",
        None,
        None,
        None,
        None,
        "building_retrofit",
    ]
    row_11 = [11, "percentage_of_bev", percentage_of_bev, "1", None, None, None, "E_Car", None]

    csv_data = [
        row_1,
        row_2,
        row_3,
        row_4,
        row_5,
        row_6,
        row_7,
        row_8,
        row_9,
        row_10,
        row_11,
    ]

    df = pd.DataFrame(
        columns=["id", "var_name", "value", "unit", "reference", "Comment", "tag_1", "tag_2", "component"],
        data=csv_data,
    )
    filepath = path + f"parameters_Team_{request.user.username}.csv"
    df.to_csv(filepath, index=False)

    request.user.has_submitted = True
    request.user.save()

    return JsonResponse(status=200, data={"Success": "Eingaben wurden übermittelt!"})
