from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Listen & Learn - Podcast Recommendation Engine"
names = ["Kevin Cook: kjc244", "Test: test"]


@irsystem.route("/", methods=["GET"])
def search():
    query = request.args.get("search")
    if not query:
        data = []
        output_message = ""
    else:
        output_message = "Your search: " + query
        data = range(5)
    return render_template(
        "search.html",
        project=project_name,
        names=names,
        output_message=output_message,
        data=data,
    )
