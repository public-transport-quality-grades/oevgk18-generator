from contextlib import contextmanager
from typing import List
from .mock_isochrone import fake_isochrone


@contextmanager
def db_connection(db_config: dict):
    yield None


def calc_isochrones(db, uic_ref: int, boundaries: List[int]):
    mocked_isochrones = {
        8503400: [fake_isochrone(450.0), fake_isochrone(1350.0)],  # no isochrone found for 300s
        8503125: [fake_isochrone(450.0), fake_isochrone(900.0)],
        8591382: [fake_isochrone(450.0)],
    }

    return mocked_isochrones[uic_ref]
