import React, { useState } from "react";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import CardActions from "@material-ui/core/CardActions";
import CircularProgress from "@material-ui/core/CircularProgress";
import TextField from "@material-ui/core/TextField";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import { KeyboardTimePicker, KeyboardDatePicker } from "@material-ui/pickers";
import { makeStyles } from "@material-ui/core/styles";
import { ChipPicker } from "./ChipPicker";

export interface AdvancedSearchProps {
  searchCallback: (
    duration: Date | null,
    genres: Array<string>,
    publisher: string | null,
    year: Date | null
  ) => void;
  setLoading: (val: boolean) => void;
  clear: () => void;
  loading: boolean;
}

const genreList = [
  "Arts & Entertainment",
  "Business & Technology",
  "Comedy",
  "Educational",
  "Fiction",
  "Games",
  "Lifestyle & Health",
  "History",
  "Kids & Family",
  "Leisure",
  "Music",
  "News & Politics",
  "Religion & Spirituality",
  "Science",
  "Society & Culture",
  "Sports & Recreation",
  "Stories",
  "TV & Film",
  "Technology",
  "True Crime",
];

const useStyles = makeStyles({
  card: {
    width: "28.75rem",
  },
  searchHeader: {
    paddingBottom: "0.6rem",
  },
  actions: {
    flexDirection: "row-reverse",
  },
});

export const AdvancedSearch = ({
  clear,
  searchCallback,
  setLoading,
  loading,
}: AdvancedSearchProps) => {
  const classes = useStyles();
  const [duration, setDuration] = useState<Date | null>(null);
  const [genres, setGenres] = useState<Array<string>>([]);
  const [publisher, setPublisher] = useState<string | null>(null);
  const [year, setYear] = useState<Date | null>(null);

  const resetFields = () => {
    setYear(null);
    setGenres([]);
    setDuration(null);
    setPublisher(null);
    clear();
  };

  return (
    <Card className={classes.card}>
      <CardContent>
        <Typography className={classes.searchHeader}>
          Advanced Search
        </Typography>
        <Grid container alignItems="flex-end" spacing={3}>
          <Grid item xs={6}>
            <KeyboardTimePicker
              ampm={false}
              autoOk
              label="Duration (hh:mm)"
              value={duration}
              variant="inline"
              onChange={setDuration}
            />
          </Grid>
          <Grid item xs={6}>
            <ChipPicker
              dropdownValues={genreList}
              genres={genres}
              setGenres={setGenres}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              label="Publisher"
              value={publisher || ""}
              onChange={(e) => setPublisher(e.target.value)}
            />
          </Grid>
          <Grid item xs={6}>
            <KeyboardDatePicker
              autoOk
              views={["year"]}
              label="Year"
              value={year}
              maxDate={new Date()}
              onChange={setYear}
            />
          </Grid>
        </Grid>
      </CardContent>
      <CardActions className={classes.actions}>
        <Button
          onClick={() => {
            searchCallback(duration, genres, publisher, year);
            setLoading(true);
          }}
          variant="contained"
          color="primary"
        >
          {loading ? (
            <CircularProgress
              style={{ height: 30, width: 30 }}
              color="secondary"
            />
          ) : (
            "Search"
          )}
        </Button>
        <Button onClick={resetFields}>Reset</Button>
      </CardActions>
    </Card>
  );
};
