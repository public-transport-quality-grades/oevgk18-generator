from contextlib import contextmanager
from records import Database
from .. import config


@contextmanager
def db_connection():
    connection = Database(config.PTSTOP_DB_CONNECTION)
    yield connection
    connection.close()


def calc_effective_kilometres(db: Database):
    _mark_relevant_roads(db)
    db.query("SELECT calc_effective_kilometres();")


def _mark_relevant_roads(db: Database):
    db.query("SELECT mark_relevant_ways();")
