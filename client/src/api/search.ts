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
  show_rank: string;
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
    publisher: response.publisher,
    release_date: response.release_date,
    show_id: response.show_id,
    show_rank: response.show_rank,
  };
};

export const searchPodcasts = async (
  query: string,
  duration: Date | null,
  genres: Array<string>,
  publisher: string | null,
  year: Date | null
): Promise<ShowData[]> => {
  const durationString = duration ? format(duration, "HH:mm") : duration;
  const yearString = year ? format(year, "yyyy") : year;
  const serverResponse = await api.post<Array<Response>>("search", {
    query,
    duration: durationString,
    genres,
    publisher,
    year: yearString,
  });
  const responseObj = serverResponse.data.map((obj) => {
    return parseResponse(obj);
  });

  // const serverResponse: ResponseObject[] = [
  //   {
  //     episode_id: "5xINVuo9jiWAuv0sxJ8QkN",
  //     show_id: "78PyQphowySboNLN1tb9mP",
  //     episode_name: "7: Our New Member - Chuckle Sandwich Podcast",
  //     episode_description:
  //       "The Boys reveal the new member of the podcast, will he survive the test of glory?",
  //     duration_ms: 3743164,
  //     genres: ["Comedy"],
  //     publisher: "Chuckle Sandwich",
  //     release_date: "2021-03-13",
  //     show_rank: "6",
  //   },
  //   {
  //     episode_id: "0CGd5Gq60pbHgGPmteiTxh",
  //     show_id: "7gozmLqbcbr6PScMjc0Zl4",
  //     episode_name: "#173 The Test Kitchen, Chapter 2",
  //     episode_description:
  //       "Chapter 2, “Glass Office”: Years later, in 2018, a new wave of people of color arrives at Bon Appétit. And when their white bosses don’t understand the problems they’re facing, those people will decide to fix the place themselves.  Check out: Jesse Sparks’ portfolio Elyse Inamine’s Instagram Ryan Walker-Hartshorn’s website and Twitter A reported story by Priya Krishna Christina Chaey’s 2016 manifesto following Bon Appétit’s pho video release. And here’s Christina’s Instagram. Learn more about your ad choices. Visit megaphone.fm/adchoices",
  //     duration_ms: 2991334,
  //     genres: ["Technology", "Comedy"],
  //     publisher: "Gimlet",
  //     release_date: "2021-02-12",
  //     show_rank: "6",
  //   },
  //   {
  //     episode_id: "6xleEgZXLj1DklEnb1rI2A",
  //     show_id: "7gozmLqbcbr6PScMjc0Zl4",
  //     episode_name: "#172 The Test Kitchen, Chapter 1",
  //     episode_description:
  //       "Chapter 1, “Original Sin”: In the summer of 2020, Bon Appétit faced an online reckoning. It imploded, seemingly overnight, former employees calling it a racist and toxic workplace. But the story of what actually happened there started ten years earlier.   Here are some recipes to try from the people featured in this week’s story: Yewande Komolafe’s\xa0yam and plantain curry with crispy shallots\xa0and\xa0sheet-pan gochujang chicken.\xa0 Sue Li’s\xa0caramelized onion galette\xa0and\xa0creamy turmeric pasta. Rick Martinez’s\xa0mole sencillo. Eleanore Park’s\xa0ginger-scallion meatballs with lemony farro. Also, you can read Rachel Premack’s breaking story on Bon Appétit from last summer\xa0here. Learn more about your ad choices. Visit megaphone.fm/adchoices",
  //     duration_ms: 3560359,
  //     genres: ["Technology"],
  //     publisher: "Gimlet",
  //     release_date: "2021-02-04",
  //     show_rank: "6",
  //   },
  //   {
  //     episode_id: "6916aBtwOEBJpRFNnOequC",
  //     show_id: "1HhK3f5Fk2EBplKMLvYVnQ",
  //     episode_name: "WeWow Earth Week Day 3: Create & Test",
  //     episode_description:
  //       "It's day 3 of WeWow--Time to create and experiment our Earth Week Podject",
  //     duration_ms: 688196,
  //     genres: ["Kids & Family"],
  //     publisher: "Tinkercast",
  //     release_date: "2021-04-21",
  //     show_rank: "7",
  //   },
  //   {
  //     episode_id: "6JgtKz9DgwgStXq5rUthuA",
  //     show_id: "0A3IirSc3Qi2MSFJcz2unj",
  //     episode_name: "Episode 2: Bene and The Gesserits",
  //     episode_description:
  //       "As we continue our quest deeper into the spicy world of Dune, Henry and Holden peel back the curtain on the mysterious society of The Fremen and we learn how Paul and Jessica survive their escape into the desert wastelands of Arrakis.  | Dune Theater Cast | HENRY ZEBROWSKI as EMPEROR BARON HARKONNEN | HOLDEN MCNEELY as THE EMPERORS PERSONAL TAYLOR |  Kevin MacLeod (incompetech.com) Licensed under Creative Commons: By Attribution 3.0 License creativecommons.org/licenses/by/3.0",
  //     duration_ms: 3812153,
  //     genres: ["Tv & Film"],
  //     publisher: "The Last Podcast Network",
  //     release_date: "2021-03-22",
  //     show_rank: "1",
  //   },
  // ];
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
