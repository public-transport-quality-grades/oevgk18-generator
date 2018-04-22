

mocked_return_values = {
    '8503400': 9,
    '8503125': 5,
    '8591382': 0
}




def get_count_of_distinct_next_stops(db_config: dict, uic_ref: str) -> int:
    return mocked_return_values[uic_ref]
