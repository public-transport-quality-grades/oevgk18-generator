from generator.business import rating_generator
from generator.ui import cli
from generator.integration import ptstop_service, routing_engine_service


def wire() -> dict:
    registry = dict()
    registry['ui'] = cli
    registry['ptstop_service'] = ptstop_service
    registry['routing_engine_service'] = routing_engine_service
    return registry


def main():
    input_params = ['some', 'params']
    registry = wire()
    rating_generator.start(registry, input_params)


if __name__ == "__main__":
    main()
