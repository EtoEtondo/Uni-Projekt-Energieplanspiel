import { useState, useEffect } from 'react';
import { BreadCrumbsWrapper, CrumbsButtonWrapper, Wrapper } from '../styling/styled-components/Wrapper';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import Button from '@mui/material/Button';

function Crumbs(props) {

const handleCrumbClick = (crumbType) =>{
    props.handleCrumbChange(crumbType)
    }
    

  return (

    <CrumbsButtonWrapper 
    disabled={props.index > props.currentCrumb ? true: false} 
    endIcon={ props.index < props.crumbsLength - 1 ? <KeyboardArrowRightIcon/> : ""}
    onClick={()=> handleCrumbClick(props.index)}
    >
        {props.crumb}
    </CrumbsButtonWrapper>
        
           
  );
}

export default Crumbs;
