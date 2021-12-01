import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import SongsGrid from './songsTable';
import NavBar from './navBar';
import {
  Link
} from "react-router-dom";


export default function ServerPaginationGrid() {
  return (
    <Grid container spacing={3}>
      <NavBar active="Tracks"/>
      {/* <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
          <Button color="primary" variant="contained" to="/artists" component={Link}>
          Artist's Page
            </Button>
          </Typography>
          <Typography component="h4" variant="h4">
          <Button color="primary" variant="contained" to="/albums" component={Link}>
          Album's Page
          </Button>
          </Typography>
          </Grid>
      <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
          <Button color="primary" variant="contained" to="/search" component={Link}>
          Search for songs
          </Button>
          </Typography>
      </Grid> */}
      {/* <Grid item xs={12} align="center"> */}
      {/* <Grid item xs={12}>
      <Box sx={{ p: 3}}>
        <Typography component="h4" variant="h4">
          Tracks
          </Typography>
          </Box>
      </Grid> */}
      <Grid item xs={11} align="center">
        <p style={{ marginLeft: '4%', fontWeight: 500, fontFamily: '"Roboto","Helvetica","Arial","sans-serif"', textAlign: 'center' }}>Tracks</p>
      </Grid>
      <SongsGrid filter={{}} />
      </Grid>
  );
}
