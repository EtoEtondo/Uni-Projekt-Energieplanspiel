import TextField from '@mui/material/TextField';
import styled from 'styled-components';
import FormControl from '@mui/material/FormControl';
export const StyledTextField = styled(TextField)`
  .MuiFormHelperText-root {
    height: 15px;
  }
  & .MuiInputBase-root {
    width: auto;
    margin-bottom: 0px;
  }
  //HEADER TEXT
  & .MuiFormLabel-root {
  }
  & label.Mui-focused {
    color: #1976d2;
  }
  & .MuiInput-underline:after {
    border-bottom-color: grey;
  }

  // Inhalt Text Eingabe default
  & .MuiOutlinedInput-root {
    color: grey;
    padding: 0px;
    & fieldset {
      // Rahmen farbe definiern
      border-color: grey;
    }
    &:hover fieldset {
      border-color: #1976d2;
      color: #1976d2;
    }
    &.Mui-focused fieldset {
      border-color: 1976d2;
    }
  }
`;

export const StyledSearchTextField = styled(TextField)`
  .MuiFormHelperText-root {
    height: 15px;
  }
  & .MuiInputBase-root {
    width: 100%;
    margin-top: 0px;
    margon-bottom: 0px;
  }
  //HEADER TEXT
  & .MuiFormLabel-root {
  }
  & label.Mui-focused {
    color: #1976d2;
  }
  & .MuiInput-underline:after {
    border-bottom-color: grey;
  }

  // Inhalt Text Eingabe default
  & .MuiOutlinedInput-root {
    color: grey;
    padding: 0px;
    & fieldset {
      // Rahmen farbe definiern
      border-color: grey;
    }
    &:hover fieldset {
      border-color: #1976d2;
      color: #1976d2;
    }
    &.Mui-focused fieldset {
      border-color: 1976d2;
    }
  }
`;

export const TextFieldsWrapper = styled.div`
  height: 50%;
  width: 300px;
  display: flex;
  align-items: stretch;
  flex-direction: column;
  justify-content: space-evenly;
`;


export const TextFieldIconWrapper = styled(FormControl)``;
