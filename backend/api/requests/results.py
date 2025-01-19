import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from ..models import Schedule
from plotly.io import to_json
import plotly.graph_objects as go
import pandas as pd
import os
from datetime import datetime
from .. import globals
from ..utility import *


@login_required
@require_http_methods(["GET"])
def get_results_for_schedule(request):
    if not request.user.is_superuser and not request.user.is_staff and not request.user.result_access:
        return JsonResponse(status=403, data={"Error": "Unzureichende Rolle!"})

    schedule = None
    if not request.user.is_superuser and not request.user.is_staff:
        schedule = request.user.date
    else:
        schedule = Schedule.objects.get(id=request.GET.get("schedule", ""))
    instructor = schedule.instructor
    institution = instructor.institution

    date = datetime.strftime(schedule.timeslot, "%Y-%m-%d")

    path = os.path.abspath(
        f"./energieplanspiel/{institution.name}/{instructor.username}/{date}") + "/results/"
    # während der berechnung oder wenn noch kein Ergebnis Ordner existiert soll returned werden
    if get_from_dict_by_path(globals.proc, [institution.name, instructor.username, date]) != {} or not os.path.exists(
        path
    ):
        return JsonResponse(status=409, data={"Error": "Es existieren noch keine Ergebnisse!"})

    plot_data = {}
    for team in os.listdir(f"{path}teams"):
        if team not in plot_data:
            plot_data[team] = []
            for team_result in sorted(os.listdir(f"{path}teams/{team}")):
                if team_result.rsplit(".", maxsplit=1)[1] != "json":
                    continue
                with open(f"{path}teams/{team}/{team_result}", encoding="utf-8") as team_data:
                    plot_data[team].append(json.loads(team_data.read()))

    with open(f"{path}summary/results_summary.json", encoding="utf-8") as results_div:
        plot_data["summary"] = json.loads(results_div.read())
        plot_data["summary"]["layout"]["annotations"] = [plot_data["summary"]["layout"]["annotations"][0]]

    results_df = pd.read_csv(f"{path}summary/results_table.csv")
    results_df = results_df.round(2)

    results_df.rename(columns={"Unnamed: 0": "Parameter"}, inplace=True)
    col_count = len(results_df.columns)
    n = 4
    plotly_table = go.Figure(data=[go.Table(
        header=dict(
            values=results_df.columns,
            fill_color='paleturquoise',
            align='left'
        ),
        cells=dict(
            values=[results_df[c] for c in results_df.columns],
            fill_color='lavender',
            align='left'
        ),
    )])
    steps=[
        {
            "args": [{
                "columnorder": [[0] + [k+j for j in range(1, n)]],
                "header.values": [[results_df.columns[0]] + list(results_df.columns[k+1:k+n])],
                "cells.values": [[results_df.iloc[:, 0]] + [results_df[col] for col in results_df.columns[k+1:k+n]]]
            }],
            "method": "restyle",
            "label": f"Abschnitt {k+1}",
            "execute": True,
        } for k in range((col_count-n+1))
    ]
    init_step = {
            "args": [{
                "columnorder": [[j for j in range(0, col_count)]],
                "header.values": [list(results_df.columns)],
                "cells.values": [[results_df[col] for col in results_df.columns]]
            }],
            "method": "restyle",
            "label": f"Übersicht",
            "execute": True,
        }
    steps.insert(0, init_step)

    plotly_table.update_layout(
        sliders=[
            dict(
                active=0,
                minorticklen=0,
                steps=steps
            )
        ],
        transition=dict(
            duration=500,
            easing="linear" 
        )
    )

    plot_data["table"] = json.loads(
        to_json(
            plotly_table,
        )
    )

    return JsonResponse(status=200, data=plot_data)
