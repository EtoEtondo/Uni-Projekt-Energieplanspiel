import {HeaderWrapper} from '../styling/styled-components/Wrapper';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import { StyledTab, StyledTabs } from '../styling/styled-components/Label';
import { useState } from 'react';
import Box from '@mui/material/Box';
import BreadCrumbs from './BreadCrumbs';

export const Header = ({handleCrumbChange, crumbType}) => {
    const [value, setValue] = useState('one');
  
    const handleChange = (event, newValue) => {
      setValue(newValue);
    };

    return (
      <HeaderWrapper>
        <Box sx={{ width: '100%' }}>
          <StyledTabs
            sx={{ width: '100%' }}
            value={value}
            onChange={handleChange}
            aria-label="wrapped label tabs example"
          >
            <StyledTab value="one" label="Energieplanspiel" />
            <StyledTab value="two" label="Konfiguration" />
          </StyledTabs>
        </Box>
      </HeaderWrapper>
    );
  };