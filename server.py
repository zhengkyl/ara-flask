import os
from ara_flask.ara import Ara

from flask import Flask, abort, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS
import requests

load_dotenv()

app = Flask(__name__)

CORS(app)

app.config.from_mapping(SECRET_KEY="dev", DB_URI=os.environ["DB_URI"])

conn_string = app.config.get("DB_URI")

ara = Ara(conn_string)


@app.route("/anime", methods=["GET"])
def get_anime():
    args = request.args
    id = args.get("id")
    title = args.get("title")

    a = ara.get_anime(id, title)
    if not a:
        abort(404)

    return jsonify(a.as_dict())


@app.route("/import", methods=["POST"])
def import_anime():
    args = request.args
    id = args.get("id")
    r = requests.get(
        "https://api.myanimelist.net/v2/anime/"
        + id
        + "?fields=synopsis,rank,popularity,num_list_users,mean,genres,num_episodes",
        headers={"X-MAL-CLIENT-ID": os.environ["MAL_CLIENT_ID"]},
    )

    data = r.json()

    ara.add_anime(
        data["id"],
        data["title"],
        data["synopsis"],
        list(map(lambda obj: obj["name"], data["genres"])),
        "",
        int(data.get("num_episodes", 0)),
        int(data.get("num_list_users", 1)),
        int(data.get("popularity", 10000)),
        int(data.get("ranked", 10000)),
        float(data.get("mean", 0)),
        data["main_picture"].get("medium", ""),
        "https://myanimelist.net/anime/" + str(data["id"]),
    )

    return ("", 204)


@app.route("/anime", methods=["POST"])
def add_anime():
    body = request.json

    ara.add_anime(
        int(body["id"]),
        body["title"],
        body.get("synopsis", ""),
        body.get("genre", []),
        body.get("aired", ""),
        int(body.get("episodes", 0)),
        int(body.get("members", 1)),
        int(body.get("popularity", 10000)),
        int(body.get("ranked", 10000)),
        float(body.get("score", 0)),
        body.get("img_url", ""),
        body.get("link", ""),
    )
    return ("", 204)


@app.route("/rate", methods=["POST"])
def rate_anime():
    body = request.json
    ara.rate_anime(body["id"], body["score"])
    return ("", 204)


@app.route("/rate", methods=["GET"])
def get_animes_to_rate():
    return ara.get_animes_to_rate()


@app.route("/top", methods=["GET"])
def get_top_animes():
    args = request.args
    query = args.get("genre")
    return ara.get_top_animes(query)


@app.route("/bot", methods=["GET"])
def get_bot_animes():
    args = request.args
    query = args.get("genre")
    return ara.get_bot_animes(query)


@app.route("/pick", methods=["GET"])
def get_pick_animes():
    return ara.get_fixed_animes()


@app.route("/search", methods=["GET"])
def fuzzy_search():
    args = request.args
    query = args.get("query")
    return ara.fuzzy_search(query)


@app.route("/recs", methods=["GET"])
def get_rec_for_genre():
    args = request.args
    query = args.get("genre")
    return ara.get_rec_for_genre(query)


@app.route("/recent", methods=["GET"])
def get_recently_rated():
    return ara.get_recently_rated()


@app.errorhandler(404)
def not_found(e):
    return ("L + Ratio", 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ["PORT"])
