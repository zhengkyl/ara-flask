import random
from ara_flask.models import Anime
from sqlalchemy import func

recently_rated = []


def get_anime_txn(session, id=None, title=None):
    if id:
        a = session.query(Anime).filter(Anime.id == id).first()
    elif title:
        a = session.query(Anime).filter(Anime.title == title).first()

    if a:
        session.expunge(a)

    return a


def add_anime_txn(
    session,
    id,
    title,
    synopsis,
    genre,
    aired,
    episodes,
    members,
    popularity,
    ranked,
    score,
    img_url,
    link,
):
    a = Anime(
        id=id,
        title=title,
        synopsis=synopsis,
        genre=genre,
        aired=aired,
        episodes=episodes,
        members=members,
        popularity=popularity,
        ranked=ranked,
        score=score,
        img_url=img_url,
        link=link,
    )

    session.add(a)


RATING_MULTIPLIER = 50


def rate_anime_txn(session, id, score):
    a = session.query(Anime).filter(Anime.id == id).first()

    bounded_score = min(max(score, 0), 10)

    if a.members == 0:
        a.members = 1

    diff = RATING_MULTIPLIER * (bounded_score - a.score) / a.members

    a.members += 1

    a.score = min(max(a.score + diff, 0), 10)

    global recently_rated
    recently_rated.append({"id": a.id, "score": bounded_score})

    if len(recently_rated) > 10:
        recently_rated = recently_rated[1:]


def get_top_animes_txn(session):
    animes = session.query(Anime).order_by(Anime.score.desc()).limit(10)

    return list(map(lambda anime: anime.as_dict(), animes))


def get_bot_animes_txn(session):
    animes = session.query(Anime).order_by(Anime.score.asc()).limit(10)

    return list(map(lambda anime: anime.as_dict(), animes))


def fuzzy_search_txn(session, query):
    animes = (
        session.query(Anime)
        .filter(func.similarity(func.lower(Anime.title), func.lower(query)) > 0.3)
        .order_by(Anime.popularity.asc())
        .limit(10)
    )
    return list(map(lambda anime: anime.as_dict(), animes))


def get_animes_to_rate_txn(session):
    candidates = session.query(Anime).order_by(Anime.members.desc()).limit(200)
    candidates2 = session.query(Anime).order_by(func.random()).limit(50)

    candidates3 = candidates.union(candidates, candidates2)

    temp = list(map(lambda anime: anime.as_dict(), candidates3))
    chosen = random.choices(temp, k=1)

    return chosen[0]


def get_recently_rated_txn(session):
    return list(
        map(
            lambda id_score: {
                "anime": session.query(Anime)
                .filter(Anime.id == id_score["id"])
                .first()
                .as_dict(),
                "score": id_score["score"],
            },
            recently_rated,
        )
    )


def get_rec_for_genre_txn(session, genre):
    animes = (
        session.query(Anime)
        .filter(Anime.genre.contains([genre]))
        .order_by(Anime.members.desc())
        .limit(100)
    )
    temp = list(map(lambda anime: anime.as_dict(), animes))
    chosen = random.choices(temp, k=10)

    return chosen
