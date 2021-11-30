import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import {
  Link
} from "react-router-dom";
import SongsGrid from './songsTable';

export default function ServerPaginationGrid() {


  return (
    <Grid container spacing={3}>
      <Grid item xs={12} align="center">
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
      <Box sx={{ p: 3}}>
        <Typography component="h2" variant="h2">
          Songs
          </Typography>
          </Box>
      </Grid>
      <SongsGrid filter={{}} />
      </Grid>
  );
}
