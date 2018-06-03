from generator.business.model.public_transport_group import PublicTransportGroup
from . import mock_transport_stops


def get_transport_groups(registry):
    return {
        mock_transport_stops.stop_8503400: PublicTransportGroup.A,
        mock_transport_stops.stop_8503125: PublicTransportGroup.B,
        mock_transport_stops.stop_8591382: PublicTransportGroup.C,
        mock_transport_stops.stop_8593245: PublicTransportGroup.A
    }
