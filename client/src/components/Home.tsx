import React from "react";
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import { Bar } from "./Bar";
import { Search } from "./Search";
import { AdvancedSearch } from "./AdvancedSearch";
import BackgroundImage from "images/podcast.jpg";

const useStyles = makeStyles({
  background: {
    backgroundImage: `url(${BackgroundImage})`,
    backgroundSize: "cover",
    backgroundRepeat: "no-repeat",
    backgroundPosition: "bottom",
  },
  layer: {
    position: "absolute",
    top: 0,
    bottom: 0,
    left: 0,
    right: 0,
  },
  overlay: {
    backgroundColor: "rgba(73, 187, 111, 0.9)",
    zIndex: 10,
  },
});

export const Home = () => {
  const classes = useStyles();
  return (
    <Container>
      <div className={`${classes.layer} ${classes.overlay}`}>
        <Bar barHeight={25}>
          <Typography variant="h1">Spotify Podcast Search</Typography>
        </Bar>
        <Bar barHeight={25}>
          <Search />
        </Bar>
        <Bar barHeight={25}>
          <AdvancedSearch />
        </Bar>
      </div>
      <div className={`${classes.layer} ${classes.background}`} />
    </Container>
  );
};
