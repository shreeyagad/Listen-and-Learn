from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Listen & Learn - Podcast Recommendation Engine"
names = ["Kevin Cook: kjc244", "Nicholas Rahardja: nmr73", "Justin Li: jl2588", "Shreeya Gad: sg988", "Mohammed Ullah: mu83"]


@irsystem.route("/", methods=["GET"])
def search():
    search_object = {
        "query": request.args.get("query"),
        "language": request.args.get("language"),
        "duration": request.args.get("duration"),
        "genre": request.args.get("genre"),
        "publisher": request.args.get("publisher"),
        "year_published": request.args.get("year_published")
    }

    if not request.args.get("query"):
        data = []
        output_message = ""
    else:
        data = get_ranked_episodes(search_object)
        output_message = "Your recommended podcasts: "
    return render_template(
        "search.html",
        project=project_name,
        names=names,
        output_message=output_message,
        data=data,
    )

def get_ranked_episodes(query):
    episodes = np.load('episodes.npy', allow_pickle='TRUE').item()

    # Each episode has the following structure: {
    #   "id": str,
    #   "show_id": str,
    #   "name": str,
    #   "description": str,
    #   "duration_ms": int,
    #   "genre": str,
    #   "languages": list[str],
    #   "publisher": str,
    #   "release_date: str,
    #   "release_date_precision": str,
    #   "show_rank": int
    # }

    # The keys are the same as the attributes of the SimplifiedEpisodeObject in the Spotify API.
    # See link for details: https://developer.spotify.com/documentation/web-api/reference/#object-simplifiedepisodeobject

    # The search_object has the following structure: {
    #     "query": str (required),
    #     "language": str (required),
    #     "duration": int (optional),
    #     "genre": str (optional),
    #     "publisher": str (optional),
    #     "year_published": int (optional)
    # }

    # Filter out episodes that do not match the parameters (except for "query")

    # Conduct cosine similarity between episode description and "query", for each episode

    # Return list of ranked results

    return ["NOT_IMPLEMENTED"]

