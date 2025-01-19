import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

export default function GroupSumbitDialog(props) {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = () => {
    setOpen(true);

  };

  const handleCloseBySubmit = () => {
    setOpen(false);
    props.handleSubmit();
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
        <Button disabled={props.disable} variant="contained" onClick={() => handleClickOpen()}>
          Abgeben
        </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Abgabe</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Sind Sie sich sicher das Sie abgeben wollen? Änderungen können danach nicht mehr durchgeführt werden.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Zurück</Button>
          <Button onClick={handleCloseBySubmit}>Abgeben</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}