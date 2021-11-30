import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Button, Grid } from '@material-ui/core';
import Typography from "@material-ui/core/Typography";
import Box from '@mui/material/Box';


export default function ServerPaginationGrid() {
  
  const columns = [
    { field: 'name', headerName: 'Artist', width: 1000, filterable: false, sortable: false },
  ];

  const [page, setPage] = React.useState(0);
  const [loading, setLoading] = React.useState(false);
  const [items, setItems] = React.useState([]);
  const [prevItem, setPrevItem] = React.useState(null);
  const [nextItem, setNextItem] = React.useState(null);
  const [prevPage, setPrevPage] = React.useState(0);
  
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

  async function loadServerRows() {
    let url = new URL(`http://${window.location.hostname}:8000/api/artists`)
    if (prevItem) {
      url.searchParams.append('prevId', prevItem)
    } else if(nextItem) {
      url.searchParams.append('nextId', nextItem)   
    }
    let result = await fetch(url)
    result = await result.json()
    result = result.map((item)=>({
            id : item.id,
            name : item.name
            })
        )
    return result;
  }

  React.useEffect(() => {
    let active = true;

    (async () => {
      setLoading(true);

    const newItems = await loadServerRows();

      if (!active) {
        return;
      }
      setItems(newItems);
      setLoading(false);
    })();

    return () => {
      active = false;
    };
  },[page]);

  function handleClick(val) {
    window.location.href = `/artist/${val.row.id}`;
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} align="center">
      <Box sx={{ p: 3}}>
        <Typography component="h2" variant="h2">
          Artists and Bands
          </Typography>
          </Box>
      </Grid>
      <Grid item xs={12} align="center">
      <div style={{ display: 'flex', height: '80vh' }}>
      <div style={{ height: '100%', flexGrow: 1 }}  >
        <DataGrid className="center"
          rows={items}
          columns={columns}
          pagination
          onCellClick={handleClick}
          pageSize={25}
          rowsPerPageOptions={[25]}
          rowCount={Math.round((Math.random() * 200000))}
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
