export const arrayDataChangeHandler = (
    value,
    setArrayInput,
    dispatchContext,
    setInputProps
  ) => {
    //setArrayInput(arrayString);
    const arrayString = convertStringToNumber(value, setInputProps);
    dispatchContext.dispatchControl({
      type: 'CONTROL_INPUT_FIELD_SET_LIST',
      list: array,
    });
  };
  
  export const convertStringToNumber0 = (string, setInputProps, setValue, tip) => {

    string = string.replaceAll(/[^-{1}+0-9,\s]/g, '');
    string = string.replaceAll(/-/g, '');
    string = string.replace('+', '');
    string = string.replaceAll(/,/g, '');
    string = string.replaceAll(/}/g, '');
    string = string.replaceAll(/{/g, '');
    string = string.replaceAll(/\d{3}/g, '');
    string = string.replaceAll(/([0-9][1-9])/g, '');
    string = string.replaceAll(/([2-9][0])/g, '');
    if(string.length === 0){
        setInputProps({
            helperText: tip,
            error: true,
          })
    }else{
        setInputProps({
            helperText: tip,
            error: false,
          })
    }  
    setValue(string)
  };

  export const convertStringToNumber1 = (string, setInputProps, setValue, tip) => {

    string = string.replaceAll(/[^-{1}+0-9,\s]/g, '');
    string = string.replaceAll(/-/g, '');
    string = string.replace('+', '');
    string = string.replaceAll(/,/g, '');
    string = string.replaceAll(/}/g, '');
    string = string.replaceAll(/{/g, '');
    string = string.replaceAll(/\d{2}/g, '');
    string = string.replaceAll(/([2-9])/g, '');

    if(string.length === 0){
        setInputProps({
            helperText: tip,
            error: true,
          })
    }else{
        setInputProps({
            helperText: tip,
            error: false,
          })
    }  
    setValue(string)
  };

  export const convertStringToNumber2 = (string, setInputProps, setValue, tip) => {
//0; 0,25; 0,5; 1; 2; 7
    string = string.replaceAll(/[^-{1}+0-9,\s]/g, '');
    string = string.replaceAll(/-/g, '');
    string = string.replace('+', '');
    string = string.replaceAll(/}/g, '');
    string = string.replaceAll(/{/g, '');
    string = string.replaceAll(/\d{2}/g, '');
    string = string.replaceAll(/([2-9])/g, '');

    if(string.length === 0){
        setInputProps({
            helperText: tip,
            error: true,
          })
    }else{
        setInputProps({
            helperText: tip,
            error: false,
          })
    }  
    setValue(string)
  };

  export const convertStringToNumber5 = (string, setInputProps, setValue, tip) => {
        string = string.replaceAll(/[^-{1}+0-9,\s]/g, '');
        string = string.replaceAll(/-/g, '');
        string = string.replace('+', '');
        string = string.replaceAll(/}/g, '');
        string = string.replaceAll(/{/g, '');
        string = string.replaceAll(/\d{3}/g, '');
        string = string.replaceAll(/([6-9][0])/g, '');
        string = string.replaceAll(/([5-9][1-9])/g, '');
    
        if(string.length === 0){
            setInputProps({
                helperText: tip,
                error: true,
              })
        }else{
            setInputProps({
                helperText: tip,
                error: false,
              })
        }  
        setValue(string)
      };


  export const convertStringToNumber6 = (string, setInputProps, setValue, tip) => {
    string = string.replaceAll(/[^-{1}+0-9,\s]/g, '');
    string = string.replaceAll(/-/g, '');
    string = string.replace('+', '');
    string = string.replaceAll(/}/g, '');
    string = string.replaceAll(/{/g, '');
    string = string.replaceAll(/\d{4}/g, '');
    string = string.replaceAll(/([2-9][0-9][0-9])/g, '');
    string = string.replaceAll(/([1][1-9][0-9])/g, '');
    string = string.replaceAll(/([1][0][1-9])/g, '');

    if(string.length === 0){
        setInputProps({
            helperText: tip,
            error: true,
          })
    }else{
        setInputProps({
            helperText: tip,
            error: false,
          })
    }  
    setValue(string)
  };