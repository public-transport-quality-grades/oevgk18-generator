from datetime import datetime
from os import path
from shutil import copyfile

import jsonschema
import ruamel.yaml

SAMPLE_CONFIG_PATH = 'sample_config.yml'

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
        },
        "color": {
            "type": "string",
            "pattern": "^#[A-Fa-f0-9]{6}$"
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
        "isochrones": {
            "$id": "/properties/isochrones",
            "type": "object",
            "properties": {
                "max-relevant-distance": {
                    "$id": "/properties/isochrones/properties/max-relevant-distance",
                    "type": "number"
                },
                "edge-segment-length": {
                    "$id": "/properties/isochrones/properties/edge-segment-length",
                    "type": "number"
                },
                "walking-speed": {
                    "$id": "/properties/isochrones/properties/walking-speed",
                    "type": "number"
                }
            },
            "additionalProperties": False,
            "required": ["max-relevant-distance", "edge-segment-length", "walking-speed"]
        },
        "output": {
            "$id": "/properties/isochrones",
            "type": "object",
            "properties": {
                "output-directory": {
                    "type": "string"
                },
                "metadata-filename": {
                    "type": "string"
                },
                "transport-stops-filename": {
                    "type": "string"
                }
            },
            "additionalProperties": False,
            "requiredProperties": ["output-directory", "metadata-filename", "transport-stops-filename"]
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
                            "$id": "/properties/transport-stop-categories/items/properties/"
                                   "transport-type-mappings/items",
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
                    "max-seconds": {
                        "$id": "/properties/public-transport-ratings/items/properties/max-seconds",
                        "type": "integer"
                    },
                    "transport-stop-categories": {
                        "$id": "/properties/public-transport-ratings/items/properties/transport-stop-categories",
                        "type": "array",
                        "items": {
                            "$id": "/properties/public-transport-ratings/items/properties/"
                                   "transport-stop-categories/items",
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
                "required": ["max-seconds", "transport-stop-categories"]

            }
        }
    }
}


def load_config(config_path: str) -> dict:
    """
    Loads the configuration and creates the default configuration if it does not yet exist.
    """

    if not path.exists(config_path):
        _create_default_config(config_path)

    with open(config_path, 'r') as f:
        config = ruamel.yaml.load(f, ruamel.yaml.RoundTripLoader)

    jsonschema.validate(config, SCHEMA, format_checker=jsonschema.FormatChecker())

    return _parse_dates(config)


def _create_default_config(config_path: str):
    """
    Creates the default configuration file.
    """
    copyfile(SAMPLE_CONFIG_PATH, config_path)


def _parse_dates(config: dict) -> dict:
    """Parse due dates as datetime objects"""
    for due_date_config in config['due-dates']:
        due_date_config['due-date'] = datetime.strptime(due_date_config['due-date'], "%Y-%m-%d")

    return config
