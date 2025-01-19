import {
  MainContentButtonsWrapper,
  MainContentWrapper,
  SearchListWrapper,
} from "../../styling/styled-components/Wrapper";
import { ListComponent } from "./../ListComponent";
import TextField from "@mui/material/TextField";
import { StyledSearchTextField } from "../../styling/styled-components/StyledTextField";
import React, { useState, useEffect, useRef } from "react";
import BreadCrumbs from "../BreadCrumbs";
import { Button } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CreateDialog from "../Dialog/CreateDialog";
import EditDialog from "../Dialog/EditDialog";
import CircularProgress from "@mui/material/CircularProgress";
import LinearProgress from "@mui/material/LinearProgress";
import {
  fetchGroups,
  fetchInstitutions,
  fetchInstructors,
  fetchProgress,
  fetchSchedule,
} from "../../Requests/GetRequests";
import {
  addGroup,
  addInstitution,
  addInstructor,
  addSchedule,
  startCalc,
} from "../../Requests/PostRequests";
import {
  deleteGroup,
  deleteInstitution,
  deleteInstructor,
  deleteSchedule,
} from "../../Requests/DeleteRequests";
import { editGroup, editInstructor } from "../../Requests/PutRequest";
import ProgressBar from "../ProgressBar";
import { ResultsContent } from "./ResultsContent";
import AlertBar from "../AlertBar";

const defaultList = [];

export const AdminContent = (props) => {
  const [filteredList, setFilteredList] = useState([]);
  const [searchInput, setSearchInput] = useState("");
  const [list, setList] = useState([...defaultList]);
  const [crumbType, setCrumbType] = useState(0);
  const [crumbs, setCrumbs] = useState([
    "Institution",
    "Instruktor",
    "Termine",
    "Gruppe",
    "Ergebnisse",
  ]);
  const [openEdit, setOpenEdit] = useState(false);
  const [editData, setEditData] = useState({});
  const [open, setOpen] = useState(false);
  const [calcButtonDisabled, setCalcButtonDisabled] = useState(false);
  const [resultsButtonDisabled, setResultsButtonDisabled] = useState(false);
  const [idHistory, setIdHistory] = useState([]);
  const [fetchError, setFetchError] = useState(-1);
  const [message, setMessage] = useState("");
  const [calcRunning, setCalcRunning] = useState(false);
  const [runningSchedule, setRunningSchedule] = useState(null);
  const [progress, setProgress] = useState(0.0);
  const progressIntervalId = useRef(null);

  useEffect(() => {
    fetchInstitutions().then((response) => {
      setFetchError(response.status);
      if (response.status !== -1) {
        setMessage(response.message);
      }
      setList(response.data);
      setFilteredList([]);
    });
  }, []);

  useEffect(() => {
    if (crumbType === 3) {
      setCalcRunning(
        list.length !== 0 && list.every((groups) => groups.calc_running)
      );
      setCalcButtonDisabled(
        list.length !== 0 && list.every((groups) => groups.has_submitted)
      );
      setResultsButtonDisabled(
        list.length !== 0 && list.every((groups) => groups.results_exist)
      );
    }
    handleSearchInput(searchInput);
  }, [crumbType, list]);

  useEffect(() => {
    switchCaseCrumbs(crumbType);
    const id = setInterval(() => {
      switchCaseCrumbs(crumbType);
    }, 5000);

    return () => clearInterval(id);
  }, [crumbType]);

  useEffect(() => {
    if (
      calcRunning &&
      idHistory[2] === runningSchedule &&
      !progressIntervalId.current
    ) {
      progressIntervalId.current = setInterval(() => {
        if (calcRunning && idHistory[2] === runningSchedule) {
          fetchProgress(idHistory[2]).then((response) => {
            setFetchError(response.status);
            if (response.status === 1) {
              setMessage(response.message);
            }
            if (response.status !== 1) {
              setProgress(response.data.progress);
            }
            if (response.status === 1 || response.data.progress === 1) {
              setCalcRunning(false);
              setProgress(0);
              clearTimeout(progressIntervalId.current);
              progressIntervalId.current = null;
              setResultsButtonDisabled(true);
              setRunningSchedule(null);
            }
          });
        }
      }, 5000);
    }
  }, [calcRunning]);

  const beginCalc = () => {
    startCalc(idHistory[2]).then((response) => {
      setFetchError(response.status);
      setMessage(response.message);
    });
    if (fetchError !== 1) {
      setCalcRunning(true);
      setRunningSchedule(idHistory[2]);
    }
  };

  const viewResults = () => {
    setCrumbType(crumbType + 1);
  };

  const handleClickOpenEditDialog = (openEdit, index) => {
    if (filteredList.length === 0) {
      setEditData(list[index]);
    } else {
      setEditData(filteredList[index]);
    }
    setOpenEdit(openEdit);
  };

  const handleClickOpenDialog = (mode) => {
    setOpen(true);
    setDialogMode(mode);
  };

  const handleCloseDialog = () => {
    setOpen(false);
  };

  const editEntry = (entryToEdit) => {
    switch (crumbType) {
      case 1:
        editInstructor(entryToEdit).then((response) => {
          setFetchError(response.status);
          setMessage(response.message);
          switchCaseCrumbs(crumbType);
        });
        break;
      case 3:
        editGroup(entryToEdit).then((response) => {
          setFetchError(response.status);
          setMessage(response.message);
          switchCaseCrumbs(crumbType);
        });
        break;
    }
  };

  const deleteEntry = (entryToDelete) => {
    switch (crumbType) {
      case 0:
        deleteInstitution(entryToDelete.id).then((response) => {
          setFetchError(response.status);
          setMessage(response.message);
          switchCaseCrumbs(crumbType);
        });
        break;
      case 1:
        deleteInstructor(entryToDelete.username, idHistory[0]).then(
          (response) => {
            setFetchError(response.status);
            setMessage(response.message);
            switchCaseCrumbs(crumbType);
          }
        );
        break;
      case 2:
        deleteSchedule(entryToDelete.id).then((response) => {
          setFetchError(response.status);
          setMessage(response.message);
          switchCaseCrumbs(crumbType);
        });
        break;
      case 3:
        deleteGroup(entryToDelete.username).then((response) => {
          setFetchError(response.status);
          setMessage(response.message);
          switchCaseCrumbs(crumbType);
        });
        break;
    }
  };

  const addNewEntry = (newEntry) => {
    switch (crumbType) {
      case 0:
        addInstitution(newEntry.name).then((response) => {
          setFetchError(response.status);
          setMessage(response.message);
          switchCaseCrumbs(crumbType);
        });
        break;
      case 1:
        addInstructor(newEntry, idHistory[0]).then((response) => {
          setFetchError(response.status);
          setMessage(response.message);
          switchCaseCrumbs(crumbType);
        });
        break;
      case 2:
        addSchedule(newEntry.date, idHistory[1]).then((response) => {
          setFetchError(response.status);
          setMessage(response.message);
          switchCaseCrumbs(crumbType);
        });
        break;
      case 3:
        addGroup(newEntry, idHistory[2]).then((response) => {
          setFetchError(response.status);
          setMessage(response.message);
          switchCaseCrumbs(crumbType);
        });
        break;
    }
  };

  const switchCaseCrumbs = (crumbType) => {
    switch (crumbType) {
      case 0:
        fetchInstitutions().then((response) => {
          setFetchError(response.status);
          if (response.status !== -1) {
            setMessage(response.message);
          }
          setList(response.data);
        });
        break;
      case 1:
        idHistory[0] &&
          fetchInstructors(idHistory[0]).then((response) => {
            setFetchError(response.status);
            if (response.status !== -1) {
              setMessage(response.message);
            }
            setList(response.data);
          });
        break;
      case 2:
        idHistory[1] &&
          fetchSchedule(idHistory[1]).then((response) => {
            setFetchError(response.status);
            if (response.status !== -1) {
              setMessage(response.message);
            }
            setList(response.data);
          });
        break;
      case 3:
        idHistory[2] &&
          fetchGroups(idHistory[2]).then((response) => {
            setFetchError(response.status);
            if (response.status !== -1) {
              setMessage(response.message);
            }
            setList(response.data);
          });
        break;
    }
  };

  const handleCrumbChange = (newCrumbType) => {
    if (newCrumbType !== crumbType) {
      setCrumbType(newCrumbType);
      if (crumbType != 4) {
        const newIdHistory = [...idHistory];
        const lengthToDelete = crumbType - newCrumbType;
        for (var i = 0; i < lengthToDelete; i++) {
          newIdHistory.pop();
        }
        setIdHistory(newIdHistory);
      }
      setFilteredList([]);
      setSearchInput("");
    }
  };

  const goToNextCrumbOnListElementClick = (newCrumbType, element) => {
    setCrumbType(newCrumbType);
    if (newCrumbType === 2) {
      setIdHistory([...idHistory, element.username]);
    } else {
      setIdHistory([...idHistory, element.id]);
    }
    setFilteredList([]);
    setSearchInput("");
  };

  const handleSearchInput = (searchInput) => {
    setSearchInput(searchInput)
    const tmpList = [];
    list.map((element, index) => {
      if (element.name.toLowerCase().includes(searchInput.toLowerCase())) {
        tmpList.push(element);
      }
    });
    setFilteredList(tmpList);
  };

  return (
    <React.Fragment>
      {crumbType === 4 ? (
        <MainContentWrapper height={"none"}>
          <BreadCrumbs
            handleCrumbChange={handleCrumbChange}
            crumbType={crumbType}
            crumbs={crumbs}
          ></BreadCrumbs>

          <ResultsContent
            id={idHistory[2]}
            setError={setFetchError}
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

          <SearchListWrapper>
            <StyledSearchTextField
              id="outlined-basic"
              label="Suche"
              variant="outlined"
              value={searchInput}
              onChange={(e) => handleSearchInput(e.target.value)}
            />
            <ListComponent
              maxCrumbs={3}
              role={"ADMIN"}
              handleClickOpenEditDialog={handleClickOpenEditDialog}
              currentList={
                filteredList.length > 0 || searchInput != ""
                  ? filteredList
                  : list
              }
              crumbType={crumbType}
              crumbsLength={crumbs.length}
              goToNextCrumbOnListElementClick={goToNextCrumbOnListElementClick}
              deleteEntry={deleteEntry}
            ></ListComponent>
          </SearchListWrapper>

          {crumbType === 3 ? (
            <MainContentButtonsWrapper>
              <Button
                disabled={!resultsButtonDisabled || calcRunning}
                variant="contained"
                onClick={() => viewResults()}
              >
                Ergebnisse einsehen
              </Button>

              <Button
                disabled={!calcButtonDisabled || calcRunning}
                variant="contained"
                onClick={() => beginCalc()}
              >
                Berechnung starten
              </Button>

              <CreateDialog
                role={"ADMIN"}
                addNewEntry={addNewEntry}
                open={open}
                crumbType={crumbType}
                disabled={calcRunning}
              />
            </MainContentButtonsWrapper>
          ) : (
            <MainContentButtonsWrapper>
              <CreateDialog
                role={"ADMIN"}
                addNewEntry={addNewEntry}
                open={open}
                crumbType={crumbType}
              />
            </MainContentButtonsWrapper>
          )}

          <EditDialog
            open={openEdit}
            role={"ADMIN"}
            crumbType={crumbType}
            setOpenEdit={setOpenEdit}
            editData={editData}
            editEntry={editEntry}
          ></EditDialog>

          {calcRunning === true &&
          crumbType === 3 &&
          idHistory[2] === runningSchedule ? (
            <ProgressBar progress={progress}></ProgressBar>
          ) : (
            ""
          )}
        </MainContentWrapper>
      )}
      <AlertBar
        error={fetchError}
        setError={setFetchError}
        message={message}
      ></AlertBar>
    </React.Fragment>
  );
};
