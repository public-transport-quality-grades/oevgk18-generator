import sys
from generator.business import core
from generator.ui import cli
from generator.integration import routing_engine_service, timetable_service, transport_stop_service
from generator.output import geojson_writer, metadata_writer


def wire() -> dict:
    registry = dict()
    registry['ui'] = cli
    registry['routing_engine_service'] = routing_engine_service
    registry['timetable_service'] = timetable_service
    registry['output_writer'] = geojson_writer
    registry['metadata_writer'] = metadata_writer
    registry['transport_stop_service'] = transport_stop_service
    return registry


def main() -> None:
    input_params = sys.argv[1:]
    registry = wire()
    core.calculate_quality_grades(registry, input_params)


if __name__ == "__main__":
    main()
