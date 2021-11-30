import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import Grid from '@mui/material/Grid';
import {
    Link
  } from "react-router-dom";
 
const pages = [
    { name: 'Tracks', link: '/welcome' },
    { name: 'Artists',link: '/artists' },
    { name: 'VCMusic' },
    { name: 'Albums',link: '/albums' },
    { name: 'Import Tracks',link: '/search' }
]
    
const settings = ['Profile', 'Account', 'Dashboard', 'Logout'];

const NavBar = (props) => {
  return (
    <AppBar position="static" color="transparent" sx={{ boxShadow: "0px 0px 0px #9E9E9E", border: "none", marginTop: '0.5%' }}>
      <Container maxWidth="xl">
          <Grid container alignItems="center" justifyContent="center" spacing={4}>
            {pages.map((page) => {
            if(page.name == 'VCMusic') {
                return (<Grid item align="center" xs>
                        <Typography
            noWrap
            variant="h6"
            color="secondary"
            component="div"
            sx={{ flexGrow: 1, display: {  color: 'black' } }}
          >
            EMOTI-TUNE
          </Typography>
                    </Grid>);
         
            }
            return (<Grid item align="center" xs>
              <Button
                key={page.name}
                variant="text"
                to={page.link} component={Link}
                sx={{ my: 2, color: 'white', display: 'block', color: (props.active == page.name) ? 'primary.main' : 'text.primary' }}
              >
                {page.name}
              </Button>
            </Grid>
            )})}
          </Grid>
      </Container>
    </AppBar>
  );
};
export default NavBar;
