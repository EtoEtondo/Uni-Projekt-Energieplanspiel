###############################################################################
# imports
###############################################################################

# Default logger of oemof
import oemof.solph as solph
from oemof.solph import helpers
from oemof.tools import logger
import logging
import os
import pandas as pd
import yaml


def run_model(config_path, team_number):
    with open(config_path, encoding="utf-8") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.CLoader)

    if cfg["debug"]:
        number_of_time_steps = 3
    else:
        number_of_time_steps = 8760

    solver = cfg["solver"]
    debug = cfg["debug"]
    solver_verbose = cfg["solver_verbose"]

    # initiate the logger (see the API docs for more information)
    logger.define_logging(
        logfile="model_team_{}.log".format(cfg["team_names"][team_number]),
        screen_level=logging.INFO,
        file_level=logging.DEBUG,
    )

    logging.info("Initialize the energy system")
    date_time_index = pd.date_range("1/1/2030", periods=number_of_time_steps, freq="H")

    energysystem = solph.EnergySystem(timeindex=date_time_index)

    ##########################################################################
    # Read time series and parameter values from data files
    ##########################################################################

    abs_path = os.path.dirname(os.path.abspath(os.path.join(__file__, "..")))

    file_path_ts = abs_path + "/" + cfg["time_series_file_name"]
    data = pd.read_csv(file_path_ts)

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

    ##########################################################################
    # Create oemof object
    ##########################################################################

    logging.info("Create oemof objects")

    # Busses
    bel = solph.Bus(label="electricity")
    bth = solph.Bus(label="heat")
    bgas = solph.Bus(label="natural_gas")
    bfuel = solph.Bus(label="fuel")
    bkm = solph.Bus(label="mobility")
    bbev = solph.Bus(label="bev")
    bkmbev = solph.Bus(label="mobility_bev")

    energysystem.add(bgas, bel, bth, bfuel, bkm, bbev, bkmbev)

    ###################
    ### Sinks       ###
    ###################

    energysystem.add(
        solph.Sink(label="excess_bel", inputs={bel: solph.Flow(variable_costs=param_value["var_costs_excess_bel"])})
    )
    energysystem.add(
        solph.Sink(label="excess_bth", inputs={bth: solph.Flow(variable_costs=param_value["var_costs_excess_bth"])})
    )
    energysystem.add(
        solph.Sink(label="demand_el", inputs={bel: solph.Flow(fix=data["Demand_el [MWh]"], nominal_value=1)})  # [MWh]
    )

    if cfg["enable_building_retrofit"]:
        demand_heat_reduction = param_value["feature_building_retrofit"]
        energysystem.add(
            solph.Sink(
                label="demand_th",
                inputs={
                    bth: solph.Flow(
                        fix=data["Demand_th [MWh]"] * (1 - (demand_heat_reduction * 0.01)), nominal_value=1  # [MWh]
                    )
                },
            )
        )
    else:
        energysystem.add(
            solph.Sink(
                label="demand_th", inputs={bth: solph.Flow(fix=data["Demand_th [MWh]"], nominal_value=1)}  # [MWh]
            )
        )

    if cfg["enable_mobility"]:
        energysystem.add(
            solph.Sink(
                label="demand_km_bev",
                inputs={
                    bkmbev: solph.Flow(
                        fix=data["Mobility_bev [MWh]"] * (param_value["percentage_of_bev"] / 100), nominal_value=1
                    )
                },
            )
        )
        energysystem.add(
            solph.Sink(
                label="demand_km",
                inputs={
                    bkm: solph.Flow(
                        fix=data["Mobility_car [km]"] * ((100 - param_value["percentage_of_bev"]) / 100),
                        nominal_value=1,
                    )
                },
            )
        )

    ###################
    ### Sources     ###
    ###################

    energysystem.add(
        solph.Source(
            label="shortage_bel", outputs={bel: solph.Flow(variable_costs=param_value["var_costs_shortage_bel"])}
        )
    )
    energysystem.add(
        solph.Source(
            label="shortage_bth", outputs={bth: solph.Flow(variable_costs=param_value["var_costs_shortage_bth"])}
        )
    )
    energysystem.add(
        solph.Source(
            label="rgas",
            outputs={
                bgas: solph.Flow(
                    nominal_value=param_value["nom_val_gas"],
                    summed_max=param_value["sum_max_gas"],
                    variable_costs=param_value["var_costs_gas"],
                )
            },
        )
    )
    if cfg["enable_mobility"]:
        energysystem.add(
            solph.Source(
                label="rfuel",
                outputs={
                    bfuel: solph.Flow(
                        nominal_value=param_value["nom_val_fuel"],
                        summed_max=param_value["sum_max_fuel"],
                        variable_costs=param_value["var_costs_fuel"],
                    )
                },
            )
        )

    # Windpower
    if param_value["number_of_windturbines"] > 0:
        energysystem.add(
            solph.Source(
                label="wind_turbine",
                outputs={
                    bel: solph.Flow(
                        fix=data["Wind_power [kW/unit]"], nominal_value=0.001 * param_value["number_of_windturbines"]
                    )
                },
            )
        )

    # Open-field photovoltaic power plant
    if param_value["number_of_PV_pp"] > 0:
        energysystem.add(
            solph.Source(
                label="PV_pp",
                outputs={
                    bel: solph.Flow(
                        fix=(data["Sol_irradiation [Wh/sqm]"] * 0.000001 * param_value["eta_PV"]),  # [MWh/m²]
                        nominal_value=param_value["PV_pp_surface_area"] * 10000,  # [m²]
                    )
                },
            )
        )

    # Rooftop photovoltaic
    if param_value["area_PV"] > 0:
        energysystem.add(
            solph.Source(
                label="PV",
                outputs={
                    bel: solph.Flow(
                        fix=(data["Sol_irradiation [Wh/sqm]"] * 0.000001 * param_value["eta_PV"]),  # [MWh/m²]
                        nominal_value=param_value["area_PV"] * 10000,  # [m²]
                    )
                },
            )
        )

    # Rooftop solar thermal
    if param_value["area_solar_th"] > 0:
        energysystem.add(
            solph.Source(
                label="solar_thermal",
                outputs={
                    bth: solph.Flow(
                        fix=(data["Sol_irradiation [Wh/sqm]"] * 0.000001 * param_value["eta_solar_th"]),  # [MWh/m²]
                        nominal_value=param_value["area_solar_th"] * 10000,  # [m²]
                    )
                },
            )
        )

    ###################
    ### Transformer ###
    ###################

    # CHP
    if param_value["number_of_chps"] > 0:
        energysystem.add(
            solph.Transformer(
                label="chp",
                inputs={bgas: solph.Flow()},
                outputs={bth: solph.Flow(nominal_value=param_value["number_of_chps"] * 0.5), bel: solph.Flow()},  # [MW]
                conversion_factors={
                    bth: param_value["conversion_factor_bth_chp"],
                    bel: param_value["conversion_factor_bel_chp"],
                },
            )
        )
    # HP
    if param_value["number_of_heat_pumps"] > 0:
        energysystem.add(
            solph.Transformer(
                label="heat_pump",
                inputs={bel: solph.Flow()},
                outputs={
                    bth: solph.Flow(nominal_value=(param_value["number_of_heat_pumps"] * param_value["COP_heat_pump"]))
                },  # [MW]
                conversion_factors={bth: param_value["COP_heat_pump"]},
            )
        )
    # Boiler
    if param_value["number_of_boilers"] > 0:
        energysystem.add(
            solph.Transformer(
                label="boiler",
                inputs={bgas: solph.Flow()},
                outputs={bth: solph.Flow(nominal_value=param_value["number_of_boilers"] * 3)},  # [MW]
                conversion_factors={bth: param_value["conversion_factor_boiler"]},
            )
        )

    if cfg["enable_mobility"]:
        # BEV-Charging
        if param_value["percentage_of_bev"] > 0:
            energysystem.add(
                solph.Transformer(
                    label="bev_charge",
                    inputs={bel: solph.Flow()},
                    outputs={
                        bbev: solph.Flow(
                            max=data["Charging [-]"],
                            nominal_value=(
                                (param_value["percentage_of_bev"] / 100)
                                * param_value["vehicle"]
                                * param_value["charging_power"]
                            ),
                            conversion_factors={bel: param_value["conversion_factor_charging"]},
                        )
                    },
                )
            )

        # BEV-Discharging
        energysystem.add(
            solph.Transformer(
                label="bev_discharge",
                inputs={
                    bbev: solph.Flow(
                        nominal_value=(param_value["percentage_of_bev"] / 100)
                        * param_value["vehicle"]
                        * param_value["charging_power"]
                    )
                },
                outputs={bkmbev: solph.Flow()},
                conversion_factors={bbev: param_value["conversion_factor_charging"]},
            )
        )

        # Car
        if param_value["percentage_of_bev"] < 100:
            energysystem.add(
                solph.Transformer(
                    label="car",
                    inputs={bfuel: solph.Flow()},
                    outputs={bkm: solph.Flow()},
                    conversion_factors={bkm: param_value["conversion_factor_car"]},
                )
            )

    ###################
    ### Storages    ###
    ###################

    # Electrical Storage
    if param_value["capacity_electr_storage"] > 0:
        storage_el = solph.components.GenericStorage(
            nominal_storage_capacity=(param_value["capacity_electr_storage"] * param_value["daily_demand_el"]),
            label="storage_el",
            inputs={
                bel: solph.Flow(
                    nominal_value=(
                        param_value["capacity_electr_storage"]
                        * param_value["daily_demand_el"]
                        / param_value["charge_time_storage_el"]
                    )
                )
            },
            outputs={
                bel: solph.Flow(
                    nominal_value=(
                        param_value["capacity_electr_storage"]
                        * param_value["daily_demand_el"]
                        / param_value["charge_time_storage_el"]
                    )
                )
            },
            loss_rate=param_value["capacity_loss_storage_el"],
            initial_storage_level=param_value["init_capacity_storage_el"],
            inflow_conversion_factor=param_value["inflow_conv_factor_storage_el"],
            outflow_conversion_factor=param_value["outflow_conv_factor_storage_el"],
        )
        energysystem.add(storage_el)

    # Thermal Storage
    if param_value["capacity_thermal_storage"] > 0:
        storage_th = solph.components.GenericStorage(
            nominal_storage_capacity=(param_value["capacity_thermal_storage"] * param_value["daily_demand_th"]),
            label="storage_th",
            inputs={
                bth: solph.Flow(
                    nominal_value=(
                        param_value["capacity_thermal_storage"]
                        * param_value["daily_demand_th"]
                        / param_value["charge_time_storage_th"]
                    )
                )
            },
            outputs={
                bth: solph.Flow(
                    nominal_value=(
                        param_value["capacity_thermal_storage"]
                        * param_value["daily_demand_th"]
                        / param_value["charge_time_storage_th"]
                    )
                )
            },
            loss_rate=param_value["capacity_loss_storage_th"],
            initial_storage_level=param_value["init_capacity_storage_th"],
            inflow_conversion_factor=param_value["inflow_conv_factor_storage_th"],
            outflow_conversion_factor=param_value["outflow_conv_factor_storage_th"],
        )
        energysystem.add(storage_th)

    if cfg["enable_mobility"]:
        # BEV-Storages
        storage_bev = solph.components.GenericStorage(
            nominal_storage_capacity=(
                param_value["capacity_bev_storage"] * param_value["vehicle"] * (param_value["percentage_of_bev"] / 100)
            ),
            label="storage_bev",
            inputs={bbev: solph.Flow()},
            outputs={bbev: solph.Flow()},
            loss_rate=0.00,
            initial_storage_level=param_value["init_capacity_storage_bev"],
            inflow_conversion_factor=1.0,
            outflow_conversion_factor=1.0,
        )
        energysystem.add(storage_bev)

    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info("Optimise the energy system")

    model = solph.Model(energysystem)

    if debug:
        filename = os.path.join(
            helpers.extend_basic_path("lp_files"), "model_team_{}.lp".format(cfg["team_names"][team_number])
        )
        logging.info("Store lp-file in {}.".format(filename))
        model.write(filename, io_options={"symbolic_solver_labels": True})

    # if tee_switch is true solver messages will be displayed
    logging.info("Solve the optimization problem of team {}".format(cfg["team_names"][team_number]))
    model.solve(solver=solver, solve_kwargs={"tee": solver_verbose})

    logging.info("Store the energy system with the results.")

    energysystem.results["main"] = solph.processing.results(model)
    energysystem.results["meta"] = solph.processing.meta_results(model)

    path = f"{abs_path}/{cfg['institution']}/{cfg['instructor']}/{cfg['schedule']}"
    dpath = path + "/results/data/dumps"
    os.makedirs(dpath, exist_ok=True)
    energysystem.dump(dpath=dpath, filename="model_team_{}.oemof".format(cfg["team_names"][team_number]))
