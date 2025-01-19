import styled from 'styled-components';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import List from '@mui/material/List';
import { Dialog, IconButton, ListItem, TextField } from '@mui/material';
import Button from '@mui/material/Button';

export const Wrapper = styled.div`
  width: 40em;
  height: 25em;
  background-color: #fcfafa;
  color: gray;
  box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
`;

export const ContentWrapper = styled(Box)`
  &.MuiBox-root {
    border: 1px solid blue;
    width: 100%;
    margin-left: auto;
    box-sizing: border-box;
    margin-right: auto;
    display: flex;
    justify-content: center;
    align-items: stretch;
    align-content: stretch;
    flex-direction: column;
  }
`;

export const HeaderWrapper = styled(Box)`
  &.MuiBox-root {
    height: 100px;
    border: none;
  }
`;

export const MainContentWrapper = styled(Box)`
  &.MuiBox-root {
    min-height: 680px;
    height: ${props => props.height};
    border: none;
    border-top: 1px solid blue;
  }
`;

export const ListWrapper = styled(List)`
&.MuiList-root{
  background-color: white;
  display: flex;
  flex-direction: column;
  width: 100%;
  min-width: 171px;
  overflow: auto;
  height: 100%;
  }
`;

export const ListItemWrapper = styled(ListItem)`
  &:hover {
    background-color: #e6e6e6;
  }
  &:active{
    background-color: #b0b0ae;
  }
`;

export const SearchListWrapper = styled(List)`
  &.MuiList-root{
    background-color: white;
    display: flex;
    flex-direction: column;
    width: 30%;
    min-width: 171px;
    height: 90%;
  }
`;

export const IconButtonWrapper = styled(IconButton)`
  margin-left: 10px;
`;

export const LoginButtonWrapper = styled(Button)`
  margin-bottom: 10px;
`;


export const FooterWrapper = styled(Box)`
  &.MuiBox-root {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 100px;
    border: none;
    margin-top: 10px;
    background-color: #2969cf;
    border-top: 1px solid blue;
  }
`;

export const MainContentButtonsWrapper = styled(Box)`
  &.MuiBox-root {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    border: none;
  }
`;

export const GroupInputsWrapper = styled(Box)`
  &.MuiBox-root {
    height: 85%;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    align-items: center;
    flex-direction: row;
    align-content: space-around;
}
  }
`;

export const GridWrapper = styled(Box)`
  &.MuiBox-root {
    display: grid;
    gridTemplateColumns: repeat(12, 1fr);
}
  }
`;

export const GroupsTextfield = styled(TextField)`
  &.MuiBox-root {
    border: 1px solid green;
  }
`;

export const BreadCrumbsWrapper = styled(Box)`
  &.MuiBox-root {
    box-sizing: border-box;
    margin-top: 10px;
    margin-right: auto;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-direction: row;
    min-width:400px;
  }
`;

export const CrumbsButtonWrapper = styled(Button)`
display: flex;
font-size : 14px;
height: 20px;
min-width:115px;
`;

export const DialogWrapper = styled(Dialog)`
  & > .MuiDialog-container > .MuiPaper-root {
    border: 3px solid blue;
  }
`;

