import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { IconButton } from "@mui/material";
import ListItemSecondaryAction from "@mui/material/ListItemSecondaryAction";
import CheckBoxIcon from "@mui/icons-material/CheckBox";
import {
  ListWrapper,
  IconButtonWrapper,
  ListItemWrapper,
} from "../styling/styled-components/Wrapper";
import React from "react";
import { useState, useEffect } from "react";

export const ListComponent = (props) => {
  const clickedOnListElement = (element) => {
    if ((props.crumbType < props.crumbsLength - 1) && props.crumbType < props.maxCrumbs) {
      props.goToNextCrumbOnListElementClick(props.crumbType + 1, element);
    }
  };

  if (props.currentList.length === 0) {
    return <h3>Liste leer.</h3>
  } else {
    if (
      (props.role === "INSTRUCTOR" && props.crumbType === 1) ||
      props.role === "ADMIN"
    ) {
      return (
        <ListWrapper>
          {props.currentList &&
            props.currentList.map((element, index) => {
              return (
                <ListItemWrapper
                  divider
                  key={index}
                  onClick={() => clickedOnListElement(element)}
                >
                  <ListItemText primary={element.name} secondary={element.username ? element.username : ""} />
                  <ListItemSecondaryAction>
                    {(props.crumbType === 1 || props.crumbType === 3 ?
                    
                    <IconButtonWrapper
                    edge="end"
                    aria-label="edit"
                    onClick={() =>
                      props.handleClickOpenEditDialog(true, index)
                    }
                  >
                    <EditIcon />
                  </IconButtonWrapper>

                    :
                      ""

                    )}
                    <IconButtonWrapper edge="end" aria-label="delete" onClick={(e) => props.deleteEntry(element)}>
                      <DeleteIcon />
                    </IconButtonWrapper>
                    {((props.role === "INSTRUCTOR" && props.crumbType === 1) || (props.role === "ADMIN" && props.crumbType === 3)) &&
                      element.has_submitted === true ? (
                      <IconButtonWrapper
                        disabled
                        edge="end"
                        aria-label="delete"
                      >
                        <CheckBoxIcon />
                      </IconButtonWrapper>
                    ) : (
                      ""
                    )}
                  </ListItemSecondaryAction>
                </ListItemWrapper>
              );
            })}
        </ListWrapper>
      );
    } else {
      return (
        <ListWrapper>
          {props.currentList &&
            props.currentList.map((element, index) => {
              return (
                <ListItem
                  divider
                  key={index}
                  onClick={() => clickedOnListElement(element)}
                >
                  <ListItemText primary={element.name} secondary={index} />
                </ListItem>
              );
            })}
        </ListWrapper>
      );
    }
  }
};
