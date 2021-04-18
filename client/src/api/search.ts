import api from "api";
import format from "date-fns/format";

export interface ResponseObject {
  description: string;
  duration_ms: number;
  genre: string;
  id: string;
  name: string;
  publisher: string;
  release_date: string;
  show_id: string;
  show_rank: string;
}

export const searchPodcasts = async (
  query: string,
  duration: Date | null,
  genres: Array<string>,
  publisher: string | null,
  year: Date | null
) => {
  const durationString = duration ? format(duration, "HH:mm") : duration;
  const yearString = year ? format(year, "yyyy") : year;
  const { data } = await api.post<Array<ResponseObject>>("search", {
    query,
    duration: durationString,
    genres,
    publisher,
    year: yearString,
  });
  return data;
};
