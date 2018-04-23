
def isochrone(registry):
    routing_engine_service = registry['routing_engine_service']
    db_config = registry['config']['database-connections']
    with routing_engine_service.db_connection(db_config) as db:
        routing_engine_service.calc_effective_kilometres(db)
