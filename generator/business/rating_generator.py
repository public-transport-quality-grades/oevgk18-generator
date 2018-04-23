from . import transport_stop_resolver, transport_stop_rating_calculator


def start(registry: dict, params):
    cli = registry['ui']
    cli.parse_params(params)
    for transport_stop_uic_ref in transport_stop_resolver.transport_stops(registry):
        transport_rating = transport_stop_rating_calculator.calculate_transport_stop_rating(registry,
                                                                                            transport_stop_uic_ref)
        # print(f"{transport_rating}: {transport_stop_uic_ref}")
