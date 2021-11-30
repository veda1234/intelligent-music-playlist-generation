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
       <Grid item xs={11} align="center">
        <p style={{ marginLeft: '4%', fontWeight: 500, fontFamily: '"Roboto","Helvetica","Arial","sans-serif"' }}>Tracks in {album.name}</p>
      </Grid>
      <Grid style={{marginLeft: 30 }}>
      <h4>Artists: </h4> <p>{album.artists.map(artist => artist.name)}</p>
      <h4>Release date: </h4> <p>{album.release_date}</p>
      </Grid>
      <SongsGrid filter={{album: album.id}} />
      </Grid>
  );
}
