import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, CircularProgress, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import NavBar from './navBar';
import PlayCell from './playCell';

export default function AlbumSong(props) {
  const [track, setTrack] = React.useState(null);
  const [track_image, setTrackImage] = React.useState(null);

  if(!track)
  {
    (async () => {
      let url = new URL(`http://${window.location.hostname}:8000/api/songs/${props.id}`)
      let result = await fetch(url);
      result = await result.json();
      console.log(result);
      setTrack(result);
      
      let track_url = new URL(`http://${window.location.hostname}:8000/spotify/search?search=${result.name}`)
      let track_result = await fetch(track_url);
      track_result = await track_result.json()
      let target_artists = result.artists.map(artist => artist.id)
      console.log(track_result);
      track_result = track_result.find(track => {
        let curr_ids = track.artists.map(artist => artist.id);
        return curr_ids.every(artist_id => target_artists.includes(artist_id));
      })
      let img_url = track_result.album.images[0].url
      setTrackImage(img_url);

    })();
    return (<CircularProgress style={{ position: 'absolute', top: '50%', left: '50%' }}/>);   
  }

  const lyricEle = track && track.lyrics.split('\n').map(para => (
    <Typography display="block" variant="body1" gutterBottom>{para}</Typography>
  ))

  const audioFeatureEle = track && Object.keys(track.audio_features).map(feature => (
    <Typography display="block" variant="body1" gutterBottom>{feature} : {track.audio_features[feature]}</Typography>
  ))
  
  return (
    <Grid container spacing={2}>
       <Grid item xs={12}>
       <Box sx={{ m: 3}}>
       <Typography component="h3" variant="h3" align="center">{track.name}</Typography>
        </Box>
      </Grid>
      <Grid item xs={4} align="center">
        <img src={track_image} width="150" height="150"></img>
        <Typography ml={10} component="h5" variant="h5">Artists</Typography> <Typography display="block" variant="body1" gutterBottom>{track.artists.map(artist => artist.name)}</Typography>
          <Typography component="h5" variant="h5">Duration</Typography> <Typography display="block" variant="body1" gutterBottom>{`${track.duration_minutes}:${track.duration_seconds}`}</Typography>
          <Typography component="h5" variant="h5">Album</Typography> <Typography display="block" variant="body1" gutterBottom>{track.album}</Typography>
          {track.preview_url && (<PlayCell large="True" url={track.preview_url}></PlayCell>)}
          {/* <Typography component="h5" variant="h5">Play</Typography> <Typography display="block" variant="body1" gutterBottom><a href={track.preview_url}>{track.preview_url}</a></Typography> */}
      </Grid>
      <Grid item xs={4}>
        <Box sx={{ m: 3}}>
          <Typography component="h5" variant="h5">Cluster</Typography> <Typography display="block" variant="body1" gutterBottom>{track.cluster}</Typography>
          <Typography component="h5" variant="h5">Emotion</Typography> <Typography display="block" variant="body1" gutterBottom>{track.emotion}</Typography>
          <Typography component="h5" variant="h5"> Audio Features</Typography> 
          {/* <Typography display="block" variant="body1" gutterBottom>{JSON.stringify(track.audio_features,null,2)}</Typography> */}
          {audioFeatureEle}
          </Box>
          </Grid>
        <Grid item xs={4}>
        <Box sx={{ m: 3}}>
          <Typography component="h5" variant="h5">Lyrics</Typography>{lyricEle}
        </Box>
      </Grid>
    </Grid>
  );
}
