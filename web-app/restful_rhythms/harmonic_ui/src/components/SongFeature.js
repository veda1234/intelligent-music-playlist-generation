import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, CircularProgress, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import NavBar from './navBar';

export default function AlbumSong(props) {
  const [track, setTrack] = React.useState(null);

  if(!track)
  {
    (async () => {
      let url = new URL(`http://${window.location.hostname}:8000/api/songs/${props.id}`)
      let result = await fetch(url);
      result = await result.json();
      setTrack(result);
    })();
    return (<CircularProgress style={{ position: 'absolute', top: '50%', left: '50%' }}/>);   
  }
  
  return (
    <Grid container spacing={3}>
       <Grid item xs={11} align="center">
        <p style={{ marginLeft: '4%', fontWeight: 500, fontFamily: '"Roboto","Helvetica","Arial","sans-serif"', textAlign: 'center' }}>{track.name}</p>
      </Grid>
      <Grid style={{marginLeft: 30 }}>
      <h4>Artists: </h4> <p>{track.artists.map(artist => artist.name)}</p>
      <h4>Duration: </h4> <p>{`${track.duration_minutes}:${track.duration_seconds}`}</p>
      <h4>Album: </h4> <p>{track.album}</p>
      <h4>Play:</h4> <p>{track.preview_url}</p>
      <h4>Cluster:</h4> <p>{track.cluster}</p>
      <h4>Emotion:</h4> <p>{track.emotion}</p>
      <h4>Audio Features:</h4> <p>{JSON.stringify(track.audio_features)}</p>
      <h4>Lyrics:</h4> <p>{track.lyrics}</p>
      </Grid>
      </Grid>
  );
}
