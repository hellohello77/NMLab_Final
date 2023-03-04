import React from "react";
import { Outlet, Navigate } from "react-router-dom";
import { Grid, Button } from "@mui/material";

import ListRouter from "./components/Router.js";

const Navigator= ({login, setLogin}) => {
  const handleLogout = ()=>{
    localStorage.removeItem("NMLAB");
    setLogin(false);
  }

  return (
    login ? 
    <Grid container>
      <Grid item md={1}>
        <ListRouter />
        <Button variant="contained" onClick={handleLogout}>Logout</Button>
      </Grid>
      <Grid item md={11}>
        <Outlet />
      </Grid>
    </Grid> : 
    <Navigate to="/login" replace={true}/>
  );
};

export default Navigator;
