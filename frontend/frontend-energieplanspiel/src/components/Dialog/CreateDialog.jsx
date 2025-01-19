import React from "react";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import PeopleIcon from "@mui/icons-material/People";
import Typography from "@mui/material/Typography";
import AddIcon from "@mui/icons-material/Add";
import { DialogWrapper } from "../../styling/styled-components/Wrapper";
import { useState, useEffect } from "react";
import { IconButton, InputAdornment } from "@mui/material";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import Visibility from "@mui/icons-material/Visibility";
import dayjs from "dayjs";
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker';
import 'dayjs/locale/de';

function CreateDialog(props) {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [date, setDate] = useState(dayjs());
  const [label, setLabel] = useState("");
  const [errorName, setErrorName] = useState(false);
  const [errorPassword, setErrorPassword] = useState(false);


  useEffect(() => {
    if (props.role === "ADMIN"){
      switch (props.crumbType) {
        case 0:
          setLabel("Institution")
          break;
        case 1:
          setLabel("Instruktor")
          break;
        case 3:
          setLabel("Gruppe")
          break;
      }
    }else if (props.role === "INSTRUCTOR"){
      if(props.crumbType === 1){
        setLabel("Gruppe")
      }
    }
  }, [props.crumbType]);

  const handleDateChange = (newDate) => {
    setDate(newDate);
  };

  const handleNewEntry = () => {
    if (props.crumbType === 2 && props.role === "ADMIN"){
      const newEntry= { date: String(date.$y) + "-" + String(date.$M+1) + "-" + String(date.$D)};
      props.addNewEntry(newEntry);
      setErrorName(false)
      setErrorPassword(false)

    }else{
      if(props.crumbType === 0){
        if(name){
          const newEntry = { name: name, password: password };
          props.addNewEntry(newEntry);
          setErrorName(false)
        }else if(!name){
          setErrorName(true)
        }
      }else if(((props.crumbType ===1 || props.crumbType === 3) && props.role === "ADMIN") || (props.role === "INSTRUCTOR" && props.crumbType === 1)){
        if(name && password){
          const newEntry = { name: name, password: password };
          props.addNewEntry(newEntry);
          setErrorName(false)
          setErrorPassword(false)
        }
        if(!name || !password){
          setErrorName(true)
          setErrorPassword(true)
        }
        if(!name && password){
          setErrorName(true)
          setErrorPassword(false)
        }
        if(!password && name){
          setErrorPassword(true)
          setErrorName(false)
        }
      }


    }
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setErrorName(false)
    setErrorPassword(false)
    setOpen(false);
    setName("");
    setPassword("");
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
    setPassword(password);
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  return (
    <div>
      <Button
        variant="contained"
        startIcon={<AddIcon />}
        onClick={() => handleClickOpen()}
        disabled={props.disabled}
      >
        Hinzufügen
      </Button>
      {props.role === "ADMIN" && props.crumbType === 2 ? (
        <DialogWrapper
          open={open}
          onClose={handleClose}
          fullWidth
          maxWidth="sm"
        >
          <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale="de">
            <DesktopDatePicker
              inputFormat="YYYY-MM-DD"
              value={date}
              onChange={handleDateChange}
              renderInput={(params) => <TextField {...params} />}
            />
          </LocalizationProvider>
          <DialogActions>
            <Button onClick={handleClose}>Abbrechen</Button>
            <Button onClick={handleNewEntry}>Erstellen</Button>
          </DialogActions>
        </DialogWrapper>
      ) : (
        <DialogWrapper
          open={open}
          onClose={handleClose}
          fullWidth
          maxWidth="sm"
        >
          <DialogTitle>
            <PeopleIcon />
          </DialogTitle>
          <DialogContent>
            <TextField
              error={errorName}
              helperText={errorName ? "Sie haben keine Eingabe getätigt" : ""}
              autoFocus
              margin="dense"
              id="name"
              label={"Gebe einen Namen für " + label + " ein"}
              type="name"
              fullWidth={true}
              variant="standard"
              value={name}
              onChange={(e) => {
                setName(e.target.value);
              }}
            />
          </DialogContent>
          {(props.role === "ADMIN" &&
            (props.crumbType === 1 || props.crumbType === 3)) ||
          (props.role === "INSTRUCTOR" && props.crumbType === 1) ? (
            <DialogContent>
              <TextField
                error={errorPassword}
                helperText={errorPassword ? "Sie haben keine Eingabe getätigt" : ""}
                autoFocus
                margin="dense"
                id="password"
                label="Gebe ein Passwort ein"
                type={showPassword ? "text" : "password"}
                fullWidth={true}
                variant="standard"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                }}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        aria-label="toggle password visibility"
                        onClick={handleClickShowPassword}
                        onMouseDown={handleMouseDownPassword}
                        edge="start"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />
            </DialogContent>
          ) : (
            ""
          )}
          <DialogActions>
            <Button onClick={handleClose}>Abbrechen</Button>
            <Button onClick={handleNewEntry}>Erstellen</Button>
          </DialogActions>
        </DialogWrapper>
      )}
    </div>
  );
}

export default CreateDialog;
