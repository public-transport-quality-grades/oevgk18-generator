from generator.business import rating_generator
from generator.ui import cli
from generator.integration import osm_service


def wire():
    registry = dict()
    registry['ui'] = cli
    registry['osm_service'] = osm_service
    return registry


def main():
    input_params = ['some', 'params']
    registry = wire()
    rating_generator.start(registry, input_params)


if __name__ == "__main__":
    main()