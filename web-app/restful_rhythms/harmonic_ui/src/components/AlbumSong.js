import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, CircularProgress, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import {
  Link
} from "react-router-dom";
import SongsGrid from './songsTable';

export default function AlbumSong(props) {
  console.log('occur');
  const [album, setAlbum] = React.useState(null);

  if(!album)
  {
    (async () => {
      let url = new URL(`http://${window.location.hostname}:8000/api/albums/${props.id}`)
      let result = await fetch(url);
      result = await result.json();
      setAlbum(result);
    })();
    return (<CircularProgress style={{ position: 'absolute', top: '50%', left: '50%' }}/>);   
  }
  
  return (
    <Grid container spacing={3}>
      <Grid item xs={12} align="center">
      <Box sx={{ p: 3}}>
        <Typography component="h2" variant="h2">
          {album.name}
          </Typography>
          </Box>
      </Grid>
      <SongsGrid filter={{album: album.id}} />
      </Grid>
  );
}
