import React, { useEffect, useRef, useState } from "react";
import { Alert, Snackbar, AppBar, Toolbar, Typography, Button, Box } from '@mui/material';

import Map from "./Map.js";
import { PositionAPI } from "../api.js";

const MapContainer = () => {
  const mapRef = useRef(null);
  const mapApp = useRef(null);
  const [time, setTime] = useState("");
  const [distance, setDistance] = useState(0);
  
  useEffect(() => {
    if (mapApp.current) return;
    mapApp.current = new Map(mapRef.current);
    mapApp.current.updateMarkerLocation(setTime, setDistance)

    const interval = setInterval(()=>{
      mapApp.current.updateMarkerLocation(setTime, setDistance)
    },5000)
    return () => clearInterval(interval);
  }, []);

  const resetDistance = () => {
    PositionAPI.resetDistance().then((res)=>{
      if (res.data.Success){
        setDistance(0);
      }
    }).catch((err)=>console.log(err));
  };

  const locate = () => {
    const coordinates = mapApp.current.marker.getLngLat();
    mapApp.current.map.flyTo({center: [coordinates.lng, coordinates.lat], speed: 0.001, maxDuration: 4000});
  }

  return <div>
    <AppBar position="static" sx={{height: "8vh"}}>
      <Toolbar>
        <Typography variant="h3" color="inherit" component="div">
            Accumulated Distance: {distance.toFixed(1)} m
        </Typography>
        <Box sx={{ flexGrow: 1 }} />
        <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
          <Button onClick={resetDistance} variant="outlined" size="large" color="secondary" >
            <Typography variant="h5" color="white" component="div">
              RESET
            </Typography>
          </Button>
          <Button onClick={locate} variant="outlined" size="large" color="secondary" >
            <Typography variant="h5" color="white" component="div">
              Locate
            </Typography>
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
    <div ref={mapRef} className="mapWrapper" style={{height: '92vh'}}></div>
    {
      time ? 
      <Snackbar
        anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
        open={true}
      >
        <Alert variant="filled" severity='info'>
          Last update: {time}
        </Alert>
      </Snackbar>:<></>
    }
  </div>
};

export default MapContainer;
