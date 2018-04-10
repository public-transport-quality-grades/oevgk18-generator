from generator.business import rating_generator
from generator.ui import cli
from generator.injector import registry


def wire():
    registry["ui"] = cli


def main():
    wire()
    rating_generator.start()


if __name__ == "__main__":
    main()