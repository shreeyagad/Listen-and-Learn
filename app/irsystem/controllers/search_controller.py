from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

project_name = "Listen & Learn - Podcast Recommendation Engine"
names = ["Kevin Cook: kjc244", "Nicholas Rahardja: nmr73",
         "Justin Li: jl2588", "Shreeya Gad: sg988", "Mohammed Ullah: mu83"]
# episodes_desc_tf_idf = np.load('../../../data/tf_idf_description.npy',
#                                allow_pickle='TRUE')
# episodes_desc_idf = np.load('../../../data/idf_description.npy',
#                             allow_pickle='TRUE')
# episodes_desc_terms = np.load('../../../data/terms_description.npy',
#                               allow_pickle='TRUE')
# episode_title_tf_idf = np.load('../../../data/tf_idf_name.npy',
#                                allow_pickle='TRUE')
# episodes_title_idf = np.load('../../../data/idf_name.npy',
#                              allow_pickle='TRUE')
# episodes_title_terms = np.load('../../../data/terms_name.npy',
#                                allow_pickle='TRUE')

@irsystem.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@irsystem.route("/search", methods=["POST"])
def search():
    search_object = {
        "query": request.json.get("query"),
        "duration": request.json.get("duration"),
        "genre": request.json.get("genres"),
        "publisher": request.json.get("publisher"),
        "year_published": request.json.get("year")
    }

    return jsonify(get_first_5_episodes())
    

def get_first_5_episodes():
    episodes = np.load('data/episodes.npy',
                       allow_pickle='TRUE').item()
    ranked_episodes = []
    episode_values = episodes.values()
    ep_iterator = iter(episode_values)
    for i in range(5):
        ranked_episodes.append(next(ep_iterator))
    return ranked_episodes

def filter_helper(genre, duration, year, publisher):
    filtered_episodes = []
    for episode in genre:
        if ((duration == None or (abs(duration - episode['duration_ms']) < 0.1 * duration))
            and
            (year == None or (
                abs(year - int(episode['release_date'][:4]))) < 2)
            and
                (publisher == None or publisher == episode['publisher'])):
            filtered_episodes.append(episode)
    return filtered_episodes


def get_ranked_episodes(query):
    # we don't actually need this episode data anymore.
    episodes = np.load('../../../data/episodes.npy',
                       allow_pickle='TRUE').item()
    ranked_episodes = []

    # DUMMY CODE that returns first 5 episodes
    # episode_values = episodes.values()
    # ep_iterator = iter(episode_values)
    # for i in range(5):
    #     ranked_episodes.append(next(ep_iterator)['name'])

    # Each episode has the following structure: {
    #   "id": str,
    #   "show_id": str,
    #   "name": str,
    #   "description": str,
    #   "duration_ms": int,
    #   "genre": str,
    #   "publisher": str,
    #   "release_date: str,
    #   "show_rank": int
    # }y

    # The keys are the same as the attributes of the SimplifiedEpisodeObject in the Spotify API.
    # See link for details: https://developer.spotify.com/documentation/web-api/reference/#object-simplifiedepisodeobject

    # The search_object has the following structure: {
    #     "query": str (required),
    #     "duration": int (optional),
    #     "genre": list[str] (optional),
    #     "publisher": str (optional),
    #     "year_published": int (optional)
    # }

    # TODO: Filter out episodes that do not match the parameters (except for "query")

    episode_ids = list(episodes.keys())
    genre_episodes = np.load('../../../data/genre_episodes.npy',
                             allow_pickle='TRUE').item()
    genre = query['genre']
    publisher = query['publisher']
    year = query['year_published']
    duration = query['duration']
    query = query['query']

    filtered_episodes = []
    if len(genre) >= 1:
        for g in genre:
            for episode in genre_episodes[g]:
                if ((duration == None or (abs(duration - episode['duration_ms']) < 0.1 * duration))
                    and
                    (year == None or (
                        abs(year - int(episode['release_date'][:4]))) < 2)
                    and
                        (publisher == None or publisher == episode['publisher'])):
                    filtered_episodes.append(episode)
    else:
        for g in genre_episodes.keys():
            for episode in genre_episodes[g]:
                if ((duration == None or (abs(duration - episode['duration_ms']) < 0.1 * duration))
                    and
                    (year == None or (
                        abs(year - int(episode['release_date'][:4]))) < 2)
                    and
                        (publisher == None or publisher == episode['publisher'])):
                    filtered_episodes.append(episode)

    # index of episode in episodes list and the dictionary for the episode
    # list of tuples, each tuple contains the index of episode in episodes data set,
    # which should be used when calculating cosine similarity with the pre-computed
    # tf-idf scores. The second element in the tuple corresponds to the dictionary
    # for the episode itself
    filtered_episodes = [(episode_ids.index(episode['id']), episode)
                         for episode in filtered_episodes]

    # print here to check if returns desired output.
    # print(filtered_episodes_idx)

    # TODO: Conduct cosine similarity between episode description and "query", for each episode

    episode_desc_vectorizer = CountVectorizer(vocabulary=episodes_desc_terms)
    episode_title_vectorizer = CountVectorizer(vocabulary=episodes_title_terms)
    query_vec_desc = episode_desc_vectorizer.fit_transform([query]).toarray()
    query_vec_title = episode_title_vectorizer.fit_transform([query]).toarray()
    query_desc_tf_idf = np.array(query_vec_desc[0])*episodes_desc_idf
    query_title_tf_idf = np.array(query_vec_title[0])*episodes_title_idf

    filtered_episodes_idx = [idx for idx, _ in filtered_episodes]

    filtered_episodes_tf_idf = []
    for idx in filtered_episodes_idx:
        filtered_episodes_tf_idf.append(episodes_desc_tf_idf[idx])

    filtered_episodes_desc_tf_idf = np.array(filtered_episodes_tf_idf)
    episodes_desc_cos_sim = cosine_similarity(
        query_desc_tf_idf.reshape(1, -1), filtered_episodes_desc_tf_idf)[0]
    top_rank_indices = list(np.argsort(episodes_desc_cos_sim)[::-1][:5])
    for i in top_rank_indices:
        ranked_episodes.append(filtered_episodes[i][1])
    # Return list of ranked results
    return ranked_episodes


# Testing out the function above
# query1 = {
#     "query": "crime detective murder mystery",
#     "duration": None,
#     "genre": [],
#     "publisher": None,
#     "year_published": None
# }
# print(get_ranked_episodes(query1))
# genre_episodes = np.load('../../../data/genre_episodes.npy',
#                         allow_pickle = 'TRUE').item()
# print(genre_episodes.keys())
