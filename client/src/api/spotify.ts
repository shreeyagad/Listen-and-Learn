import { spotifyAPI, spotifyAccounts } from "api";
import qs from "qs";

interface AuthResult {
  access_token: string;
  token_type: string;
  expires_in: number;
}

interface Show {
  available_markets: string[];
  copyrights: {
    text: string;
    type: string;
  }[];
  description: string;
  explicit: boolean;
  external_urls: {
    spotify: string;
  };
  href: string;
  id: string;
  images: {
    height: number;
    url: string;
    width: number;
  }[];
  is_externally_hosted: boolean;
  languages: string[];
  media_type: string;
  name: string;
  publisher: string;
  type: string;
  uri: string;
}

const getAuthToken = async (): Promise<AuthResult> => {
  const spotifyCredentials = process.env.REACT_APP_SPOTIFY_AUTH;
  const result = await spotifyAccounts.post<AuthResult>(
    "token",
    qs.stringify({
      grant_type: "client_credentials",
    }),
    {
      headers: {
        Authorization: `Basic ${spotifyCredentials}`,
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );
  return result.data;
};

export const searchShowsByIDs = async (ids: string[]) => {
  const authToken = await getAuthToken();
  return spotifyAPI.get<{ shows: Show[] }>("shows", {
    params: {
      ids: ids.join(","),
      market: "US",
    },
    headers: {
      Authorization: `${authToken.token_type} ${authToken.access_token}`,
    },
  });
};
