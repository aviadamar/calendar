from typing import List

from sqlalchemy.orm import Session

from app.database.models import Base, Event, UserEvent


def save(item, session: Session) -> bool:
    """Commits an instance to the db.
    source: app.database.database.Base"""

    if issubclass(item.__class__, Base):
        session.add(item)
        session.commit()
        return True
    return False


def get_all_user_events(session: Session, user_id: int) -> List[Event]:
    """Returns all events that the user participants in."""

    associations = (
        session.query(UserEvent)
        .filter(UserEvent.user_id == user_id)
        .all()
    )
    return [association.events for association in associations]


def create_model(session: Session, model_class, **kw):
    """Creates and saves a db model."""

    instance = model_class(**kw)
    session.add(instance)
    session.commit()
    return instance
