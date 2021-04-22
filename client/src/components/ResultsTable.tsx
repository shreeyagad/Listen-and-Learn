import React from "react";
import _ from "lodash";
import getYear from "date-fns/getYear";
import parse from "date-fns/parse";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";
import { ResponseObject } from "api";

export interface ResultsTableProps {
  results: Array<ResponseObject>;
}

const useStyles = makeStyles({
  table: {
    margin: "auto",
  },
});

const getDurationString = (duration: number) => {
  const seconds = duration / 1000;
  const minutes = _.floor(seconds / 60);
  const secs = _.floor(seconds % 60);
  return `${minutes}:${_.padStart(secs.toString(), 2, "0")}`;
};

export const ResultsTable = ({ results }: ResultsTableProps) => {
  const classes = useStyles();
  return (
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Description</TableCell>
            <TableCell>Genres</TableCell>
            <TableCell>Duration</TableCell>
            <TableCell>Year</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {results.map((row) => (
            <TableRow key={row.name}>
              <TableCell component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell>{row.description}</TableCell>
              <TableCell>{row.genres.join(", ")}</TableCell>
              <TableCell>{getDurationString(row.duration_ms)}</TableCell>
              <TableCell>
                {getYear(parse(row.release_date, "yyyy-MM-dd", new Date()))}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
