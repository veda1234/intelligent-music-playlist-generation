import React, { Component } from "react";

export default class Room extends Component {
  constructor(props) {
    super(props);
    this.state = {
      spotifyAuthenticated: false,
    };
    this.authenticateSpotify = this.authenticateSpotify.bind(this);
    this.authenticateSpotify()
  }
  authenticateSpotify() {
    fetch("/spotify/is-authenticated")
      .then((response) => response.json())
      .then((data) => {
        this.setState({ spotifyAuthenticated: data.status });
        console.log(data.status);
        if (!data.status) {
          fetch("/spotify/get-auth-url")
            .then((response) => response.json())
            .then((data) => {
              window.location.replace(data.url);
            });
        }
      else{
        window.location = "/welcome";
      }
      });
  }
  render() {
    return (
      <div className="center">
      </div>
    );
  }
}

