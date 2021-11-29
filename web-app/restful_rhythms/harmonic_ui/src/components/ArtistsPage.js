import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';


export default function ServerPaginationGrid() {
  
  const columns = [
    { field: 'id', headerName: 'ID', width: 150 , hide:true},
    { field: 'name', headerName: 'Artist', width: 150, headerAlign: 'center'},
    { field: 'track_id', headerName: 'Track ID', width: 150 , hide:true}
  ];

  const [page, setPage] = React.useState(0);
  const [loading, setLoading] = React.useState(false);
  const [items, setItems] = React.useState([]);
  const [pageEnd, setPageEnd] = React.useState([]);

  async function loadServerRows() {
    fetch("api/artists")
      .then(res => res.json())
      .then(
        (result) => {
          console.log(result)
          result = result.map((item)=>({
            id : item.id,
            name : item.name,
            track_id : item.track_id,
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

    //   loadServerRows();

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
          Artists
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
      </Grid>
  );
}
