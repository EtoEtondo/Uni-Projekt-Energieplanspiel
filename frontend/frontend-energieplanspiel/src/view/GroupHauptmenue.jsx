import { BodyContent } from '../styling/styled-components/BodyContent';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Button from '@mui/material/Button';
import { IconButton } from '@mui/material';
import React, { useState, useEffect } from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import {
  StyledTab,
  StyledTabs,
} from '../styling/styled-components/Label';
import { ListComponent } from '../components/ListComponent';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';
import BreadCrumbs from '../components/BreadCrumbs';
import GeneralHeader from '../components/Header/GeneralHeader';
import Configuration from '../components/Configuration';
import { GroupContent } from '../components/Content/GroupContent';

export const GroupHauptmenue = ({}) => {

  const handleTabChange = (switchedToTab) => {
    setCurrentTab(switchedToTab);
  };

  return (
    <React.Fragment>
      <GeneralHeader handleTabChange={handleTabChange}></GeneralHeader>
      <GroupContent />
      <Footer />
    </React.Fragment>
  );
};
