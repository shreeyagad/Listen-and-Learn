from nltk.corpus import wordnet
from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import numpy as np
import json
import time
import pickle
from numpy.__config__ import show
# import boto3
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import base64
import nltk
nltk.download('wordnet')


project_name = "Listen & Learn - Podcast Recommendation Engine"
names = [
    "Kevin Cook: kjc244",
    "Nicholas Rahardja: nmr73",
    "Justin Li: jl2588",
    "Shreeya Gad: sg988",
    "Mohammed Ullah: mu83",
]

# Download files from S3
# s3 = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
#                         aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
#                         region_name=os.environ.get('AWS_DEFAULT_REGION'))
# s3.download_file('cs4300-listen-and-learn-tf-idf-data', 'tf_idf_description.json', 'tf_idf_description.json')
with open("episode_id_to_idx.json") as f:
    episode_id_to_idx = json.load(f)
with open("genre_to_episodes.json") as f:
    genre_to_episodes = json.load(f)
with open("terms_description.json") as f:
    terms_description = json.load(f)
with open("idf_description.json") as f:
    idf_description = json.load(
        f, object_hook=json_numpy_obj_hook, encoding="utf8")
with open("tf_idf_description.json") as f:
    tf_idf_description = json.load(
        f, object_hook=json_numpy_obj_hook, encoding="utf8")
with open("terms_name.json") as f:
    terms_name = json.load(f)
with open("idf_name.json") as f:
    idf_name = json.load(f, object_hook=json_numpy_obj_hook, encoding="utf8")
with open("tf_idf_name.json") as f:
    tf_idf_name = json.load(
        f, object_hook=json_numpy_obj_hook, encoding="utf8")
with open("thesaurus.json") as f:
    thesaurus = json.load(f, object_hook=json_numpy_obj_hook, encoding="utf8")


@irsystem.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@irsystem.route("/search", methods=["POST"])
def search():
    search_object = {
        "query": request.json.get("query"),
        "duration": request.json.get("duration"),
        "genres": request.json.get("genres"),
        "publisher": request.json.get("publisher"),
        "year_published": request.json.get("year"),
    }

    return jsonify(get_ranked_episodes(search_object))


def filter_helper(genre, duration, year, publisher):
    filtered_episodes = []
    episodes_by_genre = genre_to_episodes[genre]
    for episode in episodes_by_genre:
        if ((duration == None or (abs(duration - episode["duration_ms"]) < 0.1 * duration)
             )
            and (year == None or (abs(year - int(episode["release_date"][:4]))) < 2)
            and (publisher == None or publisher == episode["publisher"])
            ):
            filtered_episodes.append(episode)
    return filtered_episodes


def synonym_fn(term):
    synonyms = []
    for syn in wordnet.synsets(term):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return " ".join(list(set(synonyms))[1:3])  # only 2 synonyms per term


def thesaurus_fn(query_tokens):
    new_query = ""
    for token in query_tokens:
        new_query = new_query + " " + token
        if token in thesaurus.keys():
            synonyms = thesaurus[token][0]
            new_query = new_query + " " + synonyms
        new_query = new_query + " " + synonym_fn(token)
    new_query = new_query.strip()
    return new_query


def get_cos_sim(query):
    """
    returns a tuple of 3 elements: cos_sim with desc, cos_sim with title, episode dictionary.
    """

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
    # }

    # The search_object has the following structure: {
    #     "query": str (required),
    #     "duration": int (optional),
    #     "genre": list[str] (optional),
    #     "publisher": str (optional),
    #     "year_published": int (optional)
    # }

    genres = query["genres"]
    publisher = query["publisher"]
    year = query["year_published"]
    duration = query["duration"]
    query = query["query"]

    if year:
        year = int(year)
    if duration:
        duration = duration.split(":")
        duration = 60000*(int(duration[0])*60 + int(duration[1]))
    if query:
        query = query.lower()

    filtered_episodes = []

    if len(genres) >= 1:
        for g in genres:
            filtered_episodes += filter_helper(g, duration, year, publisher)
    else:
        for g in genre_to_episodes.keys():
            filtered_episodes += filter_helper(g, duration, year, publisher)
    # if there are no filter episodes
    if filtered_episodes == [] or (query.strip() == ""):
        return None
    filtered_episodes = {
        episode_id_to_idx[episode["id"]]: episode for episode in filtered_episodes}
    filtered_episodes = [(k, v) for (k, v) in filtered_episodes.items()]

    # List of tuples, each tuple contains the index of episode in episodes data set.
    # Used when calculating cosine similarity with the pre-computed tf-idf scores.
    # filtered_episodes = [
    #     (episode_id_to_idx[episode["id"]], episode) for episode in filtered_episodes
    # ]
    filtered_episode_indices = [episode[0] for episode in filtered_episodes]
    episode_desc_vectorizer = CountVectorizer(vocabulary=terms_description)

    # Incorporating similar words into query
    tokenizer = episode_desc_vectorizer.build_tokenizer()
    query_tokens = tokenizer(query)

    if len(query_tokens) == 1:
        query = thesaurus_fn(query_tokens)

    query_vec_desc = episode_desc_vectorizer.fit_transform(
        [query]).toarray().flatten()

    query_desc_tf_idf = query_vec_desc * idf_description[np.newaxis, :]

    episode_name_vectorizer = CountVectorizer(vocabulary=terms_name)
    query_vec_name = episode_name_vectorizer.fit_transform(
        [query]).toarray().flatten()
    query_name_tf_idf = query_vec_name * idf_name[np.newaxis, :]
    filtered_episodes_desc_tf_idf = tf_idf_description[filtered_episode_indices]
    filtered_episodes_name_tf_idf = tf_idf_name[filtered_episode_indices]

    episodes_desc_cos_sim = cosine_similarity(
        query_desc_tf_idf, filtered_episodes_desc_tf_idf
    )[0]

    episodes_name_cos_sim = cosine_similarity(
        query_name_tf_idf, filtered_episodes_name_tf_idf
    )[0]

    return (episodes_desc_cos_sim, episodes_name_cos_sim, filtered_episodes, query_desc_tf_idf)


def get_ranked_episodes(query, name_wt=40, desc_wt=60, name_thr=0.8, num_ep=5):
    """
    Inputs:
    - Query
    The query object has the following structure: {
         "query": str (required),
         "duration": int (optional),
         "genres": list[str] (optional),
         "publisher": str (optional),
         "year_published": int (optional)
     }
    - name_wt (int) - multiplier for name cos sim
    - desc_wt (int) - multiplier for description cos sim
    - name_thr (float) - if name cos_sim exceeds this immdetialy return that episode
    - num_ep (int) - number of episodes to return as results

    Output: a list of tuples of the form [(ep object 1, cos sim score 1), (ep object 2, cos sim score 2)...]
    --> has type list (dict, float)
    Each episode dictionary returned has the added filed sim_score which is out of 100.
    """
    ranked_episodes = []
    if get_cos_sim(query) == None:
        return ranked_episodes

    desc_cs, name_cs, filtered_episodes, query_desc_tf_idf = get_cos_sim(query)

    for idx in np.argwhere(name_cs > name_thr):
        idx = idx[0]
        filtered_episodes[idx][1]["sim_score"] = 100 * name_cs[idx]
        ranked_episodes.append(filtered_episodes[idx][1])
        desc_cs = np.delete(desc_cs, idx)
        name_cs = np.delete(name_cs, idx)
        del filtered_episodes[idx]

    loaded_model = pickle.load(open("genre_classification_model.sav", 'rb'))
    prediction = loaded_model.predict(query_desc_tf_idf)

    genre_to_idx = {genre: g for g,
                    genre in enumerate(genre_to_episodes.keys())}
    predicted_genre = list(genre_to_idx)[prediction[0]]
    genre_scores = np.zeros((len(filtered_episodes),))

    for i in range(len(filtered_episodes)):
        if predicted_genre in filtered_episodes[i][1]["genres"]:
            genre_scores[i] = 1
        else:
            genre_scores[i] = 0.8

    show_ranks = np.array(
        [int(episode[1]["show_rank"]) for episode in filtered_episodes]
    )
    show_num_reviews = np.array([episode[1]["show_num_reviews"]
                                 for episode in filtered_episodes])
    show_num_reviews_log = np.log10(np.log10(show_num_reviews + 10) + 9)

    num = len(ranked_episodes)
    name_cs = name_cs * name_wt
    desc_cs = desc_cs * desc_wt
    total_cs = genre_scores * ((desc_cs + name_cs) / (np.log(show_ranks) + 1))
    total_cs = total_cs * show_num_reviews_log
    # make sure total sim score has a max value of 100
    total_cs[total_cs > 100] = 100

    if num < num_ep:
        top_rank_indices = list(np.argsort(total_cs)[::-1][: num_ep - num])
        for i in top_rank_indices:
            filtered_episodes[i][1]["sim_score"] = total_cs[i]
            ranked_episodes.append(filtered_episodes[i][1])
    return ranked_episodes


# test_query = {
#     "query": "   hi     ",
#     "duration": None,
#     "genres": [],
#     "publisher": None,
#     "year_published": None
# }

# print(get_ranked_episodes(test_query))
