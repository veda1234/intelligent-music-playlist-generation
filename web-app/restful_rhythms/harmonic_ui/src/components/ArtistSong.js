import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, CircularProgress, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import {
  Link
} from "react-router-dom";
import SongsGrid from './songsTable';

export default function ArtistSong(props) {
  
  const [artist, setArtist] = React.useState(null);

  if(!artist)
  {
    (async () => {
      let url = new URL(`http://${window.location.hostname}:8000/api/artists/${props.id}`)
      let result = await fetch(url);
      result = await result.json();
      setArtist(result);
    })();
    return (<CircularProgress style={{ position: 'absolute', top: '50%', left: '50%' }}/>);   
  }
  
  return (
    <Grid container spacing={3}>
      <Grid item xs={12} align="center">
      <Box sx={{ p: 3}}>
        <Typography component="h2" variant="h2">
          Songs of {artist.name}
          </Typography>
          </Box>
      </Grid>
      <SongsGrid filter={{artist: artist.id}} />
      </Grid>
  );
}
