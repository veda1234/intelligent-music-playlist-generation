import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, CircularProgress, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import NavBar from './navBar';

import SongsGrid from './songsTable';

export default function AlbumSong(props) {
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
      <NavBar />
       <Grid item xs={12} align="center">
       <Typography component="h4" variant="h4" align="center">Tracks in {album.name}</Typography>
      </Grid>
      <Grid item xs={12} align="center">
      <Typography component="h5" variant="h5">Artists</Typography> <Typography display="block" variant="body1" gutterBottom>{album.artists.map(artist => artist.name)}</Typography>
      <Typography component="h5" variant="h5">Release date</Typography> <Typography display="block" variant="body1" gutterBottom>{album.release_date}</Typography>
      </Grid>
      <SongsGrid filter={{album: album.id}} />
      </Grid>
  );
}
