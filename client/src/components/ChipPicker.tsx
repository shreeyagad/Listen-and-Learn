import React from "react";
import Select from "@material-ui/core/Select";
import Chip from "@material-ui/core/Chip";
import Input from "@material-ui/core/Input";
import InputLabel from "@material-ui/core/InputLabel";
import MenuItem from "@material-ui/core/MenuItem";
import FormControl from "@material-ui/core/FormControl";
import { makeStyles, Theme, useTheme } from "@material-ui/core/styles";

export interface ChipProps {
  dropdownValues: Array<string>;
  genres: Array<string>;
  setGenres: (val: Array<string>) => void;
}

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

const getStyles = (item: string, selected: Array<string>, theme: Theme) => {
  return {
    fontWeight:
      selected.indexOf(item) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  };
};

const useStyles = makeStyles({
  formControl: {
    minWidth: 167,
    maxWidth: 300,
  },
  chips: {
    display: "flex",
    flexWrap: "wrap",
  },
  chip: {
    fontSize: 12,
    margin: 2,
    height: 20,
  },
});

export const ChipPicker = ({
  dropdownValues,
  genres,
  setGenres,
}: ChipProps) => {
  const classes = useStyles();
  const theme = useTheme();

  return (
    <FormControl className={classes.formControl}>
      <InputLabel id="multiple-chip-label">Genres</InputLabel>
      <Select
        labelId="multiple-chip-label"
        id="multiple-chip"
        multiple
        value={genres}
        onChange={(event) => setGenres(event.target.value as Array<string>)}
        input={<Input id="select-multiple-chip" />}
        renderValue={(selected: any) => (
          <div className={classes.chips}>
            {selected.map((value: any) => (
              <Chip key={value} label={value} className={classes.chip} />
            ))}
          </div>
        )}
        MenuProps={MenuProps}
      >
        {dropdownValues.map((item) => (
          <MenuItem
            key={item}
            value={item}
            style={getStyles(item, genres, theme)}
          >
            {item}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};
