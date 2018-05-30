import datetime


def mock_output_config() -> dict:
    return {
        'output-directory': 'results/',
        'metadata-filename': 'oevgk18_metadata.json',
        'transport-stops-filename': 'transport_stops.geojson'
    }


def mock_due_date_config() -> dict:
    return {
        'type-of-day': 'Working Day',
        'type-of-interval': 'Day',
        'due-date': datetime.datetime(2018, 11, 13, 0, 0),
        'lower-bound': '06:00',
        'upper-bound': '20:00'
    }