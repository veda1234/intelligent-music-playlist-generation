import React, { Component } from "react";
import { render } from "react-dom";
import {
  Route,
  BrowserRouter,
  Link
} from "react-router-dom";
import Room from "./Room";
import WelcomePage from "./WelcomePage"
import HomePage from "./HomePage";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
      <BrowserRouter>
      <Route path="/" exact render={() => <HomePage/>}></Route>
      <Route path="/room" exact render={() => <Room/>}></Route>
      <Route path="/welcome" exact render={() => <WelcomePage/>}></Route>
      </BrowserRouter>
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
