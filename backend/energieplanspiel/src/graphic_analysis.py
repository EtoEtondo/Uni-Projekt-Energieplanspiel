###############################################################################
# imports
###############################################################################

import oemof.solph as solph
import oemof.tools.economics as eco

import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import plotly
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.tools as tls
import yaml
import numpy as np

from pathlib import Path
import logging

import oemof_visio as oev
from datetime import datetime, date


def pie_charts(config_path, team_number):
    with open(config_path, encoding="utf-8") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.CLoader)

    logging.info("Make Pie Charts")

    file_name = "teamdata_" + cfg["team_names"][team_number] + ".csv"
    apath = f"../{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}/results/data/analysis/"
    os.makedirs(apath, exist_ok=True)
    datafile = apath + file_name
    df = pd.read_csv(datafile)

    # 1.Pie Chart: Shares of electricity inputs
    fig, axs = plt.subplots(2, 3, figsize=(17, 8))
    plt.subplots_adjust(left=0.0, right=0.88, top=0.874, bottom=0.0, wspace=0.226, hspace=0.086)
    share_of_pv = float(df["el_from_pv"]) / float(df["total_el_demand"])
    share_of_wind = float(df["el_from_wind"]) / float(df["total_el_demand"])
    share_of_chp = float(df["el_from_chp"]) / float(df["total_el_demand"])
    share_of_shortage_el = float(df["el_from_grid"]) / float(df["total_el_demand"])

    rows = 2
    cols = 3
    plotly_fig = make_subplots(
        rows,
        cols,
        specs=[
            [{"type": "pie"}, {"type": "pie"}, {"type": "pie"}],
            [{"type": "pie"}, {"type": "pie"}, {"type": "pie"}],
        ],
    )

    PieChart1 = {
        "labels": ["PV", "WEA", "BHKW", "Stromzukauf"],
        "sizes": [share_of_pv, share_of_wind, share_of_chp, share_of_shortage_el],
        #'colors':['#f6ff00','#ffd500','#02a2f7','#69009e','#ff8585']}
        "colors": ["#f6ff00", "#02a2f7", "#69009e", "#ff8585"],
    }
    axs[0, 0].pie(
        PieChart1["sizes"],
        autopct="%1.1f%%",
        colors=PieChart1["colors"],
        shadow=False,
        startangle=0,
        labeldistance=1.3,
        radius=4,
        normalize=True,
        counterclock=False,
    )
    axs[0, 0].legend(PieChart1["labels"], loc="upper left", bbox_to_anchor=(0.87, 0, 0.5, 1), fontsize=9)
    axs[0, 0].axis("equal")
    axs[0, 0].set_title(
        "Aufteilung der Stromproduktion\n 100% ≙ {:.0f} kWh pro Person & Jahr".format(float(df["total_el_demand"]))
    )
    plotly_fig.add_trace(
        go.Pie(
            title="Aufteilung der Stromproduktion<br>100% ≙ {:.0f} kWh pro Person & Jahr".format(
                float(df["total_el_demand"])
            ),
            title_font_size=18,
            values=PieChart1["sizes"],
            labels=PieChart1["labels"],
            marker_colors=PieChart1["colors"],
            legendgroup=1,
            legendgrouptitle_text="Diagramm 1",
            name="Diagramm 1",
            hovertemplate="%{label}: <br>%{percent}",
        ),
        row=1,
        col=1,
    )

    # 2.Pie Chart: Shares of electricity outputs
    share_of_demand_el = float(df["el_demand"]) / float(df["total_el_demand"])
    share_of_excess_el = float(df["el_excess"]) / float(df["total_el_demand"])
    share_of_el_to_hp = float(df["el_hp_demand"]) / float(df["total_el_demand"])
    share_of_el_to_bev = float(df["el_bev_demand"]) / float(df["total_el_demand"])
    if cfg["enable_mobility"]:
        PieChart2 = {
            "labels": ["Strom-Nutzung", "Stromüberschuss", "Wärmepumpe", "Ladung der E-PKW"],
            "sizes": [share_of_demand_el, share_of_excess_el, share_of_el_to_hp, share_of_el_to_bev],
            "colors": ["#ff0000", "#00872d", "#6b6b6b", "#00ff91"],
        }
    else:
        PieChart2 = {
            "labels": ["Strom-Nutzung", "Stromüberschuss", "Wärmepumpe"],
            "sizes": [share_of_demand_el, share_of_excess_el, share_of_el_to_hp],
            "colors": ["#ff0000", "#00872d", "#6b6b6b"],
        }
    axs[1, 0].pie(
        PieChart2["sizes"],
        autopct="%1.1f%%",
        shadow=False,
        startangle=90,
        labeldistance=1.3,
        radius=3,
        colors=PieChart2["colors"],
        normalize=True,
    )
    axs[1, 0].legend(PieChart2["labels"], loc="upper left", bbox_to_anchor=(0.87, 0, 0.5, 1), fontsize=9)
    axs[1, 0].axis("equal")
    axs[1, 0].set_title(
        "Aufteilung des Strombedarfs\n 100% ≙ {:.0f} kWh pro Person & Jahr".format(float(df["total_el_demand"]))
    )
    plotly_fig.add_trace(
        go.Pie(
            title="Aufteilung des Strombedarfs<br>100% ≙ {:.0f} kWh pro Person & Jahr".format(
                float(df["total_el_demand"])
            ),
            title_font_size=18,
            values=PieChart2["sizes"],
            labels=PieChart2["labels"],
            marker_colors=PieChart2["colors"],
            legendgroup=2,
            legendgrouptitle_text="Diagramm 2",
            name="Diagramm 2",
            hovertemplate="%{label}: <br>%{percent}",
        ),
        row=1,
        col=2,
    )

    # 3.Pie Chart: Shares of heat inputs
    share_of_solarthermal = float(df["heat_from_solar"]) / float(df["heat_demand"])
    share_of_chp = float(df["heat_from_chp"]) / float(df["heat_demand"])
    share_of_boiler = float(df["heat_from_boiler"]) / float(df["heat_demand"])
    share_of_shortage_heat = float(df["heat_shortage"]) / float(df["heat_demand"])
    share_of_hp = float(df["heat_from_hp"]) / float(df["heat_demand"])
    PieChart3 = {
        "labels": ["Solarthermie", "BHKW", "Heizkessel", "Wärmezukauf", "Wärmepumpe"],
        "sizes": [share_of_solarthermal, share_of_chp, share_of_boiler, share_of_shortage_heat, share_of_hp],
        "colors": ["#ffde32", "#69009e", "#e095fc", "#78000c", "#6b6b6b"],
    }
    axs[0, 1].pie(
        PieChart3["sizes"],
        autopct="%1.1f%%",
        shadow=False,
        startangle=90,
        labeldistance=1.3,
        radius=3,
        colors=PieChart3["colors"],
        normalize=True,
    )
    axs[0, 1].legend(PieChart3["labels"], loc="upper left", bbox_to_anchor=(0.87, 0, 0.5, 1), fontsize=9)
    axs[0, 1].axis("equal")
    axs[0, 1].set_title(
        "Aufteilung der Wärmeproduktion\n 100% ≙ {:.0f} kWh pro Person & Jahr".format(float(df["heat_demand"]))
    )
    plotly_fig.add_trace(
        go.Pie(
            title="Aufteilung der Wärmeproduktion<br>100% ≙ {:.0f} kWh pro Person & Jahr".format(
                float(df["heat_demand"])
            ),
            title_font_size=18,
            values=PieChart3["sizes"],
            labels=PieChart3["labels"],
            marker_colors=PieChart3["colors"],
            legendgroup=3,
            legendgrouptitle_text="Diagramm 3",
            name="Diagramm 3",
            hovertemplate="%{label}: <br>%{percent}",
        ),
        row=1,
        col=3,
    )

    # 4.Pie Chart: Shares of CO2-emissions
    if float(df["emissions"]) > 0:
        share_of_em_el_import = float(df["em_el_shortage"]) / (float(df["emissions"]) * 1000)
        share_of_em_heat_import = float(df["em_heat_shortage"]) / (float(df["emissions"]) * 1000)
        share_of_em_chp = float(df["em_chp"]) / (float(df["emissions"]) * 1000)
        share_of_em_boiler = float(df["em_boiler"]) / (float(df["emissions"]) * 1000)
        share_of_em_car = float(df["em_car"]) / (float(df["emissions"]) * 1000)
        if cfg["enable_mobility"]:
            PieChart4 = {
                "labels": ["Stromzukauf", "Wärmezukauf", "BHKW", "Heizkessel", "PKW"],
                "sizes": [
                    share_of_em_el_import,
                    share_of_em_heat_import,
                    share_of_em_chp,
                    share_of_em_boiler,
                    share_of_em_car,
                ],
                "colors": ["#ff8585", "#78000c", "#69009e", "#e095fc", "#ff0000"],
            }
        else:
            PieChart4 = {
                "labels": ["Stromzukauf", "Wärmezukauf", "BHKW", "Heizkessel"],
                "sizes": [share_of_em_el_import, share_of_em_heat_import, share_of_em_chp, share_of_em_boiler],
                "colors": ["#ff8585", "#78000c", "#69009e", "#e095fc"],
            }
        axs[1, 1].pie(
            PieChart4["sizes"],
            autopct="%1.1f%%",
            shadow=False,
            startangle=90,
            labeldistance=1.3,
            radius=3,
            colors=PieChart4["colors"],
            normalize=True,
        )
        axs[1, 1].legend(PieChart4["labels"], loc="upper left", bbox_to_anchor=(0.87, 0, 0.5, 1), fontsize=9)
        axs[1, 1].axis("equal")
        axs[1, 1].set_title(
            "Aufteilung der CO2-Emissionen\n 100% ≙ {:.1f} kg pro Person & Jahr".format(float(df["emissions"]))
        )
        plotly_fig.add_trace(
            go.Pie(
                title="Aufteilung der CO2-Emissionen<br>100% ≙ {:.1f} kg pro Person & Jahr".format(
                    float(df["emissions"])
                ),
                title_font_size=18,
                values=PieChart4["sizes"],
                labels=PieChart4["labels"],
                marker_colors=PieChart4["colors"],
                legendgroup=4,
                legendgrouptitle_text="Diagramm 4",
                name="Diagramm 4",
                hovertemplate="%{label}: <br>%{percent}",
            ),
            row=2,
            col=1,
        )
    else:
        PieChart4 = {"labels": ["None"], "sizes": [1.0], "colors": ["#ff8585"]}
        axs[1, 1].pie(
            PieChart4["sizes"],
            autopct="%1.1f%%",
            shadow=False,
            startangle=90,
            labeldistance=1.3,
            radius=0.01,
            colors=PieChart4["colors"],
            normalize=True,
        )
        axs[1, 1].set_title("Keine CO2-Emissionen")
        plotly_fig.add_trace(
            go.Pie(
                title="Keine CO2-Emissionen",
                title_font_size=18,
                values=PieChart4["sizes"],
                labels=PieChart4["labels"],
                marker_colors=PieChart4["colors"],
                legendgroup=4,
                legendgrouptitle_text="Diagramm 4",
                name="Diagramm 4",
                hovertemplate="%{label}: <br>%{percent}",
            ),
            row=2,
            col=1,
        )

    # 5.Pie Chart: Shares of capex
    # total_annuity1= total_annuity + total_annuity_subsidization #100% Anpassung an Subventionierung

    if float(df["total_annuity"]) > 0:
        share_of_an_chp = 100 * float(df["annuity_chp"]) / float(df["total_annuity"])
        share_of_an_boiler = 100 * float(df["annuity_boiler"]) / float(df["total_annuity"])
        share_of_an_wind = 100 * float(df["annuity_wind"]) / float(df["total_annuity"])
        share_of_an_hp = 100 * float(df["annuity_hp"]) / float(df["total_annuity"])
        share_of_an_storage_el = 100 * float(df["annuity_storage_el"]) / float(df["total_annuity"])
        share_of_an_storage_th = 100 * float(df["annuity_storage_th"]) / float(df["total_annuity"])
        share_of_an_pv = 100 * float(df["annuity_pv"]) / float(df["total_annuity"])
        share_of_an_solarthermal = 100 * float(df["annuity_solar_th"]) / float(df["total_annuity"])
        share_of_an_pv_pp = 100 * float(df["annuity_PV_pp"]) / float(df["total_annuity"])
        share_of_an_building_retrofit = 100 * float(df["annuity_building_retrofit"]) / float(df["total_annuity"])
        share_of_an_car = 100 * float(df["annuity_car"]) / float(df["total_annuity"])
        share_of_an_bev = 100 * float(df["annuity_bev"]) / float(df["total_annuity"])
        # share_of_an_subsidization=      total_annuity_subsidization/ total_annuity1*100
        if cfg["enable_mobility"]:
            if cfg["enable_building_retrofit"]:
                PieChart5 = {
                    "labels": [
                        "BHKW",
                        "Heizkessel",
                        "WEA",
                        "Wärmepumpe",
                        "Stromspeicher",
                        "Wärmespeicher",
                        "Dachflächen-PV",
                        "Solarthermie",
                        "Freiflächen-PV",
                        "Gebäudesanierung",
                        "PKW",
                        "E-PKW",
                    ],
                    "sizes": [
                        share_of_an_chp,
                        share_of_an_boiler,
                        share_of_an_wind,
                        share_of_an_hp,
                        share_of_an_storage_el,
                        share_of_an_storage_th,
                        share_of_an_pv,
                        share_of_an_solarthermal,
                        share_of_an_pv_pp,
                        share_of_an_building_retrofit,
                        share_of_an_car,
                        share_of_an_bev,
                    ],
                    "colors": [
                        "#69009e",
                        "#e095fc",
                        "#02a2f7",
                        "#6b6b6b",
                        "#1500ff",
                        "#2020ab",
                        "#f6ff00",
                        "#fa7e02",
                        "#ffd500",
                        "#d9534f",
                        "#ff0000",
                        "#4af9ff",
                    ],
                }
                PieChart5["labels"] = [
                    "{}: {:1.1f} %".format(l, s) for l, s in zip(PieChart5["labels"], PieChart5["sizes"])
                ]
            else:
                PieChart5 = {
                    "labels": [
                        "BHKW",
                        "Heizkessel",
                        "WEA",
                        "Wärmepumpe",
                        "Stromspeicher",
                        "Wärmespeicher",
                        "Dachflächen-PV",
                        "Solarthermie",
                        "Freiflächen-PV",
                        "PKW",
                        "E-PKW",
                    ],
                    "sizes": [
                        share_of_an_chp,
                        share_of_an_boiler,
                        share_of_an_wind,
                        share_of_an_hp,
                        share_of_an_storage_el,
                        share_of_an_storage_th,
                        share_of_an_pv,
                        share_of_an_solarthermal,
                        share_of_an_pv_pp,
                        share_of_an_car,
                        share_of_an_bev,
                    ],
                    "colors": [
                        "#69009e",
                        "#e095fc",
                        "#02a2f7",
                        "#6b6b6b",
                        "#1500ff",
                        "#2020ab",
                        "#f6ff00",
                        "#fa7e02",
                        "#ffd500",
                        "#ff0000",
                        "#4af9ff",
                    ],
                }
        else:
            if cfg["enable_building_retrofit"]:
                PieChart5 = {
                    "labels": [
                        "BHKW",
                        "Heizkessel",
                        "WEA",
                        "Wärmepumpe",
                        "Stromspeicher",
                        "Wärmespeicher",
                        "Dachflächen-PV",
                        "Solarthermie",
                        "Freiflächen-PV",
                        "Gebäudesanierung",
                    ],
                    "sizes": [
                        share_of_an_chp,
                        share_of_an_boiler,
                        share_of_an_wind,
                        share_of_an_hp,
                        share_of_an_storage_el,
                        share_of_an_storage_th,
                        share_of_an_pv,
                        share_of_an_solarthermal,
                        share_of_an_pv_pp,
                        share_of_an_building_retrofit,
                    ],
                    "colors": [
                        "#69009e",
                        "#e095fc",
                        "#02a2f7",
                        "#6b6b6b",
                        "#1500ff",
                        "#2020ab",
                        "#f6ff00",
                        "#fa7e02",
                        "#ffd500",
                        "#d9534f",
                    ],
                }
            # PieChart5['labels']=['%s: %1.1f %%' % (l, s) for l, s in zip(PieChart5['labels'], PieChart5['sizes'])]
            else:
                PieChart5 = {
                    "labels": [
                        "BHKW",
                        "Heizkessel",
                        "WEA",
                        "Wärmepumpe",
                        "Stromspeicher",
                        "Wärmespeicher",
                        "Dachflächen-PV",
                        "Solarthermie",
                        "Freiflächen-PV",
                    ],
                    "sizes": [
                        share_of_an_chp,
                        share_of_an_boiler,
                        share_of_an_wind,
                        share_of_an_hp,
                        share_of_an_storage_el,
                        share_of_an_storage_th,
                        share_of_an_pv,
                        share_of_an_solarthermal,
                        share_of_an_pv_pp,
                    ],
                    "colors": [
                        "#69009e",
                        "#e095fc",
                        "#02a2f7",
                        "#6b6b6b",
                        "#1500ff",
                        "#2020ab",
                        "#f6ff00",
                        "#fa7e02",
                        "#ffd500",
                    ],
                }
            # PieChart5['labels']=['%s: %1.1f %%' % (l, s) for l, s in zip(PieChart5['labels'], PieChart5['sizes'])]

        axs[0, 2].pie(
            PieChart5["sizes"],
            shadow=False,
            startangle=90,
            labeldistance=1.3,
            radius=3,
            colors=PieChart5["colors"],
            normalize=True,
        )
        axs[0, 2].legend(PieChart5["labels"], loc="upper left", bbox_to_anchor=(0.87, 0, 0.5, 1), fontsize=9)
        axs[0, 2].axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
        axs[0, 2].set_title(
            "Aufteilung der anteiligen Investitionskosten\n 100% ≙ {:.0f} € pro Person & Jahr".format(
                float(df["total_annuity"])
            )
        )
        plotly_fig.add_trace(
            go.Pie(
                title="Aufteilung der anteiligen Investitionskosten<br>100% ≙ {:.0f} € pro Person & Jahr".format(
                    float(df["total_annuity"])
                ),
                title_font_size=18,
                values=PieChart5["sizes"],
                labels=[l.split(":", maxsplit=1)[0] for l in PieChart5["labels"]],
                marker_colors=PieChart5["colors"],
                legendgroup=5,
                legendgrouptitle_text="Diagramm 5",
                name="Diagramm 5",
                hovertemplate="%{label}: <br>%{percent}",
            ),
            row=2,
            col=2,
        )
    else:
        PieChart5 = {"labels": ["None"], "sizes": [1.0], "colors": ["#ff8585"]}
        axs[0, 2].pie(
            PieChart5["sizes"],
            autopct="%1.1f%%",
            shadow=False,
            startangle=90,
            labeldistance=1.3,
            radius=0.01,
            colors=PieChart5["colors"],
            normalize=True,
        )
        axs[0, 2].set_title("Keine Investitionskosten")
        plotly_fig.add_trace(
            go.Pie(
                title="Keine Investitionskosten",
                title_font_size=18,
                values=PieChart5["sizes"],
                labels=[l.split(":", maxsplit=1)[0] for l in PieChart5["labels"]],
                marker_colors=PieChart5["colors"],
                legendgroup=5,
                legendgrouptitle_text="Diagramm 5",
                name="Diagramm 5",
                hovertemplate="%{label}: <br>%{percent}",
            ),
            row=2,
            col=2,
        )

    # 6.Pie Chart: Shares of variable costs
    if float(df["var_costs_total"]) > 0:
        share_of_vc_gas = float(df["var_costs_gas"]) / (float(df["var_costs_total"]) * 1e6)
        share_of_vc_el_import = float(df["var_costs_el"]) / (float(df["var_costs_total"]) * 1e6)
        share_of_vc_heat_import = float(df["var_costs_heat"]) / (float(df["var_costs_total"]) * 1e6)
        share_of_vc_fuel = float(df["var_costs_fuel"]) / (float(df["var_costs_total"]) * 1e6)
        if cfg["enable_mobility"]:
            PieChart6 = {
                "labels": ["Gas", "Stromzukauf", "Wärmezukauf", "Kraftstoff"],
                "sizes": [share_of_vc_gas, share_of_vc_el_import, share_of_vc_heat_import, share_of_vc_fuel],
                "colors": ["#ff0000", "#ff8585", "#78000c", "#02a2f7"],
            }
        else:
            PieChart6 = {
                "labels": ["Gas", "Stromzukauf", "Wärmezukauf"],
                "sizes": [share_of_vc_gas, share_of_vc_el_import, share_of_vc_heat_import],
                "colors": ["#ff0000", "#ff8585", "#78000c"],
            }
            axs[1, 2].pie(
                PieChart6["sizes"],
                colors=PieChart6["colors"],
                autopct="%1.1f%%",
                shadow=False,
                startangle=90,
                labeldistance=1.3,
                radius=2,
                normalize=True,
            )
            axs[1, 2].legend(PieChart6["labels"], loc="upper left", bbox_to_anchor=(0.87, 0, 0.5, 1), fontsize=9)
            axs[1, 2].axis("equal")
            axs[1, 2].set_title(
                "Aufteilung der Betriebskosten\n 100% ≙ {:.0f} € pro Person & Jahr".format(float(df["var_costs_total"]))
            )
            plotly_fig.add_trace(
                go.Pie(
                    title="Aufteilung der Betriebskosten<br>100% ≙ {:.0f} € pro Person & Jahr".format(
                        float(df["var_costs_total"])
                    ),
                    title_font_size=18,
                    values=PieChart6["sizes"],
                    labels=PieChart6["labels"],
                    marker_colors=PieChart6["colors"],
                    legendgroup=6,
                    legendgrouptitle_text="Diagramm 6",
                    name="Diagramm 6",
                    hovertemplate="%{label}: <br>%{percent}",
                ),
                row=2,
                col=3,
            )
    else:
        PieChart6 = {"labels": ["None"], "sizes": [1.0], "colors": ["#ff8585"]}
        axs[1, 2].pie(
            PieChart6["sizes"],
            autopct="%1.1f%%",
            shadow=False,
            startangle=90,
            labeldistance=1.3,
            radius=0.01,
            colors=PieChart6["colors"],
            normalize=True,
        )
        axs[1, 2].set_title("Keine Betriebskosten")
        plotly_fig.add_trace(
            go.Pie(
                title="Keine Betriebskosten",
                title_font_size=18,
                values=PieChart6["sizes"],
                labels=PieChart6["labels"],
                marker_colors=PieChart6["colors"],
                legendgroup=6,
                legendgrouptitle_text="Diagramm 6",
                name="Diagramm 6",
                hovertemplate="%{label}: <br>%{percent}",
            ),
            row=2,
            col=3,
        )

    plt.suptitle("Team: " + cfg["team_names"][team_number], fontsize=20, fontweight="bold")
    tpath = f"../{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}/results/teams/team_{cfg['team_names'][team_number]}/"
    os.makedirs(tpath, exist_ok=True)
    plt.savefig(f"{tpath}PieCharts.png", dpi=300)
    plt.close("all")

    plotly_fig.update_layout(
        title="<b>Team: " + cfg["team_names"][team_number] + "</b>",
        title_font_size=20,
        title_x=0.5,
        legend_tracegroupgap=50,
    )
    plotly_fig.update_traces(
        textinfo="none",
    )

    plot_json = plotly.io.to_json(plotly_fig)
    with open(f"{tpath}results_piecharts.json", "w") as f:
        f.write(plot_json)


def static_teamgraphics(config_path, team_number):

    with open(config_path, encoding="utf-8") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.CLoader)

    abs_path = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))
    logging.info("Static visulization")

    file_name_param_01 = cfg["design_parameters_file_name"][team_number]
    file_name_param_02 = cfg["parameters_file_name"]
    path = f"{abs_path}/{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}"
    fpath = path + "/data/"
    file_path_param_01 = fpath + file_name_param_01
    file_path_param_02 = abs_path + "/" + file_name_param_02
    param_df_01 = pd.read_csv(file_path_param_01, index_col=1)
    param_df_02 = pd.read_csv(file_path_param_02, index_col=1)
    param_df = pd.concat([param_df_01, param_df_02], sort=True)
    param_value = param_df["value"]

    number_of_chps = param_value["number_of_chps"]
    number_of_boilers = param_value["number_of_boilers"]
    number_of_windturbines = param_value["number_of_windturbines"]
    number_of_heat_pumps = param_value["number_of_heat_pumps"]
    number_of_daydemand_capacity_el = param_value["capacity_electr_storage"]
    number_of_daydemand_capacity_th = param_value["capacity_thermal_storage"]
    area_pv = param_value["area_PV"]
    area_solar_th = param_value["area_solar_th"]
    number_of_pv_pp = param_value["number_of_PV_pp"]
    # percentage_building_retrofit = param_value['feature_building_retrofit']
    percentage_of_bev = param_value["percentage_of_bev"]

    # Colors:
    def make_color_list(keys):
        col_options = [
            "#69009e",  # 0 BHKW
            "#f6ff00",  # 1 Dachflaechen-PV
            "#ffd500",  # 2 Freiflaechen-PV
            "#02a2f7",  # 3 WEA
            "#ff8585",  # 4 Stromzukauf
            "#1500ff",  # 5 (Ent-) Ladung Stromspeicher
            "#ff0000",  # 6 Strombedarf
            "#00872d",  # 7 Stromueberschuss
            "#6b6b6b",  # 8 (Strombedarf fuer) Waermepumpe
            "#00ff91",  # 9 Ladung E-PKW
            "#e095fc",  # 10 Heizkessel
            "#fa7e02",  # 11 Solarthermie
            "#ff1f00",  # 12 Wärmebedarf
            "#78000c",  # 13 Wärmezukauf
            "#1f6e00",  # 14 Wärmeüberschuss
            "#2020ab",  # 15 Speicher in/ out
            "#4af9ff",  # 16 Mobility_el
            "#e7ff4a",  # 17 Mobility_konventionell
            "#ff4a4a",
        ]  # 18 Mobilitätsbedarf
        col_list = []
        for k in keys:
            # electricity
            if k == "BHKW":
                col_list.append(col_options[0])
            elif k == "Dachflaechen-PV":
                col_list.append(col_options[1])
            elif k == "Freiflaechen-PV":
                col_list.append(col_options[2])
            elif k == "WEA":
                col_list.append(col_options[3])
            elif k == "Stromzukauf":
                col_list.append(col_options[4])
            elif k == "Ladung Stromspeicher":
                col_list.append(col_options[5])
            elif k == "Entladung Stromspeicher":
                col_list.append(col_options[5])
            elif k == "Strombedarf":
                col_list.append(col_options[6])
            elif k == "Stromueberschuss":
                col_list.append(col_options[7])
            elif k == "Strombedarf fuer Waermepumpe":
                col_list.append(col_options[8])
            elif k == "Ladung E-PKW":
                col_list.append(col_options[9])
            # Heat
            elif k == "Waermepumpe":
                col_list.append(col_options[8])
            elif k == "Heizkessel":
                col_list.append(col_options[10])
            elif k == "Solarthermie":
                col_list.append(col_options[11])
            elif k == "Waermebedarf":
                col_list.append(col_options[12])
            elif k == "Waermezukauf":
                col_list.append(col_options[13])
            elif k == "Waermeueberschuss":
                col_list.append(col_options[14])
            elif k == "Entladung Waermespeicher":
                col_list.append(col_options[15])
            elif k == "Ladung Waermespeicher":
                col_list.append(col_options[15])
            # Mobility
            elif k == "Mobilitaet elektrisch":
                col_list.append(col_options[16])
            elif k == "Mobilitaet konventionell":
                col_list.append(col_options[17])
            elif k == "Mobilitaetsbedarf":
                col_list.append(col_options[18])
        return col_list

    energysystem = solph.EnergySystem()
    abs_path = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))
    path = f"{abs_path}/{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}"
    dpath = path + "/results/data/dumps"
    os.makedirs(dpath, exist_ok=True)
    energysystem.restore(dpath=dpath, filename="model_team_{}.oemof".format(cfg["team_names"][team_number]))

    string_results = solph.views.convert_keys_to_strings(energysystem.results["main"])
    shortage_electricity = string_results["shortage_bel", "electricity"]["sequences"]
    shortage_heat = string_results["shortage_bth", "heat"]["sequences"]
    excess_electricity = string_results["electricity", "excess_bel"]["sequences"]
    excess_heat = string_results["heat", "excess_bth"]["sequences"]
    # fuel_consumption = string_results[
    #    'rfuel', 'fuel']['sequences']
    # gas_consumption = string_results[
    #    'rgas', 'natural_gas']['sequences']
    heat_demand = string_results["heat", "demand_th"]["sequences"]
    el_demand = string_results["electricity", "demand_el"]["sequences"]
    if number_of_windturbines > 0:
        el_from_wind = string_results["wind_turbine", "electricity"]["sequences"]
    if area_pv > 0:
        el_from_pv = string_results["PV", "electricity"]["sequences"]
    if number_of_pv_pp > 0:
        el_from_pv_pp = string_results["PV_pp", "electricity"]["sequences"]
    if area_solar_th > 0:
        heat_from_solar = string_results["solar_thermal", "heat"]["sequences"]
    if number_of_chps > 0:
        el_from_chp = string_results["chp", "electricity"]["sequences"]
        heat_from_chp = string_results["chp", "heat"]["sequences"]
    #    fuel_to_chp = string_results[
    #                'natural_gas', 'chp']['sequences']
    if number_of_boilers > 0:
        heat_from_boiler = string_results["boiler", "heat"]["sequences"]
    #    fuel_to_boiler = string_results[
    #        'natural_gas', 'boiler']['sequences']
    if number_of_heat_pumps > 0:
        heat_from_hp = string_results["heat_pump", "heat"]["sequences"]
        el_to_hp = string_results["electricity", "heat_pump"]["sequences"]
    if number_of_daydemand_capacity_el > 0:
        EES_charge = string_results["electricity", "storage_el"]["sequences"]
        EES_discharge = string_results["storage_el", "electricity"]["sequences"]
    if number_of_daydemand_capacity_th > 0:
        TES_charge = string_results["heat", "storage_th"]["sequences"]
        TES_discharge = string_results["storage_th", "heat"]["sequences"]
    if cfg["enable_mobility"] and percentage_of_bev > 0:
        #    mobility_of_bev = string_results[
        #        'bev_discharge', 'mobility_bev']['sequences']
        el_to_bev = string_results["electricity", "bev_charge"]["sequences"]
    # if percentage_of_bev < 100:
    #    mobility_of_car = string_results[
    #        'car', 'mobility']['sequences']
    #    fuel_to_car = string_results[
    #        'fuel', 'car']['sequences']

    # Loop:
    for x in range(1, 5):
        start = cfg["start{}".format(+x)]
        end = cfg["end{}".format(+x)]

        if not start == None and not end == None:
            if start <= 8760 and end <= 8760 and start < end and start >= 0 and end >= 0:
                zeitreihen_el = pd.DataFrame()
                if param_value["number_of_chps"] > 0:
                    zeitreihen_el["BHKW"] = el_from_chp.flow[start:end]
                if param_value["area_PV"] > 0:
                    zeitreihen_el["Dachflaechen-PV"] = el_from_pv.flow[start:end]
                if param_value["number_of_PV_pp"] > 0:
                    zeitreihen_el["Freiflaechen-PV"] = el_from_pv_pp.flow[start:end]
                if param_value["number_of_windturbines"] > 0:
                    zeitreihen_el["WEA"] = el_from_wind.flow[start:end]
                if sum(shortage_electricity.flow[start:end]) > 0.1:
                    zeitreihen_el["Stromzukauf"] = shortage_electricity.flow[start:end]
                if param_value["capacity_electr_storage"] > 0:
                    zeitreihen_el["Ladung Stromspeicher"] = abs(EES_charge.flow[start:end]) * (-1)
                    zeitreihen_el["Entladung Stromspeicher"] = abs(EES_discharge.flow[start:end])
                zeitreihen_el["Strombedarf"] = (el_demand.flow[start:end]) * (-1)
                if sum(excess_electricity.flow[start:end]) > 0.1:
                    zeitreihen_el["Stromueberschuss"] = (excess_electricity.flow[start:end]) * (-1)
                if param_value["number_of_heat_pumps"] > 0:
                    zeitreihen_el["Strombedarf fuer Waermepumpe"] = (el_to_hp.flow[start:end]) * (-1)
                if cfg["enable_mobility"]:
                    if param_value["percentage_of_bev"] > 0:
                        zeitreihen_el["Ladung E-PKW"] = abs(el_to_bev.flow[start:end]) * (-1)
                zeitreihen_el_sortiert = zeitreihen_el.reindex(
                    zeitreihen_el.abs().sum().sort_values(ascending=False).index, axis=1
                )
                dpath = f"../{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}/results/data/dumps/"
                os.makedirs(dpath, exist_ok=True)
                zeitreihen_el_sortiert.to_csv(f"{dpath}Zeitraum_el.csv")
                filename = Path(__file__).parent / f"{dpath}Zeitraum_el.csv"
                param_df = pd.read_csv(filename, index_col=0, encoding="unicode_escape")
                color_list = make_color_list(param_df.keys())
                param_df.plot(kind="area", stacked=True, color=color_list, linewidth=0)
                plt.title(
                    "Team: "
                    + cfg["team_names"][team_number]
                    + "\n Aufteilung der elektrischen Energiemengen des ausgewählten {}. Bereichs: ".format(+x)
                    + str(start)
                    + "h - "
                    + str(end)
                    + "h",
                    size=25,
                )
                plt.ylabel("Stromflüsse [MWh/h]", size=25)
                current1 = pd.DataFrame(list(plt.gca().get_legend_handles_labels()))
                current = current1.transpose()
                sorter = param_df.sum().sort_values(ascending=False).index.tolist()
                sorterIndex = dict(zip(sorter, range(len(sorter))))
                current["Sortiere"] = current[1].map(sorterIndex)
                current.sort_values(by="Sortiere", inplace=True)
                new_handles = current[0]
                new_labels = current[1]
                plt.legend(
                    new_handles,
                    new_labels,
                    bbox_to_anchor=(1.02, 1),
                    loc="upper left",
                    borderaxespad=0,
                    prop={"size": 25},
                )
                plt.yticks(size=25)
                plt.xticks(rotation=45, size=25)
                plt.grid(True)
                figure = plt.gcf()
                figure.set_size_inches(30, 15)
                tpath = f"../{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}/results/teams/"
                os.makedirs(tpath, exist_ok=True)
                plt.savefig(
                    f"{tpath}team_{cfg['team_names'][team_number]}" + "/Zeitraum_el_{}.png".format(+x),
                    dpi=150,
                    bbox_inches="tight",
                )

                # Heat:
                zeitreihen_th = pd.DataFrame()
                if param_value["number_of_heat_pumps"] > 0:
                    zeitreihen_th["Waermepumpe"] = heat_from_hp.flow[start:end]
                if param_value["number_of_chps"] > 0:
                    zeitreihen_th["BHKW"] = heat_from_chp.flow[start:end]
                if param_value["number_of_boilers"] > 0:
                    zeitreihen_th["Heizkessel"] = heat_from_boiler.flow[start:end]
                if param_value["area_solar_th"] > 0:
                    zeitreihen_th["Solarthermie"] = heat_from_solar.flow[start:end]
                zeitreihen_th["Waermebedarf"] = (heat_demand.flow[start:end]) * (-1)
                if sum(shortage_heat.flow[start:end]) > 0.1:
                    zeitreihen_th["Waermezukauf"] = shortage_heat.flow[start:end]
                if sum(excess_heat.flow[start:end]) > 0.1:
                    zeitreihen_th["Waermeueberschuss"] = (excess_heat.flow[start:end]) * (-1)
                if param_value["capacity_thermal_storage"] > 0:
                    zeitreihen_th["Entladung Waermespeicher"] = abs(TES_discharge.flow[start:end])
                    zeitreihen_th["Ladung Waermespeicher"] = abs(TES_charge.flow[start:end]) * (-1)
                zeitreihen_th_sortiert = zeitreihen_th.reindex(
                    zeitreihen_th.abs().sum().sort_values(ascending=False).index, axis=1
                )
                dpath = f"../{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}/results/data/dumps/"
                os.makedirs(dpath, exist_ok=True)
                zeitreihen_th_sortiert.to_csv(f"{dpath}Zeitraum_th.csv")
                filename = Path(__file__).parent / f"{dpath}Zeitraum_th.csv"
                param_df = pd.read_csv(filename, index_col=0, encoding="unicode_escape")
                color_list = make_color_list(param_df.keys())
                param_df.plot(kind="area", stacked=True, color=color_list, linewidth=0)
                plt.title(
                    "Team: "
                    + cfg["team_names"][team_number]
                    + "\n Aufteilung der thermischen Energiemengen des ausgewählten {}. Bereichs: ".format(+x)
                    + str(start)
                    + "h - "
                    + str(end)
                    + "h",
                    size=25,
                )
                plt.ylabel("Stromflüsse [MWh/h]", size=25)
                current1 = pd.DataFrame(list(plt.gca().get_legend_handles_labels()))
                current = current1.transpose()
                sorter = param_df.sum().sort_values(ascending=False).index.tolist()
                sorterIndex = dict(zip(sorter, range(len(sorter))))
                current["Sortiere"] = current[1].map(sorterIndex)
                current.sort_values(by="Sortiere", inplace=True)
                new_handles = current[0]
                new_labels = current[1]
                plt.legend(
                    new_handles,
                    new_labels,
                    bbox_to_anchor=(1.02, 1),
                    loc="upper left",
                    borderaxespad=0,
                    prop={"size": 25},
                )
                plt.yticks(size=25)
                plt.xticks(rotation=45, size=25)
                plt.grid(True)
                figure = plt.gcf()
                figure.set_size_inches(30, 15)
                tpath = f"../{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}/results/teams/"
                os.makedirs(tpath, exist_ok=True)
                plt.savefig(
                    f"{tpath}team_{cfg['team_names'][team_number]}" + "/Zeitraum_th_{}.png".format(+x),
                    dpi=150,
                    bbox_inches="tight",
                )
                plt.close("all")
            else:
                print("Überprüfen Sie die Eingabe des {}. Zeitraums in der Datei: Config.yml".format(+x))


def plot_interactive(config_path, team_number):
    ########################################
    #         Mange Paths and Files        #
    ########################################
    with open(config_path, encoding="utf-8") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.CLoader)

    abs_path = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))

    file_name_param_01 = cfg["design_parameters_file_name"][team_number]
    file_name_param_02 = cfg["parameters_file_name"]
    path = f"{abs_path}/{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}"
    fpath = path + "/data/"
    file_path_param_01 = fpath + file_name_param_01
    file_path_param_02 = abs_path + "/" + file_name_param_02
    param_df_01 = pd.read_csv(file_path_param_01, index_col=1)
    param_df_02 = pd.read_csv(file_path_param_02, index_col=1)
    param_df = pd.concat([param_df_01, param_df_02], sort=True)
    param_value = param_df["value"]

    ########################################
    #      Extract Data From Solution      #
    ########################################
    energysystem = solph.EnergySystem()
    abs_path = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))
    path = f"{abs_path}/{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}"
    dpath = path + "/results/data/dumps"
    os.makedirs(dpath, exist_ok=True)
    energysystem.restore(dpath=dpath, filename="model_team_{}.oemof".format(cfg["team_names"][team_number]))

    ########################################
    #      Interactive Visualization       #
    ########################################
    if cfg["enable_visualization_interactive"]:
        logging.info("Visualize the interactive option of the energy system")
        ########################################
        #    Electricity and heat figures      #
        ########################################

        def shape_legend(node, ax, handles, labels, reverse=False, **kwargs):
            handels = handles
            labels = labels
            axes = ax
            parameter = {}
            new_labels = []
            for label in labels:
                label = label.replace("(", "")
                label = label.replace("), flow)", "")
                label = label.replace(node, "")
                label = label.replace("_pump", "heat_pump")
                label = label.replace("heatheat_pump", "Wärmepumpe")
                label = label.replace(",", "")
                label = label.replace(" ", "")
                label = label.replace("wind_turbine", "WEA")
                label = label.replace("chp", "BHKW")
                label = label.replace("boiler", "Heizkessel")
                label = label.replace("solar_thermal", "Solarthermie")
                label = label.replace("storage_el", "Stromspeicher")
                label = label.replace("storage_th", "Wärmespeicher")
                label = label.replace("PV_pp", "Freiflächen-PV")
                label = label.replace("PV", "Dachflächen-PV")
                label = label.replace("Freiflächen-Dachflächen-PV", "Freiflächen-PV")
                label = label.replace("shortage_bel", "Stromzukauf")
                label = label.replace("shortage_bth", "Wärmezukauf")
                label = label.replace("excess_bel", "Stromüberschuss")
                label = label.replace("excess_bth", "Wärmeüberschuss")
                label = label.replace("bev_charge", "Ladung E-PKW")
                label = label.replace("demand_el", "Strombedarf")
                label = label.replace("demand_th", "Wärmebedarf")
                label = label.replace("heat_pump", "Wärmepumpe")
                new_labels.append(label)
            labels = new_labels

            parameter["bbox_to_anchor"] = kwargs.get("bbox_to_anchor", (1, 0.5))
            parameter["loc"] = kwargs.get("loc", "center left")
            parameter["ncol"] = kwargs.get("ncol", 1)
            plotshare = kwargs.get("plotshare", 0.9)

            if reverse:
                handels = handels.reverse()
                labels = labels.reverse()

            box = axes.get_position()
            axes.set_position([box.x0, box.y0, box.width * plotshare, box.height])
            parameter["handles"] = handels
            parameter["labels"] = labels
            axes.legend(**parameter)
            return axes

        results = energysystem.results["main"]

        area_labels = {
            "((boiler, heat), flow)": "Heizkessel",
            "((chp, heat), flow)": "BHKW",
            "((solar_thermal, heat), flow)": "Solarthermie",
            "((heat_pump, heat), flow)": "Wäremepumpe",
            "((shortage_bth, heat), flow)": "Wärmezukauf",
            "((storage_th, heat), flow)": "Wärmespeicher",
            "((heat, demand_th), flow)": "Wärmebedarf",
            "((heat, storage_th), flow)": "Wärmespeicher",
            "((heat, excess_bth), flow)": "Wärmeüberschuss",
            "((PV, electricity), flow)": "Dachflächen-PV",
            "((PV_pp, electricity), flow)": "Freiflächen-PV",
            "((wind_turbine, electricity), flow)": "WEA",
            "((chp, electricity), flow)": "BHKW",
            "((storage_el, electricity), flow)": "Stromspeicher",
            "((shortage_bel, electricity), flow)": "Stromzukauf",
            "((electricity, excess_bel), flow)": "Stromüberschuss",
            "((electricity, storage_el), flow)": "Stromspeicher",
            "((electricity, bev_charge), flow)": "Ladung E-PKW",
            "((electricity, heat_pump), flow)": "Wärmepumpe",
            "((electricity, demand_el), flow)": "Strombedarf",
        }

        if param_value["number_of_chps"] > 0:
            chp_el_out = (("chp", "electricity"), "flow")
            chp_th_out = (("chp", "heat"), "flow")
            gas_in_chp = (("natural_gas", "chp"), "flow")
        else:
            chp_el_out = 0
            chp_th_out = 0
            gas_in_chp = 0
        if param_value["number_of_boilers"] > 0:
            boiler_th_out = (("boiler", "heat"), "flow")
            gas_in_boiler = (("natural_gas", "boiler"), "flow")
        else:
            boiler_th_out = 0
            gas_in_boiler = 0
        if param_value["number_of_heat_pumps"] > 0:
            heat_pump_th_out = (("heat_pump", "heat"), "flow")
            el_in_heat_pump = (("electricity", "heat_pump"), "flow")
        else:
            heat_pump_th_out = 0
            el_in_heat_pump = 0
        if param_value["capacity_electr_storage"] > 0:
            el_in_els = (("electricity", "storage_el"), "flow")
            els_el_out = (("storage_el", "electricity"), "flow")
        else:
            el_in_els = 0
            els_el_out = 0
        if param_value["capacity_thermal_storage"] > 0:
            th_in_ths = (("heat", "storage_th"), "flow")
            ths_th_out = (("storage_th", "heat"), "flow")
        else:
            th_in_ths = 0
            ths_th_out = 0
        if param_value["percentage_of_bev"] > 0:
            el_in_bev = (("electricity", "bev_charge"), "flow")
        else:
            el_in_bev = 0
        # General Coloring
        cdict = {
            # electricity
            (("PV", "electricity"), "flow"): "#f6ff00",
            (("PV_pp", "electricity"), "flow"): "#ffd500",
            (("wind_turbine", "electricity"), "flow"): "#02a2f7",
            chp_el_out: "#69009e",
            el_in_els: "#1500ff",
            els_el_out: "#1500ff",
            (("shortage_bel", "electricity"), "flow"): "#ff8585",
            el_in_heat_pump: "#6b6b6b",
            el_in_bev: "#00ff91",
            (("electricity", "excess_bel"), "flow"): "#00872d",
            (("electricity", "demand_el"), "flow"): "#ff0000",
            # Heat
            heat_pump_th_out: "#6b6b6b",
            chp_th_out: "#69009e",
            boiler_th_out: "#e095fc",
            (("solar_thermal", "heat"), "flow"): "#fa7e02",
            (("heat", "demand_th"), "flow"): "#ff1f00",
            (("shortage_bth", "heat"), "flow"): "#78000c",
            (("heat", "excess_bth"), "flow"): "#1f6e00",
            ths_th_out: "#2020ab",
            th_in_ths: "#2020ab",
            # Gas
            gas_in_chp: "#ff0000",
            gas_in_boiler: "#00872d",
            (("rgas", "natural_gas"), "flow"): "#70e7ff",
            # km_bev
            (("bev_discharge", "mobility_bev"), "flow"): "#00ff91",
        }

        # Figure electricity one year
        if cfg["enable_mobility"]:
            if param_value["capacity_electr_storage"] > 0:
                inorder = [
                    (("PV", "electricity"), "flow"),
                    (("PV_pp", "electricity"), "flow"),
                    (("wind_turbine", "electricity"), "flow"),
                    (("chp", "electricity"), "flow"),
                    (("storage_el", "electricity"), "flow"),
                    (("shortage_bel", "electricity"), "flow"),
                ]
            else:
                inorder = [
                    (("PV", "electricity"), "flow"),
                    (("PV_pp", "electricity"), "flow"),
                    (("wind_turbine", "electricity"), "flow"),
                    (("chp", "electricity"), "flow"),
                    (("shortage_bel", "electricity"), "flow"),
                ]

            if (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "bev_charge"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "bev_charge"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "bev_charge"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "bev_charge"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            else:
                outorder = [(("electricity", "demand_el"), "flow"), (("electricity", "excess_bel"), "flow")]
        else:
            if param_value["capacity_electr_storage"] > 0:
                inorder = [
                    (("PV", "electricity"), "flow"),
                    (("PV_pp", "electricity"), "flow"),
                    (("wind_turbine", "electricity"), "flow"),
                    (("chp", "electricity"), "flow"),
                    (("storage_el", "electricity"), "flow"),
                    (("shortage_bel", "electricity"), "flow"),
                ]
            else:
                inorder = [
                    (("PV", "electricity"), "flow"),
                    (("PV_pp", "electricity"), "flow"),
                    (("wind_turbine", "electricity"), "flow"),
                    (("chp", "electricity"), "flow"),
                    (("shortage_bel", "electricity"), "flow"),
                ]

            if (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [(("electricity", "demand_el"), "flow"), (("electricity", "excess_bel"), "flow")]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            else:
                outorder = [(("electricity", "demand_el"), "flow"), (("electricity", "excess_bel"), "flow")]

        fig = plt.figure(figsize=(25, 7.5))
        electricity_seq = solph.views.node(results, "electricity")["sequences"]
        plot_slice = oev.plot.slice_df(electricity_seq, date_from=date(2030, 1, 1))
        my_plot = oev.plot.io_plot(
            "electricity",
            plot_slice,
            cdict=cdict,
            inorder=inorder,
            outorder=outorder,
            ax=fig.add_subplot(1, 1, 1),
            smooth=True,
            line_kwa={"linewidth": 1.7},
        )
        ax = shape_legend("electricity", **my_plot)
        oev.plot.set_datetime_ticks(ax, plot_slice.index, tick_distance=72, date_format="%d.%m", offset=12)
        plt.subplots_adjust(left=0.045, right=0.88, top=0.93)
        ax.xaxis.set_tick_params(rotation=90, labelsize=8)
        ax.set_ylabel("Electricity Power in MW")
        ax.set_xlabel("2030")
        ax.set_title("Team: " + cfg["team_names"][team_number] + "\n Aufteilung der elektrischen Energiemengen")

        # Figure heat one year
        if param_value["capacity_thermal_storage"] > 0 and param_value["number_of_heat_pumps"] > 0:
            inorder = [
                (("solar_thermal", "heat"), "flow"),
                (("boiler", "heat"), "flow"),
                (("chp", "heat"), "flow"),
                (("heat_pump", "heat"), "flow"),
                (("shortage_bth", "heat"), "flow"),
                (("storage_th", "heat"), "flow"),
            ]
        elif ["capacity_thermal_storage"] == 0 and param_value["number_of_heat_pumps"] == 0:
            inorder = [
                (("solar_thermal", "heat"), "flow"),
                (("boiler", "heat"), "flow"),
                (("chp", "heat"), "flow"),
                (("shortage_bth", "heat"), "flow"),
            ]
        elif param_value["capacity_thermal_storage"] > 0 and param_value["number_of_heat_pumps"] == 0:
            inorder = [
                (("solar_thermal", "heat"), "flow"),
                (("boiler", "heat"), "flow"),
                (("chp", "heat"), "flow"),
                (("shortage_bth", "heat"), "flow"),
                (("storage_th", "heat"), "flow"),
            ]
        else:
            inorder = [
                (("solar_thermal", "heat"), "flow"),
                (("boiler", "heat"), "flow"),
                (("chp", "heat"), "flow"),
                (("heat_pump", "heat"), "flow"),  # test
                (("shortage_bth", "heat"), "flow"),
            ]
        if param_value["capacity_thermal_storage"] > 0:
            outorder = [
                (("heat", "demand_th"), "flow"),
                (("heat", "storage_th"), "flow"),
                (("heat", "excess_bth"), "flow"),
            ]
        else:
            outorder = [(("heat", "demand_th"), "flow"), (("heat", "excess_bth"), "flow")]

        fig = plt.figure(figsize=(25, 7.5))
        heat_seq = solph.views.node(results, "heat")["sequences"]
        # heat_seq.to_csv("seq.csv", header=True)
        plot_slice = oev.plot.slice_df(heat_seq, date_from=date(2030, 1, 1))
        my_plot = oev.plot.io_plot(
            "heat",
            plot_slice,
            cdict=cdict,
            inorder=inorder,
            outorder=outorder,
            ax=fig.add_subplot(1, 1, 1),
            smooth=True,
            line_kwa={"linewidth": 1.7},
        )
        ax = shape_legend("heat", **my_plot)
        oev.plot.set_datetime_ticks(ax, plot_slice.index, tick_distance=72, date_format="%d.%m", offset=12)
        plt.subplots_adjust(left=0.045, right=0.86, top=0.93)
        ax.xaxis.set_tick_params(rotation=90, labelsize=8)
        ax.set_ylabel("Heat Power in MW")
        ax.set_xlabel("2030")
        ax.set_title("Team: " + cfg["team_names"][team_number] + "\nAufteilung der thermischen Energiemengen")

        # plt.show()

        # Figure electricity of choice of period of time
        with open(config_path, encoding="utf-8") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.CLoader)
        if cfg["enable_mobility"]:
            if param_value["capacity_electr_storage"] > 0:
                inorder = [
                    (("PV", "electricity"), "flow"),
                    (("PV_pp", "electricity"), "flow"),
                    (("wind_turbine", "electricity"), "flow"),
                    (("chp", "electricity"), "flow"),
                    (("storage_el", "electricity"), "flow"),
                    (("shortage_bel", "electricity"), "flow"),
                ]
            else:
                inorder = [
                    (("PV", "electricity"), "flow"),
                    (("PV_pp", "electricity"), "flow"),
                    (("wind_turbine", "electricity"), "flow"),
                    (("chp", "electricity"), "flow"),
                    (("shortage_bel", "electricity"), "flow"),
                ]
            if (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "bev_charge"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "bev_charge"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "bev_charge"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "bev_charge"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            else:
                outorder = [(("electricity", "demand_el"), "flow"), (("electricity", "excess_bel"), "flow")]
        else:
            if param_value["capacity_electr_storage"] > 0:
                inorder = [
                    (("PV", "electricity"), "flow"),
                    (("PV_pp", "electricity"), "flow"),
                    (("wind_turbine", "electricity"), "flow"),
                    (("chp", "electricity"), "flow"),
                    (("storage_el", "electricity"), "flow"),
                    (("shortage_bel", "electricity"), "flow"),
                ]
            else:
                inorder = [
                    (("PV", "electricity"), "flow"),
                    (("PV_pp", "electricity"), "flow"),
                    (("wind_turbine", "electricity"), "flow"),
                    (("chp", "electricity"), "flow"),
                    (("shortage_bel", "electricity"), "flow"),
                ]
            if (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] > 0
            ):
                outorder = [(("electricity", "demand_el"), "flow"), (("electricity", "excess_bel"), "flow")]
            elif (
                param_value["number_of_heat_pumps"] > 0
                and param_value["capacity_electr_storage"] == 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "heat_pump"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            elif (
                param_value["number_of_heat_pumps"] == 0
                and param_value["capacity_electr_storage"] > 0
                and param_value["percentage_of_bev"] == 0
            ):
                outorder = [
                    (("electricity", "demand_el"), "flow"),
                    (("electricity", "storage_el"), "flow"),
                    (("electricity", "excess_bel"), "flow"),
                ]
            else:
                outorder = [(("electricity", "demand_el"), "flow"), (("electricity", "excess_bel"), "flow")]

        fig = plt.figure(figsize=(16, 7))
        plt.subplots_adjust(left=0.038, right=0.98, top=0.926, bottom=0.15)
        electricity_seq = solph.views.node(results, "electricity")["sequences"]
        plot_slice = oev.plot.slice_df(
            electricity_seq,
            date_from=date(cfg["year_from"], cfg["month_from"], cfg["day_from"]),
            date_to=date(cfg["year_to"], cfg["month_to"], cfg["day_to"]),
        )
        my_plot = oev.plot.io_plot(
            "electricity",
            plot_slice,
            cdict=cdict,
            inorder=inorder,
            outorder=outorder,
            ax=fig.add_subplot(1, 1, 1),
            smooth=True,
            line_kwa={"linewidth": 2.5},
        )
        ax = shape_legend("electricity", **my_plot)
        oev.plot.set_datetime_ticks(ax, plot_slice.index, number_autoticks=15, date_format="%H Uhr %d.%m", offset=0)
        ax.xaxis.set_tick_params(rotation=45, labelsize=10)
        ax.set_ylabel("Electricity Power in MW")
        ax.set_xlabel("2030")
        ax.set_title(
            "Team: "
            + cfg["team_names"][team_number]
            + "\nAufteilung der elektrischen Energiemengen des ausgewählten Bereichs: "
            + str(cfg["day_from"])
            + "/"
            + str(cfg["month_from"])
            + "-"
            + str(cfg["day_to"])
            + "/"
            + str(cfg["month_to"])
            + "/"
            + str(cfg["year_to"])
        )
        ax.grid(True)
        tpath = f"../{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}/results/teams/"
        os.makedirs(tpath, exist_ok=True)
        plt.savefig(
            f"{tpath}team_{cfg['team_names'][team_number]}/electricity_selected_timezone.png",
            dpi=300,
            bbox_inches="tight",
        )
        plt.close(fig)
        plotly_fig = go.Figure()
        # plotly_fig = tls.mpl_to_plotly(fig)
        for c in reversed(ax.properties()["children"]):
            if type(c) == matplotlib.collections.PolyCollection:
                color = c.get_facecolor()[0]
                vertices = c.properties()["paths"][0].vertices
                plotly_fig.add_trace(
                    go.Scatter(
                        name=area_labels[c.properties()["label"]],
                        mode="none",
                        x=plot_slice.index,
                        y=np.flip(vertices[:, 1][-98:-1]),
                        fill="tozeroy",
                        fillcolor=f"rgb({color[0]*255},{color[1]*255},{color[2]*255})",
                    )
                )
        for c in ax.properties()["children"]:
            if type(c) == matplotlib.lines.Line2D:
                if "_line" in c.properties()["label"]:
                    continue
                plotly_fig.add_trace(
                    go.Scatter(
                        name=area_labels[c.properties()["label"]],
                        mode="lines",
                        line=dict(
                            color=c.properties()["color"],
                            width=3,
                        ),
                        x=plot_slice.index,
                        y=c.properties()["ydata"],
                    )
                )
        plotly_fig.update_layout(
            hovermode="x unified",
            title=f'Team: {cfg["team_names"][team_number]}<br>'
            + "Aufteilung der elektrischen Energiemengen des ausgewählten Bereichs: "
            + str(cfg["day_from"])
            + "/"
            + str(cfg["month_from"])
            + "-"
            + str(cfg["day_to"])
            + "/"
            + str(cfg["month_to"])
            + "/"
            + str(cfg["year_to"]),
            title_x=0.5,
            title_font_size=20,
        )

        plot_json = plotly.io.to_json(plotly_fig)
        with open(f"{tpath}team_{cfg['team_names'][team_number]}/results_electricity.json", "w") as f:
            f.write(plot_json)

        # Figure heat of choice of period of time
        if param_value["capacity_thermal_storage"] > 0 and param_value["number_of_heat_pumps"] > 0:
            inorder = [
                (("solar_thermal", "heat"), "flow"),
                (("boiler", "heat"), "flow"),
                (("chp", "heat"), "flow"),
                (("heat_pump", "heat"), "flow"),
                (("shortage_bth", "heat"), "flow"),
                (("storage_th", "heat"), "flow"),
            ]
        elif ["capacity_thermal_storage"] == 0 and param_value["number_of_heat_pumps"] == 0:
            inorder = [
                (("solar_thermal", "heat"), "flow"),
                (("boiler", "heat"), "flow"),
                (("chp", "heat"), "flow"),
                (("shortage_bth", "heat"), "flow"),
            ]
        elif param_value["capacity_thermal_storage"] > 0 and param_value["number_of_heat_pumps"] == 0:
            inorder = [
                (("solar_thermal", "heat"), "flow"),
                (("boiler", "heat"), "flow"),
                (("chp", "heat"), "flow"),
                (("shortage_bth", "heat"), "flow"),
                (("storage_th", "heat"), "flow"),
            ]
        else:
            inorder = [
                (("solar_thermal", "heat"), "flow"),
                (("boiler", "heat"), "flow"),
                (("chp", "heat"), "flow"),
                (("heat_pump", "heat"), "flow"),
                (("shortage_bth", "heat"), "flow"),
            ]

        if param_value["capacity_thermal_storage"] > 0:
            outorder = [
                (("heat", "demand_th"), "flow"),
                (("heat", "storage_th"), "flow"),
                (("heat", "excess_bth"), "flow"),
            ]
        else:
            outorder = [(("heat", "demand_th"), "flow"), (("heat", "excess_bth"), "flow")]
        fig = plt.figure(figsize=(16, 7))
        plt.subplots_adjust(left=0.038, right=0.975, top=0.926, bottom=0.15)
        heat_seq = solph.views.node(results, "heat")["sequences"]
        plot_slice = oev.plot.slice_df(
            heat_seq,
            date_from=date(cfg["year_from"], cfg["month_from"], cfg["day_from"]),
            date_to=date(cfg["year_to"], cfg["month_to"], cfg["day_to"]),
        )
        my_plot = oev.plot.io_plot(
            "heat",
            plot_slice,
            cdict=cdict,
            inorder=inorder,
            outorder=outorder,
            ax=fig.add_subplot(1, 1, 1),
            smooth=True,
            line_kwa={"linewidth": 2.5},
        )
        ax = shape_legend("heat", **my_plot)
        oev.plot.set_datetime_ticks(ax, plot_slice.index, number_autoticks=15, date_format="%H Uhr %d.%m", offset=0)
        ax.xaxis.set_tick_params(rotation=45, labelsize=10)
        ax.set_ylabel("Heat Power in MW")
        ax.set_xlabel("2030")
        ax.grid(True)
        ax.set_title(
            "Team: "
            + cfg["team_names"][team_number]
            + "\nAufteilung der thermischen Energiemengen des asgewählten Bereichs: "
            + str(cfg["day_from"])
            + "/"
            + str(cfg["month_from"])
            + "-"
            + str(cfg["day_to"])
            + "/"
            + str(cfg["month_to"])
            + "/"
            + str(cfg["year_to"])
        )
        tpath = f"../{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}/results/teams/"
        os.makedirs(tpath, exist_ok=True)
        plt.savefig(
            f"{tpath}team_{cfg['team_names'][team_number]}/Heat_selected_timezone.png", dpi=300, bbox_inches="tight"
        )
        plt.close(fig)
        plotly_fig = go.Figure()
        # plotly_fig = tls.mpl_to_plotly(fig)
        for c in reversed(ax.properties()["children"]):
            if type(c) == matplotlib.collections.PolyCollection:
                color = c.get_facecolor()[0]
                vertices = c.properties()["paths"][0].vertices
                plotly_fig.add_trace(
                    go.Scatter(
                        name=area_labels[c.properties()["label"]],
                        mode="none",
                        x=plot_slice.index,
                        y=np.flip(vertices[:, 1][-98:-1]),
                        fill="tozeroy",
                        fillcolor=f"rgb({color[0]*255},{color[1]*255},{color[2]*255})",
                    )
                )
        for c in ax.properties()["children"]:
            if type(c) == matplotlib.lines.Line2D:
                if "_line" in c.properties()["label"]:
                    continue
                plotly_fig.add_trace(
                    go.Scatter(
                        name=area_labels[c.properties()["label"]],
                        mode="lines",
                        line=dict(
                            color=c.properties()["color"],
                            width=3,
                        ),
                        x=plot_slice.index,
                        y=c.properties()["ydata"],
                    )
                )
        plotly_fig.update_layout(
            hovermode="x unified",
            title=f'Team: {cfg["team_names"][team_number]}<br>'
            + "Aufteilung der thermischen Energiemengen des asgewählten Bereichs: "
            + str(cfg["day_from"])
            + "/"
            + str(cfg["month_from"])
            + "-"
            + str(cfg["day_to"])
            + "/"
            + str(cfg["month_to"])
            + "/"
            + str(cfg["year_to"]),
            title_x=0.5,
            title_font_size=20,
        )

        plot_json = plotly.io.to_json(plotly_fig)
        with open(f"{tpath}team_{cfg['team_names'][team_number]}/results_heat.json", "w") as f:
            f.write(plot_json)


def plot_team_results(config_path, df_teamdata):

    with open(config_path, encoding="utf-8") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.CLoader)

    cost = df_teamdata["costs"]
    em = df_teamdata["emissions"]
    suff = df_teamdata["selfsufficiency"]
    # print(suff)

    red_beuth = (227 / 255, 35 / 255, 37 / 255)
    beuth_col_1 = (223 / 255, 242 / 255, 243 / 255)
    beuth_col_2 = (178 / 255, 225 / 255, 227 / 255)
    beuth_col_3 = (0 / 255, 152 / 255, 161 / 255)
    white = (255 / 255, 255 / 255, 255 / 255)

    labels_list = []
    for tn in cfg["team_names"]:
        # new_name = 'Team ' + tn
        new_name = tn
        labels_list.append(new_name)
    labels = labels_list

    spath = f"../{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}/results/summary/"
    os.makedirs(spath, exist_ok=True)

    for show_team_names in [False, True]:
        fig = plt.figure(figsize=(8, 6))  # default figsize=(8, 6)
        plt.style.use("ggplot")
        plt.rcParams["axes.facecolor"] = beuth_col_3
        plt.ylabel("CO2-Emissionen in kg/a & Person", fontsize=14)
        plt.xlabel("Kosten in €/a & Person", fontsize=14)
        if cfg["enable_mobility"]:
            plt.axis([0, 10000, 0, 5000])
            # plt.axis([0, 5000, 0, 20000])
        else:
            plt.axis([0, 7000, 0, 3500])

        plt.title("Jährliche Emissionen und Kosten der Energieversorgung je Person", fontsize=14)
        plt.suptitle(cfg["workshop_title"], fontsize=10)
        plt.tick_params(axis="both", which="major", labelsize=12)
        # N = len(df_basic_results_and_team_decision)

        plt.scatter(
            cost,
            em,
            marker="o",
            c=[red_beuth],
            # s=df_basic_results_and_team_decision['selfsufficiency'] * 10, #default *1000
            s=20 + (suff * suff * suff * suff) * 0.000005,
            # s=100,
            edgecolors=beuth_col_2,
            linewidths=1.0,
            alpha=1,
            cmap=plt.get_cmap("Spectral"),
        )
        plt.text(
            100,
            200,
            "Copyright ©, Berliner Hochschule für " + "Technik Berlin. All rights reserved.",
            fontsize=11.5,
            color=beuth_col_1,
            ha="left",
            va="top",
            alpha=0.5,
        )
        if not show_team_names:
            # plt.show()
            plt.savefig(f"{spath}results_no_names.png", dpi=300)

        if show_team_names:
            for label, x, y in zip(labels, cost, em):
                plt.annotate(
                    label,
                    xy=(x, y),
                    xytext=(75, 40),
                    textcoords="offset points",
                    ha="right",  # horizontal alignment
                    va="bottom",  # vertical alignment 'bottom'
                    bbox=dict(boxstyle="round,pad=0.5", fc=beuth_col_1, alpha=0.5),
                    arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"),
                )
            plt.savefig(f"{spath}results_with_team_names.png", dpi=300)
            plotly_fig = tls.mpl_to_plotly(fig)
            x_range = [0, 0]
            y_range = [0, 0]
            if cfg["enable_mobility"]:
                x_range = [0, 10000]
                y_range = [0, 5000]
            else:
                x_range = [0, 7000]
                y_range = [0, 3500]
            plotly_fig.update_traces(
                dict(
                    hovertext=labels,
                    hoverinfo="text",
                    marker=dict(
                        symbol="circle",
                        size=20 + (suff * suff * suff * suff) * 0.0000001,
                        color=f"rgb{red_beuth}",
                        line=dict(width=1, color=f"rgb{beuth_col_2}"),
                    ),
                ),
            )
            plotly_fig.update_annotations(
                patch=dict(
                    font=dict(size=16),
                ),
                selector=dict(text="Copyright ©, Berliner Hochschule für Technik Berlin. All rights reserved."),
            )
            plotly_fig.update_layout(
                plot_bgcolor=f"rgb{beuth_col_3}",
                hovermode="closest",
                # hovermode="x unified",
                title=f"<sup>{cfg['workshop_title']}</sup><br>Jährliche Emissionen und Kosten der Energieversorgung je Person",
                title_font_size=20,
                title_x=0.5,
                xaxis_range=x_range,
                xaxis_title="Kosten in €/a & Person",
                xaxis_title_font_size=20,
                yaxis_range=y_range,
                yaxis_title="CO2-Emissionen in kg/a & Person",
                yaxis_title_font_size=20,
                width=800,
                height=700,
                dragmode=False,
            )

            plot_json = plotly.io.to_json(plotly_fig)
            with open(f"{spath}results_summary.json", "w") as f:
                f.write(plot_json)

    plt.rcParams["axes.facecolor"] = white
    plt.style.use("default")
