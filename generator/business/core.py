import logging

from . import stop_category_calculator, transport_group_retriever, stop_grade_calculator
from ..types import TransportGroups, TransportStopCategories, TransportStopGradings

logger = logging.getLogger(__name__)


def calculate_quality_grades(registry: dict, params: list) -> None:
    cli = registry['ui']
    cli.setup_cli(params, registry)

    stop_grade_calculator.prepare_calculation(registry)
    transport_groups: TransportGroups = transport_group_retriever.get_transport_groups(registry)

    output_writer = registry['output_writer']
    config = registry['config']

    for due_date_config in config['due-dates']:
        logger.info(f"Calculate public transport quality grades with due date "
                    f"{due_date_config['due-date'].strftime('%Y-%m-%d')}, {due_date_config['type-of-interval']}")
        stop_categories: TransportStopCategories = \
            stop_category_calculator.get_stop_categories(registry, due_date_config, transport_groups)

        stop_gradings: TransportStopGradings = stop_grade_calculator.calculate_stop_grades(
            registry, stop_categories)

        output_writer.write_gradings(config['output'], due_date_config, stop_gradings)

        gradings_with_isochrones = [(uic_ref, gradings) for uic_ref, gradings in stop_gradings.items()
                                    if gradings]

        logger.debug(f"Found {len(gradings_with_isochrones)} stops with isochrones")

    metadata_writer = registry['metadata_writer']
    metadata_writer.write_metadata(config['output'], config['due-dates'])

    output_writer.write_transport_stops(config['output'], [*transport_groups])
