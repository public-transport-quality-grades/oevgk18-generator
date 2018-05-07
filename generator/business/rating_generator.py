import logging
from . import transport_stop_rating_calculator

logger = logging.getLogger(__name__)


def start(registry: dict, params):
    cli = registry['ui']
    cli.parse_params(params)
    for due_date_config in registry['config']['due-dates'][:1]:
        # TODO execute for all configurations
        transport_rating = \
            transport_stop_rating_calculator.calculate_transport_stop_ratings(registry, due_date_config)