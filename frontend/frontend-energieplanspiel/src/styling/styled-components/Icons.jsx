import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { CircularProgress } from '@mui/material';
import styled, { css } from 'styled-components';

const setColor = (successfulAuth) => {
  switch (successfulAuth) {
    case 'OK':
      return css`
        color: #94cf68;
      `;
    case 'NOT OK':
      return css`
        color: #ff5d55;
      `;
    default:
      return css`
        color: #77767c;
      `;
  }
};

export const SvgWrapper = styled.svg`
  font-size: 15px;
  vertical-align: middle;
  fill: white;
  ${({ successfulAuth }) => setColor(successfulAuth)};
`;

export const LoginIcon = ({ successfulAuth }) => {
  return (
    <SvgWrapper
      viewBox={`0 0 512 512`}
      height="30%"
      width="30%"
      successfulAuth={successfulAuth}
    >
      <AccountCircleIcon />
    </SvgWrapper>
  );
};
