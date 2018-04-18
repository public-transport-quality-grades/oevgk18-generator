
def isochrone(registry):
    routing_engine_service = registry['routing_engine_service']
    with routing_engine_service.db_connection() as db:
        routing_engine_service.calc_effective_kilometres(db)