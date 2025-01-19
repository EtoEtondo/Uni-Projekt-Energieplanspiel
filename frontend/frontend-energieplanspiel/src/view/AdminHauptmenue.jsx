import { BodyContent } from '../styling/styled-components/BodyContent';
import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import Button from '@mui/material/Button';
import { IconButton } from '@mui/material';
import React, { useState, useEffect, useContext } from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import {
  StyledTab,
  StyledTabs,
} from '../styling/styled-components/Label';
import { ListComponent } from '../components/ListComponent';
import AdminHeader from '../components/Header/AdminHeader';
import { Footer } from '../components/Footer';
import { AdminContent } from '../components/Content/AdminContent';
import BreadCrumbs from '../components/BreadCrumbs';
import Configuration from '../components/Configuration';
import { Navigate, useLocation, useNavigate } from 'react-router-dom';
import { AuthStateContext } from '../context/AuthProvider';

export const AdminHauptmenue = ({role}) => {
  const [currentTab, setCurrentTab] = useState(0);
  let location = useLocation();
  const navigate = useNavigate();
  const authState = useContext(AuthStateContext)


  const handleTabChange = (switchedToTab) => {
    setCurrentTab(switchedToTab);
  };

  return (
    <React.Fragment>
      <AdminHeader handleTabChange={handleTabChange}></AdminHeader>
      {(() => {
        if (currentTab === 0) {
          return <AdminContent />
        } else if (currentTab === 1) {
          return <Configuration></Configuration>
        }


      })()}
      <Footer />
    </React.Fragment>
  );
};
