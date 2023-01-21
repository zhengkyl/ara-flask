from ara_flask.models import Anime


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
