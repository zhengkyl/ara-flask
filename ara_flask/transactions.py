import random
from ara_flask.models import Anime
from sqlalchemy import and_, func, or_
from random import randrange


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
    a = session.query(Anime).filter(Anime.id == id)

    bounded_score = min(max(score, 0), 10)

    if a.members == 0:
        a.members = 1

    new_score = min(
        max(RATING_MULTIPLIER * (bounded_score - a.score) / a.members, 0), 10
    )

    a.score = new_score


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
