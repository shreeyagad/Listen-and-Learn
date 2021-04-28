import React, { useState } from "react";
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import { Bar } from "./Bar";
import { Search } from "./Search";
import { AdvancedSearch } from "./AdvancedSearch";
import { ResultsCard } from "./ResultsCard";
import { searchPodcasts, ShowData } from "api";
import BackgroundImage from "images/podcast.jpg";

const useStyles = makeStyles({
  main: {
    background: `linear-gradient(0deg, rgba(73, 187, 111, 0.9), rgba(73, 187, 111, 0.9)), url(${BackgroundImage})`,
    backgroundAttachment: "fixed",
    backgroundSize: "cover",
    backgroundRepeat: "no-repeat",
    backgroundPosition: "bottom",
    minHeight: "100%",
    minWidth: "100%",
  },
});

export const Home = () => {
  const classes = useStyles();
  const [query, setQuery] = useState("");
  const [dataResults, setData] = useState<Array<ShowData> | null>(null);

  const searchCallback = async (
    duration: Date | null,
    genres: Array<string>,
    publisher: string | null,
    year: Date | null
  ) => {
    const results = await searchPodcasts(
      query,
      duration,
      genres,
      publisher,
      year
    );
    setData(results);
  };

  return (
    <Container disableGutters className={classes.main}>
      <Bar barHeight={25}>
        <Typography variant="h1">Spotify Podcast Search</Typography>
      </Bar>
      <Bar barHeight={25}>
        <Search query={query} setQuery={setQuery} />
      </Bar>
      <Bar barHeight={25}>
        <AdvancedSearch searchCallback={searchCallback} />
      </Bar>
      {dataResults?.map((result) => {
        return (
          <Bar key={result.episode_id} barHeight={25}>
            <ResultsCard result={result} />{" "}
          </Bar>
        );
      })}
    </Container>
  );
};
