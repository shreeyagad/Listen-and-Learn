import api, { searchShowsByIDs } from "api";
import format from "date-fns/format";

interface Response {
  description: string;
  duration_ms: number;
  genres: Array<string>;
  id: string;
  name: string;
  publisher: string;
  release_date: string;
  show_id: string;
  show_num_reviews: number;
  show_rank: string;
  sim_score: number;
}

export interface ResponseObject {
  episode_description: string;
  duration_ms: number;
  genres: Array<string>;
  episode_id: string;
  episode_name: string;
  publisher: string;
  release_date: string;
  show_id: string;
  num_reviews: number;
  show_rank: string;
  sim_score: number;
}

export interface ShowData extends ResponseObject {
  show_description: string;
  images: {
    height: number;
    url: string;
    width: number;
  }[];
  show_name: string;
}

const parseResponse = (response: Response): ResponseObject => {
  return {
    episode_description: response.description,
    duration_ms: response.duration_ms,
    genres: response.genres,
    episode_id: response.id,
    episode_name: response.name,
    num_reviews: response.show_num_reviews,
    publisher: response.publisher,
    release_date: response.release_date,
    show_id: response.show_id,
    show_rank: response.show_rank,
    sim_score: response.sim_score,
  };
};

export const searchPodcasts = async (
  query: string,
  duration: Date | null,
  genres: Array<string>,
  publisher: string | null,
  year: Date | null
): Promise<ShowData[]> => {
  if (query.trim() === "") return [];
  const durationString = duration ? format(duration, "HH:mm") : duration;
  const yearString = year ? format(year, "yyyy") : year;
  const serverResponse = await api.post<Array<Response>>("search", {
    query,
    duration: durationString,
    genres,
    publisher,
    year: yearString,
  });
  if (serverResponse.data.length === 0) return [];
  const responseObj = serverResponse.data.map((obj) => {
    return parseResponse(obj);
  });

  const ids = responseObj.map((obj) => {
    return obj.show_id;
  });
  const { data } = await searchShowsByIDs(ids);
  const shows: ShowData[] = data.shows.map((show, idx) => {
    const serverObj = responseObj[idx];
    const picked = {
      show_description: show.description,
      images: show.images,
      show_name: show.name,
    };
    return Object.assign(serverObj, picked);
  });
  return shows;
};
