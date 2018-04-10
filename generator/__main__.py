from generator.business import rating_generator
from generator.ui import cli


def wire():
    registry = dict()
    registry["ui"] = cli
    return registry


def main():
    input_params = ['some', 'params']
    registry = wire()
    rating_generator.start(registry, input_params)


if __name__ == "__main__":
    main()