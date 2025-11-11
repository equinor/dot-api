from typing import Any
from sqlalchemy import event
from sqlalchemy.orm import Session
from src.events.discrete_probability_event_handler import DiscreteProbabilityEventHandler

@event.listens_for(Session, 'before_flush')
def before_flush_event_handler(session: Session, flush_context: Any, instances: Any) -> None:
    DiscreteProbabilityEventHandler().process_session_changes_before_flush(session)