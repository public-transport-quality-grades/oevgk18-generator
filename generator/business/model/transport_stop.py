from typing import List
from shapely.geometry import Point


class TransportStop:

    def __init__(self, uic_name: str, uic_ref: int, location: Point, platforms: List[str]):
        self.uic_name = uic_name
        self.uic_ref = uic_ref
        self.location = location
        self.platforms = platforms

    def __repr__(self):
        return f"{{uic_name: {self.uic_name}, uic_ref: {self.uic_ref}," \
               f" location: {self.location}, platforms: {self.platforms}}}"
