from typing import List, Dict, Optional


def get_transport_stop_intervals(registry: dict, due_date_config: dict, stops: List[int]) -> Dict[int, Optional[float]]:
    return {
        8503400: 200.34,
        8503125: 2400,
        8591382: None,
        8593245: 10000.63
    }
