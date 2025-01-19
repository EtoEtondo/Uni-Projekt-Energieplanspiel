import { useState } from 'react';
import Button from '@mui/material/Button';
import { StyledEngineProvider } from '@mui/material/styles';
import styled from 'styled-components';
import LoginView from './view/LoginView';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AdminHauptmenue } from './view/AdminHauptmenue';
import { AuthProvider } from './context/AuthProvider';
import { RequireAuthAdmin } from './routes/RequireAuthAdmin';
import { RequireAuthInstructor } from './routes/RequireAuthInstructor';
import { RequireAuthGroup } from './routes/RequireAuthGroup';
import { GroupHauptmenue } from './view/GroupHauptmenue';
import { InstructorHauptmenue } from './view/InstructorHauptmenue';

function App() {
  return (
    <StyledEngineProvider injectFirst>
      <AuthProvider>
        <Routes>
          <Route
            path="admin"
            element={
              <RequireAuthAdmin>
                <AdminHauptmenue/>
              </RequireAuthAdmin>
            }
          />
          <Route
            path="group"
            element={
              <RequireAuthGroup>
                <GroupHauptmenue />
              </RequireAuthGroup>
            }
          />
          <Route
            path="instructor"
            element={
              <RequireAuthInstructor>
                <InstructorHauptmenue />
              </RequireAuthInstructor>
            }
          />

          <Route path="/" element={<LoginView />} />
        </Routes>
      </AuthProvider>
    </StyledEngineProvider>
  );
}

export default App;
