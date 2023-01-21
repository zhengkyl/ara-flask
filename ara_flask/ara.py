from ara_flask.transactions import add_anime_txn, get_anime_txn, rate_anime_txn
from sqlalchemy_cockroachdb import run_transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import registry

registry.register("cockroachdb", "cockroachdb.sqlalchemy.dialect", "CockroachDBDialect")


class Ara:
    def __init__(self, conn_string) -> None:
        self.engine = create_engine(conn_string, convert_unicode=True)
        self.sessionmaker = sessionmaker(bind=self.engine)

    def get_anime(self, id, title):
        return run_transaction(
            self.sessionmaker, lambda session: get_anime_txn(session, id, title)
        )

    def add_anime(
        self,
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
        return run_transaction(
            self.sessionmaker,
            lambda session: add_anime_txn(
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
            ),
        )

    def rate_anime(self, id, score):
        return run_transaction(
            self.sessionmaker, lambda session: rate_anime_txn(session, id, score)
        )
