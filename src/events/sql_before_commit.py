from sqlalchemy import event
from sqlalchemy.orm import Session
from src.events.discrete_probability_event_handler import DiscreteProbabilityEventHandler

@event.listens_for(Session, 'before_commit')
def before_commit_event_handler(session: Session) -> None:
    DiscreteProbabilityEventHandler().recalculate_affected_probabilities(session)