import sys
import time
import logging

from generator.business import core
from generator.ui import cli
from generator.integration import routing_engine_service, timetable_service, transport_stop_service
from generator.output import geojson_writer, metadata_writer
from generator import config

CONFIGURATION_PATH = "generator_config.yml"

logger = logging.getLogger('generator')


def wire() -> dict:
    registry = dict()
    registry['ui'] = cli
    registry['routing_engine_service'] = routing_engine_service
    registry['timetable_service'] = timetable_service
    registry['output_writer'] = geojson_writer
    registry['metadata_writer'] = metadata_writer
    registry['transport_stop_service'] = transport_stop_service
    registry['config'] = config.load_config(CONFIGURATION_PATH)
    return registry


def setup_logging(verbose=False, quiet=False):
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
            '[%(levelname)-7s] - %(message)s')
    if verbose and not quiet:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)-7s] - %(message)s')
    if quiet:
        logger.setLevel(logging.WARNING)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.debug("Setting up logging complete")


def main():
    input_params = ['some', 'params']
    registry = wire()
    setup_logging(verbose=True)
    core.calculate_quality_grades(registry, input_params)


if __name__ == "__main__":
    start = time.time()
    main()
    logger.info(f"Completed in {time.time() - start} seconds")
