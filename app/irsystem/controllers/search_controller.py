from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import numpy as np
import json
import boto3
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

project_name = "Listen & Learn - Podcast Recommendation Engine"
names = ["Kevin Cook: kjc244", "Nicholas Rahardja: nmr73",
         "Justin Li: jl2588", "Shreeya Gad: sg988", "Mohammed Ullah: mu83"]

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
    idf_description = json.load(f, object_hook=json_numpy_obj_hook, encoding='utf8')
with open("tf_idf_description.json") as f:
    tf_idf_description = json.load(f, object_hook=json_numpy_obj_hook, encoding='utf8')
with open("terms_name.json") as f:
    terms_name = json.load(f)
with open("idf_name.json") as f:
    idf_name = json.load(f, object_hook=json_numpy_obj_hook, encoding='utf8')
with open("tf_idf_name.json") as f:
    tf_idf_name = json.load(f, object_hook=json_numpy_obj_hook, encoding='utf8')


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
        "year_published": request.json.get("year")
    }

    return jsonify(get_ranked_episodes(search_object))
    

def filter_helper(genre, duration, year, publisher):
    filtered_episodes = []
    episodes_by_genre = genre_to_episodes[genre]
    for episode in episodes_by_genre:
        if ((duration == None or (abs(duration - episode['duration_ms']) < 0.1 * duration))
            and
            (year == None or (
                abs(year - int(episode['release_date'][:4]))) < 2)
            and
                (publisher == None or publisher == episode['publisher'])):
            filtered_episodes.append(episode)
    return filtered_episodes


def get_ranked_episodes(query):
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

    ranked_episodes = []

    genres = query['genres']
    publisher = query['publisher']
    year = query['year_published']
    duration = query['duration']
    query = query['query']

    filtered_episodes = []
    if len(genres) >= 1:
        for g in genres:
            filtered_episodes += filter_helper(g, duration, year, publisher)
    else:
        for g in genre_to_episodes.keys():
            filtered_episodes += filter_helper(g, duration, year, publisher)
                    
    # List of tuples, each tuple contains the index of episode in episodes data set.
    # Used when calculating cosine similarity with the pre-computed tf-idf scores. 
    filtered_episodes = [(episode_id_to_idx[episode['id']], episode)
                         for episode in filtered_episodes]
    filtered_episode_indices = [episode[0] for episode in filtered_episodes]

    episode_desc_vectorizer = CountVectorizer(vocabulary=terms_description)
    query_vec_desc = episode_desc_vectorizer.fit_transform([query]).toarray().flatten()
    query_desc_tf_idf = query_vec_desc*idf_description[np.newaxis,:]

    # episode_name_vectorizer = CountVectorizer(vocabulary=terms_name)
    # query_vec_name = episode_name_vectorizer.fit_transform([query]).toarray().flatten()
    # query_name_tf_idf = query_vec_name*idf_name[np.newaxis,:]

    filtered_episodes_desc_tf_idf = tf_idf_description[filtered_episode_indices]
    episodes_desc_cos_sim = cosine_similarity(
        query_desc_tf_idf, filtered_episodes_desc_tf_idf)[0]
    top_rank_indices = list(np.argsort(episodes_desc_cos_sim)[::-1][:5])
    for i in top_rank_indices:
        ranked_episodes.append(filtered_episodes[i][1])

    return ranked_episodes