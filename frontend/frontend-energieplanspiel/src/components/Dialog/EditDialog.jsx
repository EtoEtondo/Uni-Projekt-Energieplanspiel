import { useState, useEffect } from "react";
import * as React from "react";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import { IconButton, InputAdornment } from "@mui/material";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import Visibility from "@mui/icons-material/Visibility";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";

export default function EditDialog(props) {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [accountEnable, setAccountEnable] = useState(false);
  const [error, setError] = useState(false);

  useEffect(() => {
    setValue(""); // Je nachdem was wir für Password vom backend bekommen muss es gehandlet werden
    setAccountEnable(props.editData["enabled"]);
  }, [props.editData]);

  useEffect(() => {
    setOpen(props.open);
  }, [props.open]);

  const handleClose = () => {
    props.setOpenEdit(false);
    setValue("");
    setError(false);
  };

  const handleSubmit = () => {
    if (value) {
      props.editData["password"] = value;
      setError(false);
    }

    if (props.editData["enabled"] !== accountEnable) {
      props.editData["enabled"] = accountEnable;
    }
    props.editEntry(props.editData);
  };

  const handleCheck = (event) => {
    setAccountEnable(event.target.checked);
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
    setValue(value);
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  return (
    <div>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Bearbeiten - Wollen Sie Änderungen vornehmen?</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Anmeldename: {props.editData["username"]}
          </DialogContentText>

          {props.role === "ADMIN" && props.crumbType === 1 ? (
            <FormControlLabel
              control={
                <Checkbox
                  defaultChecked={accountEnable}
                  onChange={(e) => handleCheck(e)}
                />
              }
              label="Account aktiv"
            />
          ) : (props.role === "ADMIN" && props.crumbType === 3) ||
            (props.role === "INSTRUCTOR" && props.crumbType === 1) ? (
            <DialogContentText>
              Acount-Status:
              {props.editData["enabled"] === true ? " aktiv" : " deaktiviert"}
            </DialogContentText>
          ) : (
            ""
          )}
          <TextField
            autoFocus
            margin="dense"
            error={error}
            helperText={error ? "Es wurde kein Passwort eingegeben" : ""}
            id="name"
            label={"Passwort"}
            type={showPassword ? "text" : "password"}
            value={value}
            fullWidth
            variant="standard"
            onChange={(e) => setValue(e.target.value)}
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
        <DialogActions>
          <Button onClick={handleClose}>Zurück</Button>
          <Button onClick={handleSubmit}>Speichern</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
