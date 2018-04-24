from os import path
from datetime import datetime
import ruamel.yaml
import jsonschema

DEFAULT_CONFIG = """
database-connections:
    public-transport-stops: "postgres://test:test@localhost:5432/oevgk18"

due-dates:
    - type-of-day: "Working Day"
      type-of-interval: "Day"
      due-date: "2018-11-13"
      lower-bound: '06:00'
      upper-bound: '20:00'

    - type-of-day: "Working Day"
      type-of-interval: "Evening"
      due-date: "2018-11-13"
      lower-bound: '20:00'
      upper-bound: '00:00'

    - type-of-day: "Saturday"
      type-of-interval: "Day"
      due-date: "2018-11-10"
      lower-bound: '06:00'
      upper-bound: '20:00'

    - type-of-day: "Saturday"
      type-of-interval: "Night"
      due-date: "2018-11-10"
      lower-bound: '01:00'
      upper-bound: '04:00'

    - type-of-day: "Sunday"
      type-of-interval: "Day"
      due-date: "2018-11-18"
      lower-bound: '06:00'
      upper-bound: '20:00'

    - type-of-day: "Sunday"
      type-of-interval: "Night"
      due-date: "2018-11-18"
      lower-bound: '01:00'
      upper-bound: '04:00'

public-transport-types:
    train-junction-min-directions: 6 # Minimum amount of directions for a train station to be called a train junction ("Bahnknoten")

transport-stop-categories:
    - max-interval: 300 # seconds
      transport-type-mappings:
          - A: 1 # i.e. types of transports in category A are in transport stop category I
          - B: 1
          - C: 2

    - min-interval: 301
      max-interval: 600
      transport-type-mappings:
          - A: 1
          - B: 2
          - C: 3

    - min-interval: 601
      max-interval: 1200
      transport-type-mappings:
          - A: 2
          - B: 3
          - C: 4
    
    - min-interval: 1201
      max-interval: 2400
      transport-type-mappings:
          - A: 3
          - B: 4
          - C: 5
    
    - min-interval: 2401
      max-interval: 3600
      transport-type-mappings:
          - A: 4
          - B: 5
          - C: 6
    
    - min-interval: 3601
      transport-type-mappings:
          - B: 7
          - C: 7

public-transport-ratings:
    - min-seconds: 0
      max-seconds: 300
      transport-stop-categories:
          - 1: 'A' # i.e. transport stop category I gets a transport stop rating 'A'
          - 2: 'A'
          - 3: 'B'
          - 4: 'C'
          - 5: 'D'
          - 6: 'E'
          - 7: 'F'
    
    - min-seconds: 301
      max-seconds: 450
      transport-stop-categories:
          - 1: 'A'
          - 2: 'B'
          - 3: 'C'
          - 4: 'D'
          - 5: 'E'
    
    - min-seconds: 451
      max-seconds: 600
      transport-stop-categories:
          - 1: 'B'
          - 2: 'C'
          - 3: 'D'
          - 4: 'E'
    
    - min-seconds: 601
      max-seconds: 900
      transport-stop-categories:
          - 1: 'C'
          - 2: 'D'
          - 3: 'E'
"""

SCHEMA = {
    "type": "object",
    "definitions": {
        "time-string": {
            "type": "string",
            "pattern": "^\d{2}:\d{2}$"
        },
        "transport-stop-interval": {
            "type": "integer",
            "minimum": 0
        },
        "pt-stop-category": {
            "type": "integer",
            "minimum": 1,
            "maximum": 7
        },
        "pt-rating-category": {
            "type": "string",
            "pattern": "^[A-F]$"
        }
    },
    "$schema": "http://json-schema.org/draft-07/schema#",
    "properties": {
        "database-connections": {
            "$id": "/properties/database-connections",
            "type": "object",
            "properties": {
                "public-transport-stops": {
                    "type": "string"
                }
            },
            "additionalProperties": False,
            "required": ["public-transport-stops"]
        },
        "due-dates": {
            "$id": "/properties/due-dates",
            "type": "array",
            "items": {
                "$id": "/properties/due-dates/items",
                "type": "object",
                "properties": {
                    "type-of-day": {
                        "$id": "/properties/due-dates/items/properties/type-of-day",
                        "type": "string"
                    },
                    "type-of-interval": {
                        "$id": "/properties/due-dates/items/properties/type-of-interval",
                        "type": "string"
                    },
                    "due-date": {
                        "$id": "/properties/due-dates/items/properties/due-date",
                        "type": "string",
                        "format": "date"
                    },
                    "lower-bound": {
                        "$id": "/properties/due-dates/items/properties/lower-bound",
                        "$ref": "#/definitions/time-string"
                    },
                    "upper-bound": {
                        "$id": "/properties/due-dates/items/properties/upper-bound",
                        "$ref": "#/definitions/time-string"
                    }
                },
                "additionalProperties": False,
                "required": ["type-of-day", "type-of-interval", "due-date", "lower-bound", "upper-bound"]
            }
        },
        "public-transport-types": {
            "$id": "/properties/public-transport-types",
            "type": "object",
            "properties": {
                "train-junction-min-directions": {
                    "$id": "/properties/public-transport-types/properties/train-junction-min-directions",
                    "type": "integer"
                }
            },
            "additionalProperties": False,
            "required": ["train-junction-min-directions"]

        },
        "transport-stop-categories": {
            "$id": "/properties/transport-stop-categories",
            "type": "array",
            "items": {
                "$id": "/properties/transport-stop-categories/items",
                "type": "object",
                "properties": {
                    "max-interval": {
                        "$id": "/properties/transport-stop-categories/items/properties/max-interval",
                        "$ref": "#/definitions/transport-stop-interval"
                    },
                    "min-interval": {
                        "$id": "/properties/transport-stop-categories/items/properties/max-interval",
                        "$ref": "#/definitions/transport-stop-interval"
                    },
                    "transport-type-mappings": {
                        "$id": "/properties/transport-stop-categories/items/properties/transport-type-mappings",
                        "type": "array",
                        "items": {
                            "$id": "/properties/transport-stop-categories/items/properties/transport-type-mappings/items",
                            "type": "object",
                            "properties": {
                                "A": {
                                    "$ref": "#/definitions/pt-stop-category"
                                },
                                "B": {
                                    "$ref": "#/definitions/pt-stop-category"
                                },
                                "C": {
                                    "$ref": "#/definitions/pt-stop-category"
                                }
                            },
                            "additionalProperties": False,
                        }
                    }
                },
                "additionalProperties": False,
                "required": ["transport-type-mappings"]

            }
        },
        "public-transport-ratings": {
            "$id": "/properties/public-transport-ratings",
            "type": "array",
            "items": {
                "$id": "/properties/public-transport-ratings/items",
                "type": "object",
                "properties": {
                    "min-seconds": {
                        "$id": "/properties/public-transport-ratings/items/properties/min-seconds",
                        "type": "integer"
                    },
                    "max-seconds": {
                        "$id": "/properties/public-transport-ratings/items/properties/max-seconds",
                        "type": "integer"
                    },
                    "transport-stop-categories": {
                        "$id": "/properties/public-transport-ratings/items/properties/transport-stop-categories",
                        "type": "array",
                        "items": {
                            "$id": "/properties/public-transport-ratings/items/properties/transport-stop-categories/items",
                            "type": "object",
                            "properties": {
                                1: {
                                    "$ref": "#/definitions/pt-rating-category"
                                },
                                2: {
                                    "$ref": "#/definitions/pt-rating-category"
                                },
                                3: {
                                    "$ref": "#/definitions/pt-rating-category"
                                },
                                4: {
                                    "$ref": "#/definitions/pt-rating-category"
                                },
                                5: {
                                    "$ref": "#/definitions/pt-rating-category"
                                },
                                6: {
                                    "$ref": "#/definitions/pt-rating-category"
                                },
                                7: {
                                    "$ref": "#/definitions/pt-rating-category"
                                }
                            },
                            "additionalProperties": False,
                        }
                    }
                },
                "additionalProperties": False,
                "required": ["min-seconds", "max-seconds", "transport-stop-categories"]

            }
        }
    }
}


def load_config(config_path: str) -> dict:
    """
    Loads the configuration and creates the default configuration if it does not yet exist.
    """

    if not path.exists(config_path):
        create_default_config(config_path)

    with open(config_path, 'r') as f:
        config = ruamel.yaml.load(f, ruamel.yaml.RoundTripLoader)

    jsonschema.validate(config, SCHEMA, format_checker=jsonschema.FormatChecker())

    return _parse_dates(config)


def create_default_config(config_path: str):
    """
    Creates the default configuration file.
    """
    with open(config_path, 'w') as f:
        f.write(DEFAULT_CONFIG)


def _parse_dates(config: dict) -> dict:
    """Parse due dates as datetime objects"""
    for due_date_config in config['due-dates']:
        due_date_config['due-date'] = datetime.strptime(due_date_config['due-date'], "%Y-%m-%d")

    return config
