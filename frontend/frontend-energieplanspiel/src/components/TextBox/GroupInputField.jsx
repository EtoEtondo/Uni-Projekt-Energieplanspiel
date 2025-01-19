import React, { useContext, useEffect, useState } from 'react';
import { StyledTextField, TextFieldsWrapper } from '../../styling/styled-components/StyledTextField';
import { arrayDataChangeHandler, convertStringToNumber0, convertStringToNumber1, convertStringToNumber5, convertStringToNumber6,  } from './HelperFunction';


export const GroupInputField = ({functionVariation, label, tip, setState}) => {
  const [value, setValue] = useState("0");
  const [inputProps, setInputProps] = useState({
    helperText: tip,
  });

  useEffect(() => {
    setState(value)
  }, [value])

  return (
    <StyledTextField
      {...inputProps}
      variant="outlined"
      label={label}
      value={value}
      autoComplete="off"
      onChange={(event) => {
        switch(functionVariation) {
            case 0:
                convertStringToNumber0(event.target.value, setInputProps, setValue, tip)
                break
            case 1:
                convertStringToNumber1(event.target.value, setInputProps, setValue, tip)
                break
            case 5:
                convertStringToNumber5(event.target.value, setInputProps, setValue, tip)
                break
            case 6:
                convertStringToNumber6(event.target.value, setInputProps, setValue, tip)
                break
            default:
                convertStringToNumber0(event.target.value, setInputProps, setValue, tip)
                break
          }
        
      }}
    />
  );
};

export const InputTextFieldsContainer = ({ children }) => {
  return <TextFieldsWrapper>{children}</TextFieldsWrapper>
};