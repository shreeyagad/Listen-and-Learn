import collections
import numpy as np
import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET')))


## Use Chartable & BeautifulSoup to get top (podcast) shows on Spotify
chartable_url = 'https://chartable.com/charts/spotify/us'
page = requests.get(chartable_url, headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'})
page_soup = BeautifulSoup(page.content, 'html.parser')
charts_by_genre = page_soup.find_all('div', class_='podcast mb1')
chart_urls = [chart.find('a')['href'] for chart in charts_by_genre]
chart_urls = chart_urls[:-3] + [chart_urls[-1]] # remove "top podcasts" and "trending podcasts"
num_urls = len(chart_urls)


## For each genre, append all of its page urls
def add_next_pages(chart_indices):
    for i in chart_indices:
        temp_chart_url = chart_urls[i]
        while temp_chart_url:
            chart_page = requests.get(temp_chart_url, headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'})
            if (chart_page.status_code != 200):
                return i
            next_page = BeautifulSoup(chart_page.content, 'html.parser').find('span', class_='next')
            if next_page:
                temp_chart_url = 'http://chartable.com' + next_page.find('a')['href']
                next_page_urls.append(temp_chart_url)
            else:
                temp_chart_url = None
    return -1


## Need to load data incrementally due to request limit
next_page_urls = []
def load_next_pages():
    i = 0
    while i != -1:
        i = add_next_pages(range(i, num_urls))
    chart_urls += next_page_urls


## Get show titles using chart urls from Chartable
def collect_shows(chart_indices):
    for i in chart_indices:
        chart_url = chart_urls[i]
        chart_page = requests.get(chart_url, headers = {'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'})
        if (chart_page.status_code != 200):
            return i

        show_soup = BeautifulSoup(chart_page.content, 'html.parser')
        all_shows = show_soup.find_all('tr', class_='striped--near-white')

        key = ' '.join(((chart_url.split('/')[-1]).split('-'))[4:])
        genre_data_load[key] = len(all_shows)

        for show in all_shows:
            show_name = show.find('a', class_='link blue')
            show_rank = show.find('div', class_='b header-font f2 tc')
            if not show_name:
                show_name = show.find('div', class_='title f4')
            genre = key.split('?')[0]
            genres_to_shows[genre].append({"show_name": show_name.text, "rank": show_rank.text})
    return -1


## Need to load data incrementally due to request limit
genres_to_shows = collections.defaultdict(list)
def load_shows_from_chartable(chart_urls):
    i = 0
    while i != -1:
        i = collect_shows(range(i, num_urls))
    np.save('data/chartable_genres_to_shows.npy', genres_to_shows) 


# Get all shows
def get_all_shows():
    shows = dict()
    genres_to_shows = np.load('data/chartable_genres_to_shows.npy', allow_pickle='TRUE').item()
    for genre, show_data in genres_to_shows.items():
        for show in show_data:
            try: 
                show_name, rank = show['show_name'], show['rank']
                results = sp.search(q=show_name, type='show', market='US')
                show = results['shows']['items'][0]
                if (show['languages'] == ['en'] or show['languages'] == ['en-US']):
                    new_show = {
                        "id": show['id'],
                        "name": show['name'],
                        "description": show['description'],
                        "genre": genre,
                        "languages": show['languages'],
                        "publisher": show['publisher'],
                        "show_rank": rank
                    }
                    shows[new_show['id']] = new_show
            except:
                continue
    np.save('data/shows.npy', shows) 


# GET ALL EPISODES
def get_all_episodes():
    episodes = dict()
    shows = np.load('data/shows.npy', allow_pickle='TRUE').item()
    for show_id in shows.keys():
        try: 
            results = sp.show_episodes(show_id, limit=50, offset=0, market='US')
            episode_items = results['items']
            for episode in episode_items:
                new_episode = {
                    "id": episode['id'],
                    "show_id": show_id,
                    "name": episode['name'],
                    "description": episode['description'],
                    "duration_ms": episode['duration_ms'],
                    "genre": shows[show_id]['genre'],
                    "publisher": shows[show_id]['publisher'],
                    "release_date": episode['release_date'],
                    "show_rank": shows[show_id]['show_rank']
                }
                episodes[episode['id']] = new_episode
        except:
            continue

    np.save('data/episodes.npy', episodes) 


if __name__ == "__main__":
    shows = np.load('data/shows.npy', allow_pickle='TRUE').item()
    episodes = np.load('data/episodes.npy', allow_pickle='TRUE').item()
    print(f"There are {len(shows)} shows and {len(episodes)} episodes in our dataset.")

    # TODO: Create TFIDF vector representations of episode descriptions
