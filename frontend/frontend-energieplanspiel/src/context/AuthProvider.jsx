import {
  createContext,
  useEffect,
  useLayoutEffect,
  useReducer,
  useState,
} from 'react';
import { useNavigate } from 'react-router-dom';

// Perfrormance Context um mehrer Rerendering zu verhindern
//https://hswolff.com/blog/how-to-usecontext-with-usereducer/
//https://www.nielskrijger.com/posts/2021-02-16/use-reducer-and-use-context/;
//https://reactjs.org/docs/hooks-reference.html#usecontext
//https://reactjs.org/docs/hooks-reference.html#usereducer

export const AuthMethodContext = createContext();
export const AuthStateContext = createContext();
export const AuthProvider = ({ children }) => {
  let [user, setUser] = useState(null);
  let [roles, setRoles] = useState(null);
  const navigate = useNavigate();
  let tmp;
  useLayoutEffect(() => {
    tmp = JSON.parse(window.localStorage.getItem('user'));
    if (tmp != null) {
      setUser(tmp.user);
      setRoles(tmp.roles);
    }
  }, []);
  useEffect(() => {
    if (roles === null) {
      navigate('/', { replace: true });
    }
    if (roles === 'instructor') {
      navigate('instructor', { replace: true });
    }
    if (roles === 'group') {
      navigate('group', { replace: true });
    }

    if (roles === 'admin') {
      navigate('admin', { replace: true });
    }
  }, [user]);

  let signin = (newUser, roles) => {
    setUser(newUser);
    setRoles(roles);
    const usrObject = {
      islogged: true,
      user: newUser,
      roles: roles,
    };
    window.localStorage.setItem('user', JSON.stringify(usrObject));
  };

  let signout = (callback) => {
    setUser(null);
    setRoles(null);
    window.localStorage.clear();
    callback();
  };

  return (
    <AuthMethodContext.Provider value={{ signin, signout }}>
      <AuthStateContext.Provider
        value={{
          user,
          roles,
        }}
      >
        {children}
      </AuthStateContext.Provider>
    </AuthMethodContext.Provider>
  );
};
