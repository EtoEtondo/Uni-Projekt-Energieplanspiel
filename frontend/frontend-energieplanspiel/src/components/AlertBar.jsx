import React, { useState, useEffect } from "react";
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

export default function AlertBar(props) {
  const [open, setOpen] = React.useState(false);
  const [severityType, setSeverityType] = React.useState("error");


  useEffect(() => {
    if(props.error === 1){
      setOpen(true)
      setSeverityType("error")
    }else if(props.error === 0){
      setOpen(true)
      setSeverityType("success")
    }
    props.setError(-1)
  }, [props.error, props.success]);


  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpen(false);
  };

  return (
      <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
        <Alert onClose={handleClose} severity={severityType} sx={{ width: '100%' }}>
          {props.message}
        </Alert>
      </Snackbar>
  );
}