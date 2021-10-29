import React, { Component } from "react";
import { render } from "react-dom";
import MainPage from '../../static/images/Music_logo.jpeg'
import {
  Link
} from "react-router-dom";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";

export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Grid container spacing={3}>
        <Grid item xs={12} align="center">
        <img className="logo" src={MainPage} alt="MainPage slide"/>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography component="h2" variant="h2">
          Welcome to the Intelligent Music Playlist generator
          </Typography>
        </Grid>
          <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
          <Button color="primary" variant="contained" to="/room" component={Link}>
          Try it out
            </Button>
          </Typography>
          </Grid>
       </Grid>
    );
  }
}
