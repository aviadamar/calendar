from datetime import date, timedelta
from typing import List, Optional

import arrow
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database.models import Event
from app.internal.utils import get_all_user_events


def get_events_per_dates(
        session: Session,
        user_id: int,
        start: Optional[date],
        end: Optional[date]
) -> List[Event]:
    """Read from the db. Return a list of all
    the user events between the relevant dates."""

    if start > end:
        return []
    try:
        events = (
            filter_dates(
                sort_events_by_date(
                    get_all_user_events(session, user_id)
                ),
                start,
                end,
            )
        )
    except SQLAlchemyError:
        return []
    else:
        return events


def build_arrow_delta_granularity(diff: timedelta) -> List[str]:
    """Builds the granularity for the arrow module string"""
    granularity = []
    if diff.days > 0:
        granularity.append("day")
    hours, remainder = divmod(diff.seconds, 60 * 60)
    if hours > 0:
        granularity.append("hour")
    minutes, _ = divmod(remainder, 60)
    if minutes > 0:
        granularity.append("minute")
    return granularity


def get_time_delta_string(start: date, end: date) -> str:
    """Builds a string of the event's duration- days, hours and minutes."""
    arrow_start = arrow.get(start)
    arrow_end = arrow.get(end)
    diff = end - start
    granularity = build_arrow_delta_granularity(diff)
    duration_string = arrow_end.humanize(
        arrow_start, only_distance=True, granularity=granularity
    )
    return duration_string


def sort_events_by_date(events: List[Event]) -> List[Event]:
    """Sorts the events by the start of the event."""

    events.sort(key=lambda event: event.start)
    return events


def filter_dates(
        events: List[Event], start: Optional[date],
        end: Optional[date]) -> List[Event]:
    """filter events by a time frame."""

    return [
        event for event in events
        if start <= event.start.date() <= end
    ]
