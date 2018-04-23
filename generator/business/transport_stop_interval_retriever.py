from typing import List
from datetime import time, datetime, timedelta


def get_transport_stop_interval(registry: dict,  due_date_config: dict, uic_ref: str) -> float:
    """Calculate the departure interval in specified time bounds of one public transport stop"""

    timetable_service = registry['timetable_service']
    db_config = registry['config']['database-connections']
    due_date: datetime = due_date_config['due-date']
    start_time: datetime = _parse_time(due_date_config['lower-bound'])
    end_time: datetime = _parse_time(due_date_config['upper-bound'])

    with timetable_service.db_connection(db_config) as db:
        all_departures: List[datetime] = timetable_service.get_departure_times(db, uic_ref, due_date)

    return _calculate_transport_stop_interval(all_departures, start_time, end_time)


def _calculate_transport_stop_interval(
        all_departures: List[datetime], start_time: datetime, end_time: datetime) -> float:

    departures: List[datetime] = list(filter(
        lambda t: _departure_time_inside_interval(t, start_time, end_time), all_departures))

    departures.sort()

    print(f"departures: {departures}")

    interval_delta: timedelta = end_time - start_time

    first_scheduled_departure_after_interval: datetime = min(filter(lambda t: t > end_time, all_departures))
    # TODO: Handle if end_time is midnight, there are no departures after that
    first_fictional_departure_after_interval: datetime = departures[0] + interval_delta

    end_departure = min(first_scheduled_departure_after_interval, first_fictional_departure_after_interval)

    waiting_delta_sum = sum([
        _calculate_waiting_delta(i, departures, end_departure, start_time, end_time)
        for i in range(len(departures))])

    return float(waiting_delta_sum) / interval_delta.seconds


def _parse_time(time_str: str, due_date: datetime) -> datetime:
    """parse string from format hh:mm to time"""
    hours, minutes = time_str.split(':')
    parsed_time = time(hour=int(hours), minute=int(minutes))
    parsed_date = datetime.combine(due_date, parsed_time)
    if parsed_time == time(0, 0):
        return parsed_date + timedelta(days=1)
    return parsed_date


def _departure_time_inside_interval(t: datetime, start_time: datetime, end_time: datetime) -> bool:
    if not start_time <= t < end_time:
        print(f"{t} is not in interval")
    return start_time <= t < end_time


def _calculate_waiting_delta(
        i: int, departures: List[datetime], end_departure: datetime, start_time: datetime, end_time: datetime) -> int:

    if i == len(departures) - 1:
        return (end_departure - departures[-1]).seconds ** 2 - (end_departure - end_time).seconds ** 2
    elif i == 0:
        return (departures[0] - start_time).seconds ** 2
    else:
        return (departures[i+1] - departures[i]).seconds ** 2
