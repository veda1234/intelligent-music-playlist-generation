import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';
import {
  Link
} from "react-router-dom";


export default function ServerPaginationGrid() {
  
  const columns = [
    { field: 'name', headerName: 'Name', width: 150, headerAlign: 'center'},
    { field: 'id', headerName: 'id', width: 150 , hide:true},
    { field: 'artists', headerName: 'Artist', width: 150, headerAlign: 'center'},
    { field: 'duration_minutes', headerName: 'Duration', width: 150, headerAlign: 'center'},
    { field: 'preview_url', headerName: 'Preview URL', width: 157, headerAlign: 'center'},
    { field: 'cluster', headerName: 'Cluster Number', width: 180, headerAlign: 'center'},
    { field: 'emotion', headerName: 'Emotion detected', width: 190, headerAlign: 'center'}
  ];

  const [page, setPage] = React.useState(0);
  const [loading, setLoading] = React.useState(false);
  const [items, setItems] = React.useState([]);
  const [pageEnd, setPageEnd] = React.useState([]);

  async function loadServerRows() {
    fetch("api/songs")
      .then(res => res.json())
      .then(
        (result) => {
          result = result.map((item)=>({
            name: item.name,
            id : item.id ,
            artists : item.artists ,
            duration_minutes : item.duration_minutes ,
            preview_url : item.preview_url , 
            cluster : item.cluster,
            emotion : item.emotion,
            })
        )
          setItems(result); 
        }
      )
  }

  React.useEffect(() => {
    let active = true;

    (async () => {
      setLoading(true);

      // loadServerRows();

      if (!active) {
        return;
      }

      setLoading(false);
    })();

    return () => {
      active = false;
    };
  });

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} align="center">
      <Box sx={{ p: 3}}>
        <Typography component="h2" variant="h2">
          Songs
          </Typography>
          </Box>
      </Grid>
      <Grid item xs={10} align="center">
      <div style={{ display: 'flex', height: '100%' }}>
      <div style={{ height: 400, marginLeft: 200, flexGrow: 1 }}  >
        <DataGrid className="center"
          rows={items}
          columns={columns}
          pagination
          pageSize={5}
          rowsPerPageOptions={[25]}
          rowCount={100}
          paginationMode="server"
          onPageChange={(newPage) => setPage(newPage)}
          loading={loading}
        />
        </div>
        </div>
      </Grid>
      <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
          <Button color="primary" variant="contained" to="/artists" component={Link}>
          Artist's Page
            </Button>
          </Typography>
          </Grid>
          <Grid item xs={12} align="center">
          <Typography component="h4" variant="h4">
          <Button color="primary" variant="contained" to="/albums" component={Link}>
          Album's Page
            </Button>
          </Typography>
          </Grid>
      </Grid>
  );
}
