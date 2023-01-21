import os
from ara_flask.ara import Ara

from flask import Flask, abort, jsonify, request
from dotenv import load_dotenv

# from ara_flask.models import db_session

load_dotenv()

app = Flask(__name__)

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


@app.route("/anime", methods=["POST"])
def add_anime():
    body = request.json

    ara.add_anime(
        body["id"],
        body["title"],
        body["synopsis"],
        body["genre"],
        body["aired"],
        int(body["episodes"]),
        int(body["members"]),
        body["popularity"],
        int(body["ranked"]),
        body["score"],
        body["img_url"],
        body["link"],
    )
    return ("", 204)


if __name__ == "__main__":
    app.run()
