import {
  Button,
  FormControl,
  FormHelperText,
  Grid,
  InputLabel,
  MenuItem,
  TextField,
  Tooltip,
} from "@mui/material";
import { Box } from "@mui/system";
import React, { useState, useEffect } from "react";
import { StyledTextField } from "../../styling/styled-components/StyledTextField";
import {
  GridWrapper,
  GroupInputsWrapper,
  GroupsTextfield,
  MainContentButtonsWrapper,
  MainContentWrapper,
} from "../../styling/styled-components/Wrapper";
import { GroupInputField } from "../TextBox/GroupInputField";
import Select from "@mui/material/Select";
import GroupSumbitDialog from "../Dialog/GroupSubmitDialog";
import { submitResults } from "../../Requests/PostRequests";
import { fetchInfo } from "../../Requests/GetRequests";
import BreadCrumbs from "../BreadCrumbs";
import { ResultsContent } from "./ResultsContent";
import AlertBar from "../AlertBar";

export const GroupContent = () => {
  const [open, setOpen] = useState(false);
  const [crumbType, setCrumbType] = useState(0);
  const [crumbs, setCrumbs] = useState(["Eingaben", "Ergebnisse"]);
  const [inputList, setInputList] = useState([
    "number_of_windturbines",
    "number_of_chps",
    "number_of_boilers",
    "number_of_PV_pp",
    "number_of_heat_pumps",
    "area_PV",
    "area_solar_th",
    "capacity_electr_storage",
    "capacity_thermal_storage",
    "feature_building_retrofit",
    "percentage_of_bev",
  ]);

  const [windturbinesValue, setWindturbinesValue] = useState(0);
  const [chpsValue, setChpsValue] = useState(0);
  const [boilersValue, setBoilersValue] = useState(0);
  const [pv_ppValue, setPv_ppValue] = useState(0);
  const [heat_pumpsValue, setHeat_pumpsValue] = useState(0);
  const [capacity_electr_storageValue, setCapacity_electr_storageValue] =
    useState(0);
  const [capacity_thermal_storageValue, setCapacity_thermal_storageValue] =
    useState(0);
  const [feature_building_retrofitValue, setFeature_building_retrofitValue] =
    useState(0);
  const [percentage_of_bevValue, setPercentage_of_bevValue] = useState(0);
  const [area_pvValue, setArea_pvValue] = useState(0);
  const [area_solar_thValue, setArea_solar_thValue] = useState(0);
  const [disableSubmit, setDisableSubmit] = useState(false);
  const [resultAccess, setResultAccess] = useState(false);
  const [error, setError] = useState(-1);
  const [message, setMessage] = useState("");

  useEffect(() => {}, [windturbinesValue]);

  const viewResults = () => {
    setCrumbType(crumbType + 1);
  };

  const handleCrumbChange = (newCrumbType) => {
    if (newCrumbType !== crumbType) {
      setCrumbType(newCrumbType);
    }
  };

  const handleSelect = (event, id) => {
    if (id === "capacity_thermal_storage-select") {
      setCapacity_thermal_storageValue(event.target.value);
    } else if (id === "capacity_electr_storage-select") {
      setCapacity_electr_storageValue(event.target.value);
    }
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  useEffect(() => {
    fetchInfo().then((response) => {
      setDisableSubmit(
        response.data[Object.keys(response.data)[0]].has_submitted
      );
      setResultAccess(
        response.data[Object.keys(response.data)[0]].result_access
      );
    });
    const id = setInterval(() => {
      fetchInfo().then((response) => {
        setDisableSubmit(
          response.data[Object.keys(response.data)[0]].has_submitted
        );
        setResultAccess(
          response.data[Object.keys(response.data)[0]].result_access
        );
      });
    }, 2000);

    return () => clearInterval(id);
  }, []);

  const handleSubmit = () => {
    const inputValues = [
      windturbinesValue,
      chpsValue,
      boilersValue,
      pv_ppValue,
      heat_pumpsValue,
      capacity_electr_storageValue,
      capacity_thermal_storageValue,
      feature_building_retrofitValue,
      percentage_of_bevValue,
      area_pvValue,
      area_solar_thValue,
    ];
    if (inputValues.includes("")) {
      setError(1);
      setMessage("Nicht alle Eingaben wurden getätigt.");
    } else {
      const result =
        parseInt(area_pvValue, 10) + parseInt(area_solar_thValue, 10);
      if (result <= 100) {
        const data = {};
        for (var i = 0; i < inputList.length; ++i)
          data[inputList[i]] = parseFloat(inputValues[i], 10);

        submitResults(data).then((response) => {
          setError(response.status);
          setMessage(response.message);
        });
      } else {
        setError(1);
        setMessage(
          "Folgende Randbedingung wurde nicht erfüllt: Bereich_PV + Bereich_solar_th <=100."
        );
      }
    }
  };

  return (
    <React.Fragment>
      {crumbType === 1 ? (
        <MainContentWrapper height={"none"}>
          <BreadCrumbs
            handleCrumbChange={handleCrumbChange}
            crumbType={crumbType}
            crumbs={crumbs}
          ></BreadCrumbs>
          <ResultsContent
            role={"GROUP"}
            id={null}
            setError={setError}
            setMessage={setMessage}
          ></ResultsContent>
        </MainContentWrapper>
      ) : (
        <MainContentWrapper height={"80%"}>
          <BreadCrumbs
            handleCrumbChange={handleCrumbChange}
            crumbType={crumbType}
            crumbs={crumbs}
          ></BreadCrumbs>
          <GroupInputsWrapper>
            <GridWrapper
              display="grid"
              gridTemplateColumns="repeat(12, 1fr)"
              gap={10}
            >
              <Tooltip title="Anzahl der Windenergieanlagen (WEA)" arrow>
                <Box gridColumn="span 3">
                  <GroupInputField
                    functionVariation={0}
                    label={"Anzahl der Windenergieanlagen (WEA)"}
                    tip={"Wertebereich: 0-10"}
                    setState={setWindturbinesValue}
                  />
                </Box>
              </Tooltip>

              <Tooltip title="Anzahl der Blockheizkraftwerke (BHKW)" arrow>
                <Box gridColumn="span 3">
                  <GroupInputField
                    functionVariation={0}
                    label={"Anzahl der Blockheizkraftwerke (BHKW)"}
                    tip={"Wertebereich: 0-10"}
                    setState={setChpsValue}
                  />
                </Box>
              </Tooltip>

              <Tooltip title="Anzahl der Heizkessel" arrow>
                <Box gridColumn="span 3">
                  <GroupInputField
                    functionVariation={0}
                    label={"Anzahl der Heizkessel"}
                    tip={"Wertebereich: 0-10"}
                    setState={setBoilersValue}
                  />
                </Box>
              </Tooltip>

              <Tooltip
                title="Photovoltaik Freiflächenanlage (Ja = 1; Nein = 0)"
                arrow
              >
                <Box gridColumn="span 3">
                  <GroupInputField
                    functionVariation={1}
                    label={"Photovoltaik Freiflächenanlage (Ja = 1; Nein = 0)"}
                    tip={"Wertebereich: 0-1"}
                    setState={setPv_ppValue}
                  />
                </Box>
              </Tooltip>

              <Tooltip
                title="Anzahl der Wärmepumpen"
                arrow
              >
                <Box gridColumn="span 3">
                  <GroupInputField
                    functionVariation={0}
                    label={"Anzahl der Wärmepumpen"}
                    tip={"Wertebereich: 0-10"}
                    setState={setHeat_pumpsValue}
                  />
                </Box>
              </Tooltip>

              <Tooltip
                title="Kapazität des Stromspeichers (1 =  1 mittlerer Tagesbedarf)"
                arrow
                placement="top-start"
              >
                <Box gridColumn="span 3">
                  <FormControl fullWidth>
                    <InputLabel>
                      Kapazität des Stromspeichers (1 = 1 mittlerer Tagesbedarf)
                    </InputLabel>
                    <Select
                      id="capacity_electr_storage-select"
                      value={capacity_electr_storageValue}
                      label="Kapazität des Stromspeichers (1 =  1 mittlerer Tagesbedarf)"
                      onChange={(e) =>
                        handleSelect(e, "capacity_electr_storage-select")
                      }
                    >
                      <MenuItem value={0}>0</MenuItem>
                      <MenuItem value={0.25}>0.25</MenuItem>
                      <MenuItem value={0.5}>0.5</MenuItem>
                      <MenuItem value={1}>1</MenuItem>
                      <MenuItem value={2}>2</MenuItem>
                      <MenuItem value={7}>7</MenuItem>
                    </Select>
                    <FormHelperText>
                      Wertebereich: 0; 0,25; 0,5; 1; 2; 7
                    </FormHelperText>
                  </FormControl>
                </Box>
              </Tooltip>

              <Tooltip
                title="Kapazität des Wärmepspeichers (1 =  1 mittlerer Tagesbedarf)"
                arrow
                placement="top-start"
              >
                <Box gridColumn="span 3">
                  <FormControl fullWidth>
                    <InputLabel>
                      Kapazität des Wärmepspeichers (1 = 1 mittlerer
                      Tagesbedarf)
                    </InputLabel>
                    <Select
                      id="capacity_thermal_storage-select"
                      value={capacity_thermal_storageValue}
                      label="Kapazität des Wärmepspeichers (1 =  1 mittlerer Tagesbedarf)"
                      onChange={(e) =>
                        handleSelect(e, "capacity_thermal_storage-select")
                      }
                    >
                      <MenuItem value={0}>0</MenuItem>
                      <MenuItem value={0.25}>0.25</MenuItem>
                      <MenuItem value={0.5}>0.5</MenuItem>
                      <MenuItem value={1}>1</MenuItem>
                      <MenuItem value={2}>2</MenuItem>
                      <MenuItem value={7}>7</MenuItem>
                      <MenuItem value={30}>30</MenuItem>
                      <MenuItem value={90}>90</MenuItem>
                    </Select>
                    <FormHelperText>
                      Wertebereich: 0; 0,25; 0,5; 1; 2; 7; 30; 90
                    </FormHelperText>
                  </FormControl>
                </Box>
              </Tooltip>

              <Tooltip
                title="Reduzierung Wärmebedarf für Gebäudebeheizung durch Sanierungsmaßnahmen (in %)"
                arrow
              >
                <Box gridColumn="span 3">
                  <GroupInputField
                    functionVariation={5}
                    label={
                      "Reduzierung Wärmebedarf für Gebäudebeheizung durch Sanierungsmaßnahmen (in %)"
                    }
                    tip={"Wertebereich: 0-50"}
                    setState={setFeature_building_retrofitValue}
                  />
                </Box>
              </Tooltip>

              <Tooltip title="Anteil Elektromobilität (in %)" arrow>
                <Box gridColumn="span 3">
                  <GroupInputField
                    functionVariation={6}
                    label={"Anteil Elektromobilität (in %)"}
                    tip={"Wertebereich: 0-100"}
                    setState={setPercentage_of_bevValue}
                  />
                </Box>
              </Tooltip>

              <Tooltip
                title="Anteil der für Photovoltaik genutzten Dachfläche (in %)"
                arrow
              >
                <Box gridColumn="span 3">
                  <GroupInputField
                    functionVariation={6}
                    label={
                      "Anteil der für Photovoltaik genutzten Dachfläche (in %)"
                    }
                    tip={"Wertebereich: 0-100"}
                    setState={setArea_pvValue}
                  />
                </Box>
              </Tooltip>

              <Tooltip
                title="Anteil der für Solarthermie genutzten Dachfläche (in %)"
                arrow
              >
                <Box gridColumn="span 3">
                  <GroupInputField
                    functionVariation={6}
                    label={
                      "Anteil der für Solarthermie genutzten Dachfläche (in %)"
                    }
                    tip={"Wertebereich: 0-100"}
                    setState={setArea_solar_thValue}
                  />
                </Box>
              </Tooltip>
            </GridWrapper>
          </GroupInputsWrapper>
          <MainContentButtonsWrapper>
            <Button
              disabled={!resultAccess}
              variant="contained"
              onClick={() => viewResults()}
            >
              Ergebnisse einsehen
            </Button>
            <GroupSumbitDialog
              disable={disableSubmit}
              handleSubmit={handleSubmit}
            ></GroupSumbitDialog>
          </MainContentButtonsWrapper>
        </MainContentWrapper>
      )}
      <AlertBar error={error} setError={setError} message={message}></AlertBar>
    </React.Fragment>
  );
};
