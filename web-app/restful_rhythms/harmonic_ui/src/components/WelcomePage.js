import React, { Component } from "react";
import { render } from "react-dom";

export default class WelcomePage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <h1>You have signed in !</h1>
      </div>
    );
  }
}