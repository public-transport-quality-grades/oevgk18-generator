from typing import Tuple
import sys
import logging
import argparse
from .. import config

logger = logging.getLogger('generator')


def setup_cli(params: list, registry: dict) -> None:
    config_path, verbose = _parse_params(params)
    _setup_logging(verbose)
    logger.debug(f"Input parameters: config: {config_path}, verbose: {verbose}")
    registry['config'] = config.load_config(config_path)


def _parse_params(params: list) -> Tuple[str, bool]:

    parser = argparse.ArgumentParser(description='Generate public transport quality gradings (ÖV-Güteklassen 2018)')
    parser.add_argument('--config', default='generator_config.yml', metavar="filename",
                        help='specify a configuration file location. A default config will be created'
                             ' if the path does not exist. Default: generator_config.yml')
    parser.add_argument('-v', action='store_true', help='verbose log output')

    result = parser.parse_args(params)
    return result.config, result.v


def _setup_logging(verbose) -> None:
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
            '[%(levelname)-7s] - %(message)s')
    if verbose:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)-7s] - %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.debug("Setting up logging complete")