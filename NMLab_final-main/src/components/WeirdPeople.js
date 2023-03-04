import React, {useEffect, useState} from "react";
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ImageListItemBar from '@mui/material/ImageListItemBar';
import IconButton from '@mui/material/IconButton';
import InfoIcon from '@mui/icons-material/Info';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

import { FaceAPI } from "../api";

const WeirdPeople = ({setErr}) => {
    const [weird, setWeird] = useState([])

    useEffect(()=>{
        FaceAPI.getAllWeird().then((res)=> {
            const {all_data} = res.data;
            if (all_data){
                setWeird(all_data);
            }
        }).catch(err=>setErr(err.message))  
    },[])

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static" sx={{height: "10vh"}}>
                <Toolbar>
                <Typography variant="h3" color="inherit" component="div">
                    Strangers
                </Typography>
                </Toolbar>
            </AppBar>
            <ImageList sx={{ width: "inherit", height: "90vh" }} cols={4} rowHeight={200} >
                {weird.map((item, index) => (
                    <ImageListItem key={index}>
                    <img
                        src={`data:image/jpeg;base64,${item[0]}`}
                        alt={`test-${index}`}
                        loading="lazy"
                        style={{"object-fit": "contain", height:"100%", width:"100%"}}
                    />
                    <ImageListItemBar
                        title="Time"
                        subtitle={item[1]}
                        actionIcon={
                            <IconButton
                                sx={{ color: 'rgba(255, 255, 255, 0.54)' }}
                                aria-label={`info about ${item.title}`}
                            >
                                <InfoIcon />
                            </IconButton>
                            }
                    />
                    </ImageListItem>
                ))}
            </ImageList>
        </Box>
    );
}

export default WeirdPeople;
