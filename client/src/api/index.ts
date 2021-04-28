import axios from "axios";

export * from "./search";
export * from "./spotify";

export const spotifyAccounts = axios.create({
  baseURL: "https://accounts.spotify.com/api/",
});

export const spotifyAPI = axios.create({
  baseURL: "https://api.spotify.com/v1/",
});

export default axios.create({
  baseURL: "http://listen-and-learn.herokuapp.com/",
});
