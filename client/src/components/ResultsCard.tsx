import React, { useState } from "react";
import parse from "html-react-parser";
import { makeStyles } from "@material-ui/core/styles";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import CardActions from "@material-ui/core/CardActions";
import CardMedia from "@material-ui/core/CardMedia";
import Typography from "@material-ui/core/Typography";
import { green } from "@material-ui/core/colors";
import { DetailModal } from "./DetailModal";
import DefaultPodcast from "images/defaultPodcast.png";
import SpotifyLogo from "images/spotify.png";
import { ShowData } from "api";
import boldify from "util/boldify";

export interface ResultsCardProps {
  result: ShowData;
  query: string;
}

const useStyles = makeStyles({
  root: {
    padding: "20px",
    position: "relative",
    width: "60%",
  },
  avatar: {
    position: "absolute",
    top: 0,
    right: 0,
    margin: "10px",
    backgroundColor: green[500],
  },
  actions: {
    flexDirection: "row-reverse",
  },
  button: {},
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
    marginRight: "4px",
  },
});

export const ResultsCard = ({ result, query }: ResultsCardProps) => {
  const classes = useStyles();
  const [open, setOpen] = useState(false);

  return (
    <React.Fragment>
      <Card className={classes.root}>
        <Avatar className={classes.avatar}>
          {Math.trunc(result.sim_score)}
        </Avatar>
        <div className={classes.row}>
          <CardMedia
            className={classes.cover}
            image={result.images ? result.images[0].url : DefaultPodcast}
            title="Live from space album cover"
          />
          <div className={classes.content}>
            <Typography variant="h4">
              {parse(boldify(result.episode_name, query))}
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
                />
                <Typography variant="subtitle2" color="textSecondary">
                  SPOTIFY
                </Typography>
              </a>
            </div>
          </div>
        </div>
        <div className={classes.row} style={{ marginTop: "10px" }}>
          <Typography variant="body1">
            {parse(boldify(result.episode_description, query))}
          </Typography>
        </div>
        <CardActions className={classes.actions}>
          <Button
            onClick={() => setOpen(true)}
            variant="contained"
            color="primary"
          >
            Learn More
          </Button>
        </CardActions>
      </Card>
      <DetailModal open={open} setOpen={setOpen} show={result} query={query} />
    </React.Fragment>
  );
};
