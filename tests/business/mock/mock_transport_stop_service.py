from typing import List

from generator.business.model.transport_stop import TransportStop
from . import mock_transport_stops


def get_transport_stops(db) -> List[TransportStop]:
    return [
        mock_transport_stops.stop_8503400,
        mock_transport_stops.stop_8503125,
        mock_transport_stops.stop_8591382,
        mock_transport_stops.stop_8593245,
        mock_transport_stops.stop_8504532
    ]
