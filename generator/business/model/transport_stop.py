from typing import List
from .transport_platform import TransportPlatform


class TransportStop:

    def __init__(self, uic_name: str, uic_ref: str, platforms: List[TransportPlatform]):
        self.uic_name = uic_name
        self.uic_ref = uic_ref
        self.platforms = platforms

    def __repr__(self):
        return f"{{uic_name: {self.uic_name}, uic_ref: {self.uic_ref}, platforms: {self.platforms}}}"
