import React, { Component } from "react";
import { render } from "react-dom";
import {
  Route,
  BrowserRouter,
  Link
} from "react-router-dom";
import Room from "./Room";
import WelcomePage from "./WelcomePage"

export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="center">
      {/* <BrowserRouter> */}
      <h1>Welcome to the Intelligent Music Playlist generator!</h1>
      <Link to="/room"className="btn btn-primary">Try it out</Link>
      {/* </BrowserRouter> */}
      </div>
    );
  }
}
