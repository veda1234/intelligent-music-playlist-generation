import React, { Component } from "react";
import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
// import InfiniteScroll from 'react-infinite-scroll-component'

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));

export default class WelcomePage extends Component {
  constructor(props) {
    super(props);
    this.songs = this.songs.bind(this)
    this.state = { data:[]}
    this.songs()
    console.log(this.state.data)

  }
  songs(){
    fetch("api/songs").then((response) => response.json())
    .then((data) => {
      this.setState({ data: data });
    }
    
    );
  }

  render() {
    return (
      <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell>Name</StyledTableCell>
            <StyledTableCell>Artist</StyledTableCell>
            <StyledTableCell>Duration</StyledTableCell>
            <StyledTableCell>Preview URL</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {this.state.data.map((data) => (
            <StyledTableRow
              key={data.name}
              sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
            >
              <StyledTableCell component="th" scope="row">
                {data.name}
              </StyledTableCell>
              <StyledTableCell>{data.artists}</StyledTableCell>
              <StyledTableCell>{data.duration_minutes}:{data.duration_seconds}</StyledTableCell>
              <StyledTableCell><a href={data.preview_url} target='_blank' rel='noopener noreferrer'>{data.preview_url}</a></StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
    );
  }
}