"""

This program is part of a game-based workshop about energy systems.
During the workshop up to 8 teams design energy systems by selecting and
combining technologies to supply heat and electrical power. Their design
parameter are the simulation input.
This Program calls the energy system simulation (optimization) for
each team and analysis the results based on settings made in
'experimental_config/config.yml'.

Date: 2022
Author: Profs of University
Licence: GPL-3.0

"""

import os
import sys
import pandas as pd
from model_energy_system import run_model

# from basic_analysis import display_results
from detailed_analysis import analyse_energy_system
from detailed_analysis import store_sequences
from detailed_analysis import display_results
from graphic_analysis import static_teamgraphics
from graphic_analysis import pie_charts
from graphic_analysis import plot_interactive
from graphic_analysis import plot_team_results

import logging
import yaml
from oemof.tools import logger


def main(args):
    # Choose configuration file to run model with
    exp_cfg_file_name = "config.yml"
    if len(args) > 1:
        exp_cfg_file_name = args[1] + "/" + exp_cfg_file_name
    config_file_path = os.path.abspath("../" + exp_cfg_file_name)
    with open(config_file_path, encoding="utf-8") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.CLoader)

    logger.define_logging(logfile="main.log", screen_level=logging.INFO, file_level=logging.DEBUG)

    # global teamdata
    if cfg["run_model"]:
        for n in range(cfg["number_of_teams"]):
            run_model(config_path=config_file_path, team_number=n)

    if cfg["run_detailed_analysis"]:
        logging.info("Run detailed analysis.")
        for n in range(cfg["number_of_teams"]):
            teamdata, teamdata_as_table = analyse_energy_system(config_path=config_file_path, team_number=n)
            apath = f"../{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}/results/data/analysis/"
            os.makedirs(apath, exist_ok=True)
            teamdata.to_csv(f"{apath}teamdata_{cfg['team_names'][n]}.csv")
            if n == 0:
                df_teamdata = teamdata
                df_teamdata_table = teamdata_as_table
            else:
                df_teamdata_aux = teamdata
                df_teamdata_table_aux = teamdata_as_table
                df_teamdata = pd.concat([df_teamdata, df_teamdata_aux])
                df_teamdata_table = pd.concat([df_teamdata_table, df_teamdata_table_aux], axis=1)
        spath = f"../{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}/results/summary/"
        os.makedirs(spath, exist_ok=True)
        df_teamdata.to_csv(f"{spath}results.csv")
        df_teamdata_table.to_csv(f"{spath}results_table.csv")

    if cfg["display_results"]:
        logging.info("Display results.")
        for n in range(cfg["number_of_teams"]):
            display_results(config_path=config_file_path, team_number=n)

    if cfg["plot_team_results"] & cfg["run_detailed_analysis"]:
        logging.info("Plot team results.")
        plot_team_results(config_path=config_file_path, df_teamdata=df_teamdata)

    if cfg["enable_analysing_sequences"]:
        for n in range(cfg["number_of_teams"]):
            store_sequences(config_path=config_file_path, team_number=n)

    if cfg["enable_visualization_static"]:
        for n in range(cfg["number_of_teams"]):
            static_teamgraphics(config_path=config_file_path, team_number=n)

    if cfg["enable_pie_charts"]:
        for n in range(cfg["number_of_teams"]):
            pie_charts(config_path=config_file_path, team_number=n)

    if cfg["enable_visualization_interactive"]:
        for n in range(cfg["number_of_teams"]):
            plot_interactive(config_path=config_file_path, team_number=n)


if __name__ == "__main__":
    main(sys.argv)
