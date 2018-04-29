from typing import List
from .model.transport_stop import TransportStop


def transport_stops(registry) -> List[str]:
    ptstop_service = registry['ptstop_service']
    db_config = registry['config']['database-connections']
    return list(ptstop_service.get_transport_stops(db_config))
