import React from "react";
import parseHTML from "html-react-parser";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardMedia from "@material-ui/core/CardMedia";
import Chip from "@material-ui/core/Chip";
import Typography from "@material-ui/core/Typography";
import parse from "date-fns/parse";
import getYear from "date-fns/getYear";
import DefaultPodcast from "images/defaultPodcast.png";
import SpotifyLogo from "images/spotify.png";
import { ShowData } from "api";
import boldify from "util/boldify";

export interface DetailCardProps {
  result: ShowData;
  query: string;
}

const useStyles = makeStyles({
  root: {
    padding: "20px",
    width: "80%",
  },
  actions: {
    flexDirection: "row-reverse",
  },
  row: {
    marginLeft: 0,
    marginRight: 0,
    display: "flex",
    flexWrap: "wrap",
    flexDirection: "row",
  },
  iconRow: {
    alignItems: "center",
    marginTop: "8px",
    textDecoration: "none",
  },
  content: {
    padding: "0px",
    paddingLeft: "12px",
  },
  details: {
    display: "flex",
    flexDirection: "column",
  },
  cover: {
    width: "100px",
    height: "100px",
  },
  publisher: {
    paddingLeft: "4px",
    fontWeight: 500,
  },
  spotifyLogo: {
    height: "20px",
    width: "20px",
  },
  genreBox: {
    display: "flex",
    flexDirection: "column-reverse",
  },
});

export const DetailCard = ({ result, query }: DetailCardProps) => {
  const classes = useStyles();

  return (
    <Card className={classes.root}>
      <div className={classes.row}>
        <CardMedia
          className={classes.cover}
          image={result.images ? result.images[0].url : DefaultPodcast}
          title="Podcast cover"
        />
        <div className={classes.content}>
          <Typography variant="h4">
            {parseHTML(boldify(result.episode_name, query))}
          </Typography>
          <div className={classes.row}>
            <Typography variant="subtitle1" color="textSecondary">
              By
            </Typography>
            <Typography
              className={classes.publisher}
              variant="subtitle1"
              color="textSecondary"
            >
              {result.publisher}
            </Typography>
          </div>
          <div className={classes.row}>
            <a
              className={`${classes.row} ${classes.iconRow}`}
              href={`https://open.spotify.com/episode/${result.episode_id}`}
              target="_blank"
              rel="noreferrer"
            >
              <img
                alt="Spotify logo"
                className={classes.spotifyLogo}
                src={SpotifyLogo}
                style={{ marginRight: "4px" }}
              />
            </a>
            <Typography style={{ padding: "0px 8px", marginTop: "8px" }}>
              {`${Math.ceil(result.duration_ms / 60000)} mins`}
            </Typography>
            <Typography style={{ padding: "0px 8px", marginTop: "8px" }}>
              {`Number of reviews: ${result.num_reviews}`}
            </Typography>
          </div>
        </div>
        <div className={classes.genreBox}>
          <Typography
            variant="subtitle2"
            color="textSecondary"
            style={{ padding: "5px 0px" }}
          >
            {`Year: ${getYear(
              parse(result.release_date, "yyyy-MM-dd", new Date())
            )}`}
          </Typography>
          <div className={classes.row}>
            <Typography
              variant="subtitle2"
              color="textSecondary"
              style={{ padding: "3px 0px" }}
            >
              Genres:
            </Typography>
            {result.genres.map((genre) => {
              return (
                <Chip
                  key={genre}
                  color="primary"
                  label={genre}
                  variant="outlined"
                  style={{ margin: "0px 4px" }}
                />
              );
            })}
          </div>
        </div>
      </div>
      <div className={classes.row} style={{ marginTop: "10px" }}>
        <Typography variant="body1">
          {parseHTML(boldify(result.episode_description, query))}
        </Typography>
      </div>
      <div className={classes.row} style={{ marginTop: "10px" }}>
        <Typography variant="h5">More About this Podcast</Typography>
      </div>
      <div
        className={classes.row}
        style={{ marginTop: "10px", alignItems: "center" }}
      >
        <Typography variant="h6" style={{ paddingRight: "8px" }}>
          {result.show_name}
        </Typography>
        <a
          href={`https://open.spotify.com/show/${result.show_id}`}
          target="_blank"
          rel="noreferrer"
          style={{ display: "flex", textDecoration: "none" }}
        >
          <img
            alt="Spotify logo"
            className={classes.spotifyLogo}
            src={SpotifyLogo}
            style={{ padding: "0px 8px", marginTop: "3px" }}
          />
          <Typography
            variant="subtitle2"
            color="textSecondary"
            style={{ marginTop: "3px" }}
          >
            SPOTIFY
          </Typography>
        </a>
      </div>
      <div className={classes.row} style={{ marginTop: "10px" }}>
        <Typography variant="body2">
          {parseHTML(boldify(result.show_description, query))}
        </Typography>
      </div>
    </Card>
  );
};
