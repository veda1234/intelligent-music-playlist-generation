import React, { Component,useState } from "react";
import { Button, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import { DataGrid } from '@mui/x-data-grid';
import Alert from '@mui/material/Alert';
import NavBar from "./navBar";

export default function SearchPage(){
    const [searchQuery, setSearchQuery] = useState('');
    const [items, setItems] = React.useState([]);
    const [loading, setLoading] = React.useState(false);

    const columns = [
        { field: 'id', headerName: 'ID', width: 150 , hide:true},
        { field: 'name', headerName: 'Song Name', width: 400, headerAlign: 'center'},
        { field: 'artists', headerName: 'Artist Name', width: 400, headerAlign: 'center'},
        { field: 'uri', headerName: 'Track ID', width: 300, hide:true},
        { field: 'is_present', headerName: 'Is already present', width: 300,headerAlign: 'center',hide:true},
        {
            field: "Add to list",
            width:300,
            renderCell: (cellValues) => {
              return (
                <Button
                  variant="contained"
                  color="secondary"
                  onClick={(event) => {
                    // send selected track id here
                    addToList(cellValues.row.id)
                  }}
                >
                  Add to list
                </Button>
              );
            }
          }
      ];

    async function addToList(track_id){
        let url = new URL(`http://${window.location.hostname}:8000/api/songs/`)
        setLoading(true);
        let added_or_not = await fetch(url, 
            {
                method: 'POST',
                headers: {
                  Accept: 'application/json',
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    track_id: track_id,
                })
              })
        added_or_not = await added_or_not.text()
        setLoading(false);
        console.log(added_or_not)
        return added_or_not
    }

    async function searchTheQuery(e) {
        e.preventDefault();
        let url = new URL(`http://${window.location.hostname}:8000/spotify/search?search=${searchQuery}`)
        let result = await fetch(url);
        result = await result.json()
        // console.log(result[0].album.images[0].url)
        result = result.map((item)=>({
            name: item.name,
            id : item.id,
            artists : item.artists.map((artist)=>artist.name),
            is_present : item.is_already_present,
            uri : item.uri,
            image : item.album.images[0].url
            })
          )
        console.log(result[0].image)
        setItems(result)
        return false

    }
    let imgUrls = items.filter(item => item.image).map(item => item.image)
    const defaultUrls = [
      "https://i.scdn.co/image/ab67616d0000b273e80e7dbce3996a1ae5967751",
      "https://i.scdn.co/image/ab67616d0000b273a7c10595167c713a2df0f187",
      "https://i.scdn.co/image/ab67616d0000b273d4daf28d55fe4197ede848be"
    ]
    for(let i=imgUrls.length; i< 3; i += 1) {
      imgUrls.push(defaultUrls[i])
    }

    if (imgUrls.length > 3) {
      imgUrls = imgUrls.slice(0,3)
    } 
    const images = imgUrls.map(img => (
      <img src={img} width="150" height="150"></img>
    ))
    return (
    <Grid container>
      <NavBar active="Import Tracks" />
      <Grid item xs={12}>
      <Box sx={{ p: 2}}>
        <Typography component="h5" variant="h5">
          Search for songs
          </Typography>
          </Box>
      </Grid>
      <Grid item xs={12}>
      {/* <Alert severity="success">Song added to database!</Alert> */}
      <Box sx={{ m: 3}}>
      <form
            method="get"
            onSubmit={searchTheQuery}
        >
            {/* <Typography component="h7" variant="h7">
          Song name : 
          </Typography> */}
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
        {/* <img src={items.image} width="200" height="200"></img> */}
        {/* <Grid container> */}
        <Grid item xs={2} align="center">
          {images}
      </Grid>
      {/* </Grid> */}
        <Grid item xs={10}>
        <div style={{ display: 'flex', height: '100%' }}>
        <div style={{ height: 400, marginLeft: 150,flexGrow: 1 }}  >
        <DataGrid className="center"
          rows={items}
          columns={columns}
          pageSize={25}
          rowsPerPageOptions={[25]}
          rowCount={25}
          loading={loading}
        />
        </div>
        </div>
      </Grid>
    </Grid>
    
      );
}