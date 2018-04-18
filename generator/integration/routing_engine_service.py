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
    transaction = db.transaction()
    db.query("SELECT calc_effective_kilometres();")
    transaction.commit()


def _mark_relevant_roads(db: Database):
    transaction = db.transaction()
    db.query("SELECT mark_relevant_ways();")
    transaction.commit()
