import * as React from 'react';
import PlayArrowOutlined from '@mui/icons-material/PlayArrowOutlined';
import PauseOutlined from '@mui/icons-material/PauseOutlined';
import { Button, Grid } from '@material-ui/core';

let music;

export default function PlayCell(props) {
    const [playing, setPlaying] = React.useState(false);
    const play = (<PlayArrowOutlined color="primary"></PlayArrowOutlined>)
    const pause = (<PauseOutlined color="primary"></PauseOutlined>)

    React.useEffect(() => {
        if(music) 
        music.pause();
        music = new Audio(props.url);
        music.loop = true;
        if(playing) {
            music.play();
        } else{
            music.pause();
        }
    }, [playing])


    return (
    <Grid item align="center" style={{marginLeft: '30%'}} onClick={(ev) => setPlaying(!playing) }>
        {playing ? pause : play }
    </Grid>);
}
