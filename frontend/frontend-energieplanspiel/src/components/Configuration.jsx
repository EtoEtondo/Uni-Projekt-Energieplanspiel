import { useState, useEffect, useCallback } from "react";
import {
  MainContentWrapper,
  MainContentButtonsWrapper,
} from "../styling/styled-components/Wrapper";
import { useDropzone } from "react-dropzone";
import styled from "styled-components";
import { Box, Button } from "@mui/material";
import { addConfig } from "../Requests/PostRequests";
import AlertBar from "./AlertBar";

const getColor = (props) => {
  if (props.isDragAccept) {
    return "#00e676";
  }
  if (props.isDragReject) {
    return "#ff1744";
  }
  if (props.isFocused) {
    return "#2196f3";
  }
  return "#eeeeee";
};

const Dragzone = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border-width: 2px;
  border-radius: 2px;
  border-color: ${(props) => getColor(props)};
  border-style: dashed;
  background-color: #fafafa;
  color: #bdbdbd;
  outline: none;
  transition: border 0.24s ease-in-out;
  height: 50%;
  width: 50%;
`;

const UploadContainer = styled(Box)`
  height: 92%;
  width: 100%;
  display: flex;
  flex-wrap: nowrap;
  align-content: flex-end;
  justify-content: center;
  align-items: center;
  flex-direction: row;
`;

function Configuration({}) {
  const [filesToUpload, setFilesToUpload] = useState([]);
  const [error, setError] = useState(-1);
  const [message, setMessage] = useState("");

  const onDrop = useCallback(
    (acceptedFiles) => {
      var arr = [
        "config.yml",
        "dat_energie-workshop.csv",
        "general_parameters.csv",
      ];
      acceptedFiles.map((file) => {
        if (
          arr.indexOf(file.name.toLowerCase()) > -1 &&
          filesToUpload.length + acceptedFiles.length <= 3
        ) {
          setFilesToUpload((prevArray) => [...prevArray, file]);
        }
      });
    },
    [filesToUpload]
  );

  const {
    getRootProps,
    getInputProps,
    acceptedFiles,
    isFocused,
    isDragAccept,
    isDragReject,
    isDragActive,
  } = useDropzone({ onDrop });

  const handleSubmit = () => {
    const data = new FormData();
    filesToUpload.forEach((file) => {
      data.append("file", file);
    });
    if (filesToUpload.length > 0) {
      addConfig(data).then((response) => {
        setError(response.status);
        if(response.status !== -1){
          setMessage(response.message);
        }
        setFilesToUpload([]);
      });
    }
  };

  const cancelUpload = () => {
    if (filesToUpload.length > 0) {
      setFilesToUpload([]);
    }
  };

  return (
    <MainContentWrapper height={"80%"}>
      <UploadContainer>
        <Dragzone
          {...getRootProps({
            isFocused,
            isDragAccept,
            isDragReject,
            isDragActive,
          })}
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <p className="dropzone-content">Release to drop the files here</p>
          ) : (
            <p className="dropzone-content">
              Drag’n’drop or click to upload config.yml,
              DAT_Energie-Workshop.csv, general_parameters.csv.
            </p>
          )}
          <aside>
            <ul>
              {filesToUpload.map((file) => (
                <li key={file.path}>
                  {file.path} - {file.size} bytes
                </li>
              ))}
            </ul>
          </aside>
        </Dragzone>
      </UploadContainer>

      <MainContentButtonsWrapper>
        <Button
          variant="contained"
          disabled={filesToUpload.length === 0}
          onClick={() => handleSubmit()}
        >
          Upload
        </Button>
        <Button
          variant="contained"
          disabled={filesToUpload.length === 0}
          onClick={() => cancelUpload()}
        >
          Abbrechen
        </Button>
      </MainContentButtonsWrapper>
      <AlertBar error={error} setError={setError} message={message}></AlertBar>
    </MainContentWrapper>
  );
}

export default Configuration;
