import React, { Component,useState } from "react";
import { Button, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import { DataGrid } from '@mui/x-data-grid';
import TextField from '@mui/material/TextField';
import { render } from "react-dom";
import {
  Route,
  BrowserRouter,
  Link
} from "react-router-dom";

export default function SearchPage(){
    const [searchQuery, setSearchQuery] = useState('');
    const [items, setItems] = React.useState([]);

    const columns = [
        { field: 'id', headerName: 'ID', width: 150 , hide:true},
        { field: 'name', headerName: 'Song Name', width: 300, headerAlign: 'center'},
        { field: 'artists', headerName: 'Artist Name', width: 300},
        { field: 'uri', headerName: 'Track ID', width: 300, hide:true},
        { field: 'is_present', headerName: 'Is already present', width: 300,hide:true},
        {
            field: "Add to list",
            width:300,
            renderCell: (cellValues) => {
              return (
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={(event) => {
                    addToList(event, items)
                  }}
                >
                  Add to list
                </Button>
              );
            }
          }
      ];

    async function addToList(e, items){
        e.preventDefault();
        track_id = items.uri.split(":")[2]
        let url = new URL(`http://${window.location.hostname}:8000/api/songs?track_id=${track_id}`)
        let added_or_not = await fetch(url);
        added_or_not = await added_or_not.json()
        console.log(added_or_not)
    }

    async function searchTheQuery(e) {
        e.preventDefault();
        let url = new URL(`http://${window.location.hostname}:8000/spotify/search?search=${searchQuery}`)
        let result = await fetch(url);
        result = await result.json()
        result = result.map((item)=>({
            name: item.name,
            id : item.id,
            artists : item.artists[0].name,
            is_present : item.is_already_present,
            uri : item.uri
            })
          )
        setItems(result)
        return false

    }
    return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
      <Box sx={{ p: 3}}>
        <Typography component="h3" variant="h3">
          Search for songs
          </Typography>
          </Box>
      </Grid>
      <Grid item xs={12}>
      <Box sx={{ p: 3}}>
      <form
            method="get"
            onSubmit={searchTheQuery}
        >
            <Typography component="h6" variant="h6">
          Song name : 
          </Typography>
            <input
                value={searchQuery}
                onInput={(e) => setSearchQuery(e.target.value)}
                type="text"
                id="header-search"
                placeholder="Search for songs"
                name="search"
            />
            <Button color="primary" type="submit">Search</Button>
        </form>
        </Box>
        </Grid>
        <Grid item xs={9}>
        <div style={{ display: 'flex', height: '100%' }}>
        <div style={{ height: 400, marginLeft: 200,flexGrow: 1 }}  >
        <DataGrid className="center"
          rows={items}
          columns={columns}
        />
        </div>
        </div>
      </Grid>
      {/* <Grid item xs={12}>
      <Box sx={{ p: 3}}>
        <TextField 
            id="outlined-basic" 
            label="Enter song name"    
            variant="outlined"
            value = {searchQuery}
            onInput={(e) => setSearchQuery(e.target.value)}
            name = "spotify-song"
        />
        <Button color="primary" variant="contained">
        Search
        </Button>
        </Box>
      </Grid> */}
    </Grid>
    
      );
}