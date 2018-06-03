import logging
from datetime import time, datetime, timedelta
from typing import List, Dict, Optional

from ..business.model.transport_stop import TransportStop
from ..types import Intervals

logger = logging.getLogger(__name__)


def calculate_stop_intervals(
        registry: dict, due_date_config: dict, stops: List[TransportStop]) -> Intervals:
    """Calculate the departure interval in specified time bounds of public transport stops"""
    logger.info("Calculate Transport stop intervals")

    timetable_service = registry['timetable_service']
    db_config = registry['config']['database-connections']
    due_date: datetime = due_date_config['due-date']
    start_time: datetime = _parse_time(due_date_config['lower-bound'], due_date)
    end_time: datetime = _parse_time(due_date_config['upper-bound'], due_date)

    all_departure_times: Dict = timetable_service.get_all_departure_times(db_config, due_date)

    return {stop.uic_ref: _get_stop_interval(stop.uic_ref, all_departure_times, start_time, end_time)
            for stop in stops}


def _get_stop_interval(uic_ref: int, all_departures: Dict[int, List[datetime]],
                       start_time: datetime, end_time: datetime) -> Optional[float]:
    stop_departures: List[datetime] = all_departures.get(uic_ref)
    if not stop_departures:
        logger.debug(f"{uic_ref}: No departures found")
        return None
    interval = _calculate_stop_interval(stop_departures, start_time, end_time)
    if not interval:
        logger.debug(f"{uic_ref}: No departures in interval {start_time} - {end_time}")
        return None
    logger.debug(f"{uic_ref}: Interval is {interval / 60} min")
    return interval


def _calculate_stop_interval(stop_departures: List[datetime], start_time: datetime,
                             end_time: datetime) -> Optional[float]:
    departures: List[datetime] = list(filter(
        lambda t: _departure_time_inside_interval(t, start_time, end_time), stop_departures))

    if not departures:
        return None

    if len(departures) == 1:
        # if there is just one departure, duplicate it to use it as start and end
        departures += departures

    departures.sort()

    interval_delta: timedelta = end_time - start_time

    first_fictional_departure_after_interval: datetime = departures[0] + interval_delta

    departures_after_interval = list(filter(lambda t: t > end_time, stop_departures))
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
