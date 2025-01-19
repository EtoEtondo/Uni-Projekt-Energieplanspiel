import { useState, useEffect, useContext } from "react";
import { StyledEngineProvider } from "@mui/material/styles";
import styled from "styled-components";
import {
  LoginButtonWrapper,
  Wrapper,
} from "../styling/styled-components/Wrapper";
import { BodyContent } from "../styling/styled-components/BodyContent";
import { LoginIcon } from "../styling/styled-components/Icons";
import { InputFieldWrapper } from "../styling/styled-components/InputFieldWrapper";
import InputAdornment from "@mui/material/InputAdornment";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import IconButton from "@mui/material/IconButton";
import CircularProgress from "@mui/material/CircularProgress";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import FilledInput from "@mui/material/FilledInput";
import OutlinedInput from "@mui/material/OutlinedInput";
import { Form, useNavigate } from "react-router-dom";
import LinearProgress from "@mui/material/LinearProgress";

import {
  StyledTextField,
  TextFieldIconWrapper,
  TextFieldsWrapper,
} from "../styling/styled-components/StyledTextField";
import { delay } from "../components/HelperFunction";
import { AuthMethodContext } from "../context/AuthProvider";
import AlertBar from "../components/AlertBar";

function LoginView() {
  const authMethod = useContext(AuthMethodContext);
  const [data, setData] = useState({});
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [inputError, setInputError] = useState(false);
  const [error, setError] = useState(-1);
  const [message, setMessage] = useState("");
  const [usernameError, setUsernameError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [loading, setLoading] = useState(false);
  const [successfulAuth, setSuccessfulAuth] = useState("INIT");
  const navigate = useNavigate();

  useEffect(() => {
    const getCsrf = async () => {
      await fetch("http://localhost:8000/csrf/", {
        credentials: "include",
      });
    };
    getCsrf();

    window.addEventListener("keyup", handleKeyUp);
    return () => {
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, []);

  const handleKeyUp = (e) => {
    if (e.key === 'Enter'){
      document.getElementById("btn").click()
    }
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
    setPassword(password);
  };

  const handleSubmit = () => {
    if (!username) {
      setUsernameError("Sie müssen einen Benutzernamen eingeben!");
      setInputError(true);
    } else {
      setUsernameError("");
      setInputError(false);
    }
    if (!password) {
      setPasswordError("Sie müssen ein Password eingeben!");
      setInputError(true);
    } else {
      setPasswordError("");
      setInputError(false);
    }

    if (username && password) {
      setLoading(true);
      const login = async () => {
        await fetch("http://localhost:8000/login/", {
          method: "POST",
          header: {
            "Content-Type": "application/json",
          },
          // mode: "cors",
          credentials: "include",
          body: JSON.stringify({
            username: username,
            password: password,
          }),
        }).then(async (response) => {
          const data = await response.json();
          if (response.ok) {
            setData(data);
            await delay(1000);
            setLoading(false);
            setSuccessfulAuth("OK");
            setInputError(false);
            await delay(2000);
            authMethod.signin(username, data["roles"]);
            setError(-1);
            setMessage("");
            // navigate(data['redirect-to']);
            // window.location.href = "";
          } else {
            setLoading(false);
            setSuccessfulAuth("NOT OK");
            setError(1);
            setMessage(data["Error"]);
          }
        });
      };
      login();
    }
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  return (
    <BodyContent>
      <Wrapper>
        <InputFieldWrapper>
          <LoginIcon successfulAuth={successfulAuth} />
          <TextFieldsWrapper>
              <StyledTextField
                disabled={loading}
                required
                label="Benutzername"
                value={username}
                error={inputError}
                helperText={usernameError}
                onChange={(e) => {
                  setUsername(e.target.value);
                }}
              />
              <StyledTextField
                disabled={loading}
                required
                label="Password"
                type={showPassword ? "text" : "password"}
                value={password}
                error={inputError}
                helperText={passwordError}
                onChange={(e) => {
                  setPassword(e.target.value);
                }}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        disabled={loading}
                        aria-label="toggle password visibility"
                        onClick={handleClickShowPassword}
                        onMouseDown={handleMouseDownPassword}
                        edge="start"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />
          </TextFieldsWrapper>
          <LoginButtonWrapper
            id="btn"
            disabled={loading || !username || !password}
            variant="contained"
            type="submit"
            autoFocus={loading || !username || !password}
            onClick={handleSubmit}
          >
            Anmelden
          </LoginButtonWrapper>
        </InputFieldWrapper>

        {loading && <LinearProgress />}
      </Wrapper>
      <AlertBar error={error} setError={setError} message={message}></AlertBar>
    </BodyContent>
  );
}

export default LoginView;
