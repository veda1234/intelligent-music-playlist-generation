import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import {
  Link
} from "react-router-dom";
import Checkbox from '@mui/material/Checkbox';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Modal from '@mui/material/Modal';
import RadioGroup from '@mui/material/RadioGroup';
import Radio from '@mui/material/Radio';
import PlayCell from './playCell';

const numRows =  Math.round((Math.random() * 2500000))
export default function SongsGrid(props) {
  
  const columns = [
    { field: 'name', headerName: 'Name', width: 150, headerAlign: 'center'},
    { field: 'id', headerName: 'id', width: 150 , hide:true},
    { field: 'album', headerName: 'Album', width: 150, headerAlign: 'center'},
    { field: 'artists', headerName: 'Artist', width: 150, headerAlign: 'center'},
    { field: 'duration', headerName: 'Duration', width: 150, headerAlign: 'center'},
    { field: 'cluster', headerName: 'Cluster Number', width: 180, headerAlign: 'center'},
    { field: 'emotion', headerName: 'Emotion detected', width: 190, headerAlign: 'center'},
    {   field: 'preview_url', 
        headerName: 'Preview', 
        width: 150, 
        headerAlign: 'center',
        renderCell: (cellValues) => {
            if(cellValues.value) {
              return (<PlayCell url={cellValues.row.preview_url}></PlayCell>);
            } 
            return (<p></p>)
        }
    },
    {
        field: 'is_present',
        headerName: '  ',
        width: 150,
        headerAlign: 'center',
        renderCell: (cellValues) =>  {
          if(!cellValues.value){
            return (<Button onClick={(ev) => addToList(cellValues.row.id)} 
            variant="text" color="primary">+ ADD</Button>);
          } else {
            return (<Button onClick={(ev) => removeFromList(cellValues.row.id)} 
            variant="text" color="primary">- REMOVE</Button>);
          }
        }
    }
  ].map(column => ({ ...column,filterable: false, sortable: false }));
  

  const [page, setPage] = React.useState(0);
  const [loading, setLoading] = React.useState(false);
  const [items, setItems] = React.useState([]);
  const [prevItem, setPrevItem] = React.useState(null);
  const [nextItem, setNextItem] = React.useState(null);
  const [prevPage, setPrevPage] = React.useState(0);
  const [filter, setFilter] = React.useState(props.filter || {})

  const [openFilter, setOpenFilter] = React.useState(false);
  const handleFilterOpen = () => setOpenFilter(true);
  const handleFilterClose = () => setOpenFilter(false);
  const filterStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };

  function addToList(track_id) {
    setLoading(true);
    fetch('/api/songs/add_to_list/', {
      method: 'POST',
      body: JSON.stringify({ track_id }),
      headers: {
        'Content-Type': 'application/json',
      },
    }).then(res => res.text()).then(res => {
        const curr_items = items.map((item) => {
          if(item.id == track_id) return {
            ...item,
            is_present: true,
          } 
          return item
        })
        setItems(curr_items)
        setLoading(false);
    })
  }

  function removeFromList(track_id) {
    setLoading(true);
    fetch(`/api/songs/${track_id}/remove_from_list/`, {
      method: 'DELETE',
    }).then(res => res.text()).then(res => {
        const curr_items = items.map((item) => {
          if(item.id == track_id) return {
            ...item,
            is_present: false,
          } 
          return item
        })
        setItems(curr_items)
        setLoading(false);
    })
  }

  function handlePageChange(newPage) {
        if(newPage > prevPage) {
          setPrevItem(items[items.length - 1].id)
          setNextItem(null)
        } else {
          setNextItem(items[0].id)
          setPrevItem(null)
        }
      setPage(newPage)
      setPrevPage(page)
  }

  function handleByUser(event) {
      setFilter({
        ...filter,
        by_user: event.target.checked
      })
  }

  function handleCluster(event) {
      if(event.target.value != 0) {
        setFilter({
          ...filter,
          cluster: event.target.value
        })
      } else {
        const temp_filter = { ...filter }
        delete temp_filter.cluster
        setFilter(temp_filter)
      } 
  }

  function handleEmotion(event) {
    if(event.target.value != 'All') {
      setFilter({
        ...filter,
        emotion: event.target.value
      })
    } else {
      const temp_filter = { ...filter }
      delete temp_filter.emotion
      setFilter(temp_filter)
    } 
  }

  async function loadServerRows() {
    let url = new URL(`http://${window.location.hostname}:8000/api/songs`)
    if (prevItem) {
      url.searchParams.append('prevId', prevItem)
    } else if(nextItem) {
      url.searchParams.append('nextId', nextItem)   
    }
    if(filter.by_user) 
      url.searchParams.append('by_user', true)
    if(filter.emotion) {
      url.searchParams.append('emotion', filter.emotion)
    }
    if(filter.cluster) {
      url.searchParams.append('cluster', filter.cluster - 1)
    }
    if(filter.artist) {
      url.searchParams.append('artist_id', filter.artist)
    }
    if(filter.album) {
      url.searchParams.append('album_id', filter.album)
    }
    let result = await fetch(url);
    result = await result.json();
    result = result.map((item)=>({
      name: item.name,
      id : item.id ,
      album: item.album,
      album_id: item.album_id,
      artist_id: item.artists[0].id,
      artists: item.artists.map(artist => artist.name),
      duration: `${item.duration_minutes}:${item.duration_seconds}` ,
      preview_url : item.preview_url , 
      cluster : item.cluster + 1,
      is_present: item.is_present,
      emotion : item.emotion,
      })
    )
    return result
  }

  const emotion_labels = {
    "All": 6,
    "Sadness": 4,
    "Joy": 2,
    "Anger": 0,
    "Fear": 1,
    "Love": 3,
    "Surprise": 5,
  }

  const emotionRadioBoxes = Object.keys(emotion_labels).map((emotion) => (
      <FormControlLabel
        value={emotion}
        key={emotion}
        control={<Radio />}
        label={emotion}
        labelPlacement="end"
      />
  ))

  const clusterRadioBoxes = [0,1,2,3,4,5,6,7].map((cluster) => (
    <FormControlLabel
      value={cluster}
      key={cluster}
      control={<Radio />}
      label={(cluster == 0) ? 'All' : `Group ${cluster}`}
      labelPlacement="end"
    />
))

  React.useEffect(() => {
    let active = true;

    (async () => {
      if(openFilter) { 
        return () => {
          active = false;
        };
      }
      setLoading(true);
      
      let newItems = await loadServerRows();
      if (!active) {
        return;
      }
      setItems(newItems)
      setLoading(false);
    })();

    return () => {
      active = false;
    };
  },  [page, openFilter]);

  function handleClick(val) {
    if(val.field == 'artists')
      window.location.href = `/artist/${val.row.artist_id}`;
    else if(val.field == 'album')
      window.location.href = `/album/${val.row.album_id}`;
    else if(val.field != 'preview_url' && val.field != 'is_present')
    window.location.href = `/track/${val.row.id}`;
    
  }

  function exportToPlaylist() {
    setLoading(true);
    let track_ids = items.map(item => item.id)
    let name = 'EmotiTune'
    console.log(filter)
    if(filter.cluster && (filter.cluster > 0))
      name += `_${filter.cluster}`
    if(filter.emotion && (filter.emotion != 'All'))
      name += `_${filter.emotion}`
    if(filter.artist) {
      let artist = items[0].artists
      name += `_${artist}`
    }
    if(filter.album) {
      let album = items[0].album
      name += `_${album}`
    }
    fetch('/api/songs/export/', {
      method: 'POST',
      body: JSON.stringify({ track_ids, name }),
      headers: {
        'Content-Type': 'application/json',
      },
    }).then(res => res.json()).then((playlist_id) => {
      setLoading(false);
      window.open(`https://open.spotify.com/playlist/${playlist_id}/`,'blank_')     
    })
  }
  return (
    <Grid container spacing={3}>
      <Modal
        open={openFilter}
        onClose={handleFilterClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={filterStyle}>
        <FormControlLabel
        value="byUser"
        control={<Checkbox checked={filter.by_user} onChange={handleByUser}/>}
        label="Added by me"
        labelPlacement="end"
      />
      <FormLabel component="legend">Emotion</FormLabel>
         <RadioGroup
          row
          aria-label="emotion"
          name="emotion"
          value={filter.emotion || 'All'}
          onChange={handleEmotion}
         >
           {emotionRadioBoxes}
          </RadioGroup>
         <FormLabel component="legend">Cluster</FormLabel>
         <RadioGroup
          row          
          aria-label="cluster"
          name="cluster"
          value={filter.cluster || 0 }
          onChange={handleCluster}
         >
           {clusterRadioBoxes}
         </RadioGroup>
        </Box>
      </Modal>
      <Grid item xs={12} align="end" style={{ marginRight: '3%', padding: 0 }}>
      <FormGroup row style={{ justifyContent: "end" }}>
      <Button onClick={exportToPlaylist} style={{ visibility: (filter.by_user && items.length > 0 && (!openFilter)) ? 'visible' : 'hidden' }}>Create Playlist</Button>
      <Button onClick={handleFilterOpen}>Filter</Button>
      </FormGroup>
      </Grid>
     <Grid item xs={12} align="center">
      <div style={{ display: 'flex', height: '100%', width: "100%" }}>
      {/* <div style={{ height: 300, marginLeft: 300, flexGrow: 1 }}  > */}
      <div style={{ height: '65vh', marginLeft: '1%', flexGrow: 1 }}>
        <DataGrid className="center"
          rows={items}
          columns={columns}
          pagination
          pageSize={25}
          rowsPerPageOptions={[25]}
          onCellClick={handleClick}
          rowCount={filter.by_user ? 20 : numRows } // this is actually dummy count
          paginationMode="server"
          onPageChange={(newPage) => handlePageChange(newPage)}
          loading={loading}
        />
        </div>
        </div>
      </Grid>
      </Grid>
  );
}
