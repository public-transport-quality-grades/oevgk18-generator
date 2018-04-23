from contextlib import contextmanager
from records import Database


@contextmanager
def db_connection(db_config: dict):
    connection = Database(db_config['public-transport-stops'])
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
