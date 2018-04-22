from typing import List
from .model.transport_stop import TransportStop


def transport_stops(registry) -> List[str]:
    ptstop_service = registry['ptstop_service']
    db_config = registry['config']['database-connections']
    with ptstop_service.db_connection(db_config) as db:
        return list(ptstop_service.get_transport_stops(db))


def transport_stops_from_uic_refs(registry, uic_refs: List[str]) -> List[TransportStop]:
    ptstop_service = registry['ptstop_service']
    db_config = registry['config']['database-connections']
    with ptstop_service.db_connection(db_config) as db:
        return list(
            [ptstop_service.get_transport_stop_from_uic_ref(db, uic_ref) for uic_ref in uic_refs])
