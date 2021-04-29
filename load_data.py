import collections
import numpy as np
from gevent import monkey
monkey.patch_all()
import requests
import os
import boto3
import json
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.feature_extraction.text import TfidfVectorizer
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.models.helpers import json_numpy_obj_hook

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
                                                           client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET')))


# Use Chartable & BeautifulSoup to get top (podcast) shows on Spotify
chartable_url = 'https://chartable.com/charts/spotify/us'
page = requests.get(chartable_url, headers={
                    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'})
page_soup = BeautifulSoup(page.content, 'html.parser')
charts_by_genre = page_soup.find_all('div', class_='podcast mb1')
chart_urls = [chart.find('a')['href'] for chart in charts_by_genre]
# remove "top podcasts" and "trending podcasts"
chart_urls = chart_urls[:-3] + [chart_urls[-1]]
num_urls = len(chart_urls)


# For each genre, append all of its page urls
def add_next_pages(chart_indices):
    for i in chart_indices:
        temp_chart_url = chart_urls[i]
        while temp_chart_url:
            chart_page = requests.get(temp_chart_url, headers={
                                      'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'})
            if (chart_page.status_code != 200):
                return i
            next_page = BeautifulSoup(
                chart_page.content, 'html.parser').find('span', class_='next')
            if next_page:
                temp_chart_url = 'http://chartable.com' + \
                    next_page.find('a')['href']
                next_page_urls.append(temp_chart_url)
            else:
                temp_chart_url = None
    return -1


# Need to load data incrementally due to request limit
next_page_urls = []

def load_next_pages():
    i = 0
    while i != -1:
        i = add_next_pages(range(i, num_urls))
    chart_urls += next_page_urls


# Get show titles using chart urls from Chartable
def collect_shows(chart_indices):
    for i in chart_indices:
        chart_url = chart_urls[i]
        chart_page = requests.get(chart_url, headers={
                                  'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'})
        if (chart_page.status_code != 200):
            return i

        show_soup = BeautifulSoup(chart_page.content, 'html.parser')
        all_shows = show_soup.find_all('tr', class_='striped--near-white')[:7]

        key = ' '.join(((chart_url.split('/')[-1]).split('-'))[4:])

        for show in all_shows:
            show_name = show.find('a', class_='link blue')
            show_rank = show.find('div', class_='b header-font f2 tc')
            if not show_name:
                show_name = show.find('div', class_='title f4')
            genre = ' & '.join(key.split('?')[0].split()).title()
            if genre == "True & Crime":
                genre = "True Crime"
            
            genres_to_shows[genre].append(
                {"show_name": show_name.text, "rank": show_rank.text})
    return -1


# Need to load data incrementally due to request limit
genres_to_shows = collections.defaultdict(list)
def load_shows_from_chartable(chart_urls):
    i = 0
    while i != -1:
        i = collect_shows(range(i, num_urls))
    return genres_to_shows


# Get all shows
def get_all_shows(genres_to_shows):
    shows = dict()
    for genre, show_data in genres_to_shows.items():
        for show in show_data:
            try:
                show_name, rank = show['show_name'], show['rank']
                results = sp.search(q=show_name, type='show', market='US')
                show = results['shows']['items'][0]
                if (show['languages'] == ['en'] or show['languages'] == ['en-US']):
                    if show['id'] in shows:
                        shows[show['id']]['genres'].append(genre)
                    else:
                        new_show = {
                            "id": show['id'],
                            "name": show['name'],
                            "description": show['description'],
                            "genres": [genre],
                            "languages": show['languages'],
                            "publisher": show['publisher'],
                            "show_rank": rank
                        }
                        shows[show['id']] = new_show
            except:
                continue
    return shows


# GET ALL EPISODES
def get_all_episodes(shows):
    episodes = dict()
    episode_id_to_idx = dict()
    idx = 0
    for show_id in shows.keys():
        try:
            results = sp.show_episodes(
                show_id, limit=10, offset=0, market='US')
            episode_items = results['items']
            for episode in episode_items:
                if len(episode['description']) > 0:
                    new_episode = {
                        "id": episode['id'],
                        "show_id": show_id,
                        "name": episode['name'],
                        "description": episode['description'],
                        "duration_ms": episode['duration_ms'],
                        "genres": shows[show_id]['genres'],
                        "publisher": shows[show_id]['publisher'],
                        "release_date": episode['release_date'],
                        "show_rank": shows[show_id]['show_rank']
                    }
                    episodes[episode['id']] = new_episode
                    episode_id_to_idx[episode['id']] = idx
                    idx += 1
        except:
            continue
    with open('episode_id_to_idx.json', 'w') as json_file:
        json.dump(episode_id_to_idx, json_file)
    return episodes


def get_tf_idf_vectors(episodes, category, max_df):
    episodes_desc = [episodes[episode_id][category]
                     for episode_id in episodes]
    vectorizer = TfidfVectorizer(
        stop_words='english', max_df=max_df, dtype=np.float32)
    mat = np.array(vectorizer.fit_transform(episodes_desc).toarray())
    idf = vectorizer.idf_
    terms = vectorizer.get_feature_names()

    #cooccurrence matrix for thesaurus  
    # if category == 'description':
    #     cooccurence = np.dot(mat.T, mat)
    #     json.dump(cooccurence, open('cooccurrence.json', 'w'), cls=NumpyEncoder)

    file_name_tf_idf_vectors = 'tf_idf_{}.json'.format(category)
    file_name_idf = 'idf_{}.json'.format(category)
    file_name_terms = 'terms_{}.json'.format(category)

    json.dump(mat, open(file_name_tf_idf_vectors, 'w'), cls=NumpyEncoder)
    json.dump(idf, open(file_name_idf, 'w'), cls=NumpyEncoder)
    with open(file_name_terms, 'w') as json_file:
        json.dump(terms, json_file)
    


def group_by_genre(episodes):
    genre_to_episodes = collections.defaultdict(list)
    for episode in episodes:
        genres = episodes[episode]['genres']
        for genre in genres:
            genre_to_episodes[genre].append(episodes[episode])
    
    with open('genre_to_episodes.json', 'w') as json_file:
        json.dump(genre_to_episodes, json_file)
    return genre_to_episodes


if __name__ == "__main__":
    genres_to_shows = load_shows_from_chartable(chart_urls)
    shows = get_all_shows(genres_to_shows)
    episodes = get_all_episodes(shows)
    with open("episodes.json", 'w') as json_file:
        json.dump(episodes, json_file)
    get_tf_idf_vectors(episodes, 'description', 0.8)
    get_tf_idf_vectors(episodes, 'name', 0.8)
    genre_to_episodes = group_by_genre(episodes)
    print(f"There are {len(shows)} shows and {len(episodes)} episodes.")
    print(f"There are {len(genre_to_episodes)} genres: {genre_to_episodes.keys()}")
