import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('accessToken'));
  const [user, setUser] = useState(null); // Or load from localStorage if you store user object
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);
  const [loading, setLoading] = useState(false); // To track loading state for auth operations

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      setIsAuthenticated(true);
      // Optionally, fetch user details if only token is stored
      // fetchUser(); 
    } else {
      delete axios.defaults.headers.common['Authorization'];
      setIsAuthenticated(false);
      setUser(null);
    }
  }, [token]);

  // Placeholder login function - to be integrated with LoginPage
  const login = async (username, password) => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);
      const response = await axios.post('/api/v1/auth/login/token', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      if (response.data.access_token) {
        localStorage.setItem('accessToken', response.data.access_token);
        setToken(response.data.access_token);
        setIsAuthenticated(true);
        // Optionally fetch user data here
        // await fetchUser(response.data.access_token);
        setLoading(false);
        return { success: true };
      }
    } catch (error) {
      console.error('AuthContext login error:', error);
      setLoading(false);
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
    setLoading(false);
    return { success: false, error: 'Login failed: Unknown error' };
  };
  
  // Placeholder register function - to be integrated with RegistrationPage
  const register = async (username, password) => {
    setLoading(true);
    try {
      const payload = { username, password };
      await axios.post('/api/v1/auth/register', payload);
      // After successful registration, typically the user should log in.
      // Or, the backend could return a token directly upon registration.
      // For now, just indicate success.
      setLoading(false);
      return { success: true };
    } catch (error) {
      console.error('AuthContext register error:', error);
      setLoading(false);
      return { success: false, error: error.response?.data?.detail || 'Registration failed' };
    }
  };


  const logout = () => {
    localStorage.removeItem('accessToken');
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
    delete axios.defaults.headers.common['Authorization'];
  };

  // Example: Fetch user data if token exists (call after login or on initial load)
  // const fetchUser = async (currentToken = token) => {
  //   if (currentToken) {
  //     try {
  //       const response = await axios.get('/api/v1/auth/users/me', {
  //         headers: { Authorization: `Bearer ${currentToken}` }
  //       });
  //       setUser(response.data);
  //     } catch (error) {
  //       console.error("Failed to fetch user", error);
  //       logout(); // Token might be invalid
  //     }
  //   }
  // };
  // useEffect(() => { if(token && !user) fetchUser() }, [token, user]);


  const value = {
    token,
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    register,
    // fetchUser, // if implementing user fetching
    setUser, // Allow manual user setting if needed
    setToken, // Allow manual token setting if needed
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};