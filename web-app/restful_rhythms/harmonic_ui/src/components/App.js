import React, { Component } from "react";
import { render } from "react-dom";
import {
  Route,
  BrowserRouter,
  Link
} from "react-router-dom";
import Room from "./Room";
import WelcomePage from "./WelcomePage";
import HomePage from "./HomePage";
import ArtistsPage from "./ArtistsPage";
import AlbumsPage from "./AlbumsPage";
import AlbumSong from './AlbumSong';
import ArtistSong from './ArtistSong';

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
      <Route path="/artists" exact render={() => <ArtistsPage/>}></Route>
      <Route path="/albums" exact render={() => <AlbumsPage/>}></Route>
      <Route path="/artist/:id" exact render={({match}) => <ArtistSong id={match.params.id} />}></Route>
      <Route path="/album/:id" exact render={({match}) => <AlbumSong id={match.params.id} />}></Route>
      
      </BrowserRouter>
      </div>
    );
  }
}

const appDiv = document.getElementById("app");
render(<App />, appDiv);
