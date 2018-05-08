
def get_registry(timetable_service=None, transport_stop_service=None):
    return {
        'timetable_service': timetable_service,
        'transport_stop_service': transport_stop_service,
        'config': {
            'database-connections': {},
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
            ]
        }
    }
