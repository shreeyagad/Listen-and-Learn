import React from "react";
import TextField from "@material-ui/core/TextField";
import { makeStyles } from "@material-ui/core/styles";
import SearchIcon from "@material-ui/icons/Search";

export interface SearchProps {
  query: string;
  setQuery: (val: string) => void;
}

const useStyles = makeStyles({
  icon: {
    color: "white",
    padding: "0 10px",
  },
  search: {
    alignItems: "center",
    borderRadius: "4px",
    background: "#3b9e66",
    display: "flex",
    width: "28.75rem",
  },
});

const inputStyles = {
  disableUnderline: true,
  style: {
    color: "white",
  },
};

export const Search = ({ query, setQuery }: SearchProps) => {
  const classes = useStyles();

  return (
    <div className={classes.search}>
      <SearchIcon className={classes.icon} />
      <TextField
        fullWidth
        margin="normal"
        placeholder="Enter a query (ex: how to invest in stocks)"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        InputProps={inputStyles}
      />
    </div>
  );
};
