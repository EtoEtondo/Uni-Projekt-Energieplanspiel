import { useLocation, Navigate } from 'react-router-dom';
import { useContext, useEffect } from 'react';
import { AuthStateContext } from '../context/AuthProvider';

//miko:Quelle:für den Lösungsansastz
//https://github.com/remix-run/react-router/tree/dev/examples
export const RequireAuthGroup = ({ children }) => {
  let auth = useContext(AuthStateContext);
  let location = useLocation();
  if (auth.roles !== 'group') {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return <Navigate to="/" state={{ from: location }} replace />;
  }

  return children;
};
