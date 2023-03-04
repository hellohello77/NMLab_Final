import React, { useState, useEffect } from "react";
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from "@mui/material/Typography";
import { Navigate } from "react-router-dom";

const LoginContainer = ({login, setLogin}) => {
  const {REACT_APP_PASSWORD, REACT_APP_USER} = process.env;

  const [user, setUser] = useState('NMLAB_FINAL');
  const [password, setPassword] = useState('');
  const [err, setErr] = useState('')

  useEffect(()=>{
    if(localStorage.getItem('NMLAB')){
      setLogin(true);
    }
  })
  
  const changeUser = ({target})=> {
    setUser(target.value)
  }

  const changePassword = ({target})=> {
    setPassword(target.value)
  }

  const handleLogin = () => {
    if(password === REACT_APP_PASSWORD && user === REACT_APP_USER){
      localStorage.setItem("NMLAB", "hi")
      setLogin(true);
    }else{
      setPassword('');
      setErr("Invalid user or password");
    }
  }

  return <Box
      component="form"
      sx={{
        '& > :not(style)': { m: 1, width: '25ch', height: '7ch' },
      }}
      noValidate
      autoComplete="off"
    >
      <TextField
          required
          id="outlined-required"
          label="User"
          value={user}
          onChange={changeUser}
        />
        <TextField
          required
          id="outlined-required"
          label="Password"
          value={password}
          type="password"
          onChange={changePassword}
        />
        <Button variant="contained" onClick={handleLogin} >Login</Button>
        {err==='' ? <></>: <Typography variant="h2" gutterBottom component="div" color="red">{err}</Typography>}
        {login ? <Navigate to="/app" replace={true}/>:<></>}
    </Box>
};

export default LoginContainer;
