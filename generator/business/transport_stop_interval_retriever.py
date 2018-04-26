from typing import List, Dict
from datetime import time, datetime, timedelta


def get_transport_stop_intervals(registry: dict, due_date_config: dict, uic_refs: List[str]) -> Dict[str, float]:
    """Calculate the departure interval in specified time bounds of public transport stops"""

    timetable_service = registry['timetable_service']
    db_config = registry['config']['database-connections']
    due_date: datetime = due_date_config['due-date']
    start_time: datetime = _parse_time(due_date_config['lower-bound'], due_date)
    end_time: datetime = _parse_time(due_date_config['upper-bound'], due_date)

    with timetable_service.db_connection(db_config) as db:
        timetable_service.prepare_calendar_table(db, due_date)
        return {uic_ref: _get_transport_stop_interval(db, timetable_service, uic_ref, due_date, start_time, end_time)
                for uic_ref in uic_refs}


def _get_transport_stop_interval(db, timetable_service, uic_ref: str, due_date: datetime, start_time: datetime,
                                 end_time: datetime) -> float:
    all_departures: List[datetime] = timetable_service.get_departure_times(db, uic_ref, due_date)
    if not all_departures:
        print(f"No departures for uic_ref {uic_ref}")
        return None
    interval = _calculate_transport_stop_interval(all_departures, start_time, end_time)
    print(f"{uic_ref}: {interval / 60} min")
    return interval


def _calculate_transport_stop_interval(
        all_departures: List[datetime], start_time: datetime, end_time: datetime) -> float:
    departures: List[datetime] = list(filter(
        lambda t: _departure_time_inside_interval(t, start_time, end_time), all_departures))

    if len(departures) == 1:
        # if there is just one departure, duplicate it to use it as start and end
        departures += departures

    if not departures:
        print(f"No departures in interval {start_time} - {end_time}")
        return None

    interval_delta: timedelta = end_time - start_time

    first_fictional_departure_after_interval: datetime = departures[0] + interval_delta

    departures_after_interval = list(filter(lambda t: t > end_time, all_departures))
    if departures_after_interval:
        first_scheduled_departure_after_interval: datetime = min(departures_after_interval)
        end_departure = min(first_scheduled_departure_after_interval, first_fictional_departure_after_interval)
    else:
        end_departure = first_fictional_departure_after_interval

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
    return start_time <= t < end_time


def _calculate_waiting_delta(
        i: int, departures: List[datetime], end_departure: datetime, start_time: datetime, end_time: datetime) -> int:
    if i == len(departures) - 1:
        return (end_departure - departures[-1]).seconds ** 2 - (end_departure - end_time).seconds ** 2
    elif i == 0:
        return (departures[0] - start_time).seconds ** 2
    else:
        return (departures[i + 1] - departures[i]).seconds ** 2
