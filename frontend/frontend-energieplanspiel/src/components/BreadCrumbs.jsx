import { useState, useEffect } from 'react';
import { BreadCrumbsWrapper, Wrapper } from '../styling/styled-components/Wrapper';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import Crumbs from './Crumbs';

function BreadCrumbs({handleCrumbChange, crumbType, crumbs}) {

  return (
    <BreadCrumbsWrapper>
     {crumbs.map((crumb, index) => {
        return(
            <Crumbs key={index} index={index} crumb={crumb} currentCrumb={crumbType} handleCrumbChange={handleCrumbChange} crumbsLength={crumbs.length}></Crumbs>
        )
     })}
    </BreadCrumbsWrapper>
  );
}

export default BreadCrumbs;
