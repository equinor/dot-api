from typing import Any
from sqlalchemy import event
from sqlalchemy.orm import Session
from src.events.discrete_probability_event_handler import DiscreteProbabilityEventHandler

@event.listens_for(Session, 'after_flush')
def after_flush_event_handler(session: Session, flush_context: Any) -> None:
    DiscreteProbabilityEventHandler().process_session_changes_after_flush(session)