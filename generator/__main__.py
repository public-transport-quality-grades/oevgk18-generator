import time

from generator.business import rating_generator
from generator.ui import cli
from generator.integration import ptstop_service, routing_engine_service, timetable_service
from generator import config

CONFIGURATION_PATH = "generator_config.yaml"


def wire() -> dict:
    registry = dict()
    registry['ui'] = cli
    registry['ptstop_service'] = ptstop_service
    registry['routing_engine_service'] = routing_engine_service
    registry['timetable_service'] = timetable_service
    registry['config'] = config.load_config(CONFIGURATION_PATH)
    return registry


def main():
    input_params = ['some', 'params']
    registry = wire()
    rating_generator.start(registry, input_params)


if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time() - start)
