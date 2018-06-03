def get_registry(timetable_service=None, transport_stop_service=None, routing_engine_service=None):
    return {
        'timetable_service': timetable_service,
        'transport_stop_service': transport_stop_service,
        'routing_engine_service': routing_engine_service,
        'config': {
            'database-connections': {},
            'isochrones': {
                'walking-speed': 1.5
            },
            'public-transport-types': {
                'train-junction-min-directions': 6
            },
            "transport-stop-categories": [
                {
                    "max-interval": 300,
                    "transport-type-mappings": [
                        {
                            "A": 1
                        },
                        {
                            "B": 1
                        },
                        {
                            "C": 2
                        }
                    ]
                },
                {
                    "min-interval": 1200,
                    "max-interval": 2400,
                    "transport-type-mappings": [
                        {
                            "A": 3
                        },
                        {
                            "B": 4
                        },
                        {
                            "C": 5
                        }
                    ]
                },
                {
                    "min-interval": 2400,
                    "transport-type-mappings": [
                        {
                            "B": 7
                        },
                        {
                            "C": 7
                        }
                    ]
                }
            ],
            "public-transport-ratings": [
                {
                    "max-seconds": 300,
                    "transport-stop-categories": [
                        {
                            1: "A"
                        },
                        {
                            2: "B"
                        },
                        {
                            3: "C"
                        }
                    ]
                },
                {
                    "max-seconds": 600,
                    "transport-stop-categories": [
                        {
                            1: "D"
                        },
                        {
                            2: "E"
                        },
                    ]
                },
                {
                    "max-seconds": 900,
                    "transport-stop-categories": [
                        {
                            1: "F"
                        },
                    ]
                }
            ]
        }
    }
