import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, CircularProgress, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import {
  Link
} from "react-router-dom";
import SongsGrid from './songsTable';
import NavBar from './navBar';

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
      <NavBar />
      <Grid item xs={11} align="center">
        <p style={{ marginLeft: '4%', fontWeight: 500, fontFamily: '"Roboto","Helvetica","Arial","sans-serif"' }}>Tracks by {artist.name}</p>
      </Grid>
      <SongsGrid filter={{artist: artist.id}} />
      </Grid>
  );
}
