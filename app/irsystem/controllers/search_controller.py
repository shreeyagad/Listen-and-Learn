from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Listen & Learn - Podcast Recommendation Engine"
names = ["Kevin Cook: kjc244", "Nicholas Rahardja: nmr73", "Justin Li: jl2588", "Shreeya Gad: sg988", "Mohammed Ullah: mu83"]


@irsystem.route("/", methods=["GET"])
def search():
    search_object = {
        "query": request.args.get("query"),
        "release_date": request.args.get("release_date"),
        "duration": request.args.get("duration"),
        "genre": request.args.get("genre"),
        "language": request.args.get("language"),
        "publisher": request.args.get("publisher")
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

    # filter by user preferences

    # then conduct cosine similarity between episode descriptions and user query

    # return list of ranked results

    return ["Podcast 1", "Podcast 2"]

