import React, { useEffect, useRef, useState } from "react";
import { CardMedia, CardActions, Card, CardContent, Button, Typography, Input, Alert, Snackbar, Grid } from '@mui/material';

import { FaceAPI } from "../api.js";
import WeirdPeople from "./WeirdPeople.js";

const FaceContainer = () => {
  const [changeOwner, setChangeOwner] = useState(false);
  const [err, setErr] = useState('');
  const [image, setImage] = useState("");
  const [owner, setOwner] = useState('');
  const imageRef = useRef();

  const handleSetChangeOwner = () => {
    setChangeOwner(true);
  }

  const handleCancelChangeOwner = () => {
    setChangeOwner(false);
  }

  const handleChange = () => {
    if (image === ''){
      setErr("Image required!")
    }else{
      const formData = new FormData();
      formData.append('image', image, image.name);
      FaceAPI.updateOwner(formData).then((res)=>{
        setOwner(res.data.binary);
        setImage('');
        setChangeOwner(false);
      }).catch(err=>setErr(err.message));
    }
  }

  const updateImage = (img) => {
    setImage(img);
  }

  useEffect(() => {
    FaceAPI.getCurrentFace().then((res)=> {
      setOwner(res.data.binary);
    }).catch(err=>setErr(err.message))
  }, []);

  return <div>
    <Grid container spacing={1}>
      <Grid item md={3}>
        <Card sx={{ width: "inherit", height: "100vh" }}>
          <CardContent>
            <Typography gutterBottom variant="h2" component="div">
              Current Owner
            </Typography>
          </CardContent>
          <CardMedia
            component="img"
            width="100%"
            height="auto"
            src={`data:image/jpeg;base64,${owner}`}
            alt="current owner"
            loading="lazy"
          />
          {
            changeOwner ? 
            <CardActions>
              <Input
                id="import-button-problem"
                inputProps={{
                  accept:
                    ".jpg, .png",
                }}
                ref={imageRef}
                type="file"
                onChange = {()=>{
                  updateImage(imageRef.current.children[0].files[0])
                }}
              />
              <Button variant="contained" size="small" onClick={handleChange}>Change!</Button>
              <Button variant="outlined" size="small" onClick={handleCancelChangeOwner}>Cancel</Button>
            </CardActions> :
            <CardActions>
              <Button variant="contained" size="small" onClick={handleSetChangeOwner}>Change Owner</Button>
            </CardActions>
          }
        </Card>
      </Grid>
      <Grid item md={9}>
        <WeirdPeople setErr={setErr} />
      </Grid>
    </Grid>
    <Snackbar
      anchorOrigin={{ vertical: "top", horizontal: "center" }}
      open={err !== ''}
      autoHideDuration={3000}
      onClose={() => setErr('')}
    >
      <Alert variant="filled" severity='error'>
        {err}
      </Alert>
    </Snackbar>
  </div>
};

export default FaceContainer;
