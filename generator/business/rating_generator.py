from . import transport_stop_resolver


def start(registry: dict, params):
    cli = registry['ui']
    cli.parse_params(params)
    transport_stops = transport_stop_resolver.transport_stops_from_uic_refs(registry, ['8595591', '8574493'])
    print(transport_stops)
