import {
  MainContentButtonsWrapper,
  MainContentWrapper,
  SearchListWrapper,
} from "../../styling/styled-components/Wrapper";
import { ListComponent } from "../ListComponent";
import TextField from "@mui/material/TextField";
import { StyledSearchTextField } from "../../styling/styled-components/StyledTextField";
import React, { useState, useEffect, useRef } from "react";
import BreadCrumbs from "../BreadCrumbs";
import { Button } from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import CreateDialog from "../Dialog/CreateDialog";
import EditDialog from "../Dialog/EditDialog";
import {
  fetchGroups,
  fetchProgress,
  fetchSchedule,
} from "../../Requests/GetRequests";
import { addGroup, startCalc } from "../../Requests/PostRequests";
import { deleteGroup } from "../../Requests/DeleteRequests";
import { ResultsContent } from "./ResultsContent";
import ProgressBar from "../ProgressBar";
import AlertBar from "../AlertBar";
import { editGroup } from "../../Requests/PutRequest";

export const InstructorContent = (props) => {
  const [filteredList, setFilteredList] = useState([]);
  const [list, setList] = useState([]);
  const [searchInput, setSearchInput] = useState("");
  const [crumbType, setCrumbType] = useState(0);
  const [crumbs, setCrumbs] = useState(["Termine", "Gruppe", "Ergebnisse"]);
  const [open, setOpen] = useState(false);
  const [openEdit, setOpenEdit] = useState(false);
  const [editData, setEditData] = useState({});
  const [calcButtonDisabled, setCalcButtonDisabled] = useState(false);
  const [resultsButtonDisabled, setResultsButtonDisabled] = useState(false);
  const [idHistory, setIdHistory] = useState([]);
  const [fetchError, setFetchError] = useState(-1);
  const [message, setMessage] = useState("");
  const [user, setUser] = useState("");
  const [calcRunning, setCalcRunning] = useState(false);
  const [runningSchedule, setRunningSchedule] = useState(null);
  const [progress, setProgress] = useState(0.0);
  const progressIntervalId = useRef(null);

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user"));
    setUser(user.user);
  }, []);

  useEffect(() => {
    user &&
      fetchSchedule(user).then((response) => {
        setFetchError(response.status);
      if(response.status !== -1){
        setMessage(response.message);
      }
        setList(response.data);
        setFilteredList([]);
        setIdHistory([user]);
      });
  }, [user]);

  useEffect(() => {
    if (crumbType === 1) {
      setCalcRunning((list.length !== 0) && list.every((groups) => groups.calc_running));
      setCalcButtonDisabled((list.length !== 0) && list.every((groups) => groups.has_submitted));
      setResultsButtonDisabled((list.length !== 0) && list.every((groups) => groups.results_exist));
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
    if (calcRunning && (idHistory[1] === runningSchedule) && !progressIntervalId.current) {
      progressIntervalId.current = setInterval(() => {
        if (calcRunning && (idHistory[1] === runningSchedule)) {
          fetchProgress(idHistory[1]).then((response) => {
            setFetchError(response.status);
            if(response.status === 1){
              setMessage(response.message);
            }
            if(response.status !== 1) {
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
    startCalc(idHistory[1]).then((response) => {
      setFetchError(response.status);
      setMessage(response.message);
    });
    if (fetchError !== 1) {
      setCalcRunning(true);
      setRunningSchedule(idHistory[1]);
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

  const handleCloseDialog = () => {
    setOpen(false);
  };

  const editEntry = (entryToEdit) => {
    switch (crumbType) {
      case 1:
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
      case 1:
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
      case 1:
        addGroup(newEntry, idHistory[1]).then((response) => {
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
        idHistory[0] &&
          fetchSchedule(idHistory[0]).then((response) => {
            setFetchError(response.status);
          if(response.status !== -1){
            setMessage(response.message);
          }
            setList(response.data);
          });
        break;
      case 1:
        idHistory[1] &&
          fetchGroups(idHistory[1]).then((response) => {
            setFetchError(response.status);
            if(response.status !== -1){
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
      if (crumbType != 2) {
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
      {crumbType === 2 ? (
        <MainContentWrapper height={"none"}>
          <BreadCrumbs
            handleCrumbChange={handleCrumbChange}
            crumbType={crumbType}
            crumbs={crumbs}
          ></BreadCrumbs>

          <ResultsContent id={idHistory[1]} setError={setFetchError} setMessage={setMessage}></ResultsContent>
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
              maxCrumbs={1}
              role={"INSTRUCTOR"}
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

          {crumbType === 1 ? (
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
                role={"INSTRUCTOR"}
                addNewEntry={addNewEntry}
                open={open}
                crumbType={crumbType}
                disabled={calcRunning}
              />
            </MainContentButtonsWrapper>
          ) : (
            ""
          )}

          <EditDialog
            open={openEdit}
            role={"INSTRUCTOR"}
            crumbType={crumbType}
            setOpenEdit={setOpenEdit}
            editData={editData}
            editEntry={editEntry}
          ></EditDialog>

          {calcRunning === true && crumbType === 1 && (idHistory[1] === runningSchedule) ? (
            <ProgressBar progress={progress}></ProgressBar>
          ) : (
            ""
          )}
        </MainContentWrapper>
      )}
      <AlertBar error={fetchError} setError={setFetchError} message={message}></AlertBar>
    </React.Fragment>
  )
};
