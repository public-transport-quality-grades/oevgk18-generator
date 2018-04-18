from . import transport_stop_resolver, isochrone_handler


def start(registry: dict, params):
    cli = registry['ui']
    cli.parse_params(params)
    transport_stops = transport_stop_resolver.transport_stops(registry)
    isochrone_handler.isochrone(registry)
