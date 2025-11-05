from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import event
from src.models import (DiscreteProbabilityParentOption, DiscreteProbabilityParentOutcome)

@event.listens_for(Session, 'before_flush')
def handle_deleted_entities_in_session(session: Session, flush_context: Any, instances: Any) -> None:
    """Delete DiscreteProbability if all parent associations are removed."""
    # Find discrete probabilities that will have no parent associations after flush
    if not session.deleted: return
    actionable_objects: set[DiscreteProbabilityParentOutcome|DiscreteProbabilityParentOption] = set(
        filter(lambda item: isinstance(item, (DiscreteProbabilityParentOutcome, DiscreteProbabilityParentOption)), session.deleted)
    )

    if len(actionable_objects)==0: return
    # set of objects that have been handled and must be ignored in future iterations
    handled_objects: set[Any] = set()
    for obj in actionable_objects:
        if obj in handled_objects: continue

        # handle probability helper tables
        if isinstance(obj, (DiscreteProbabilityParentOutcome, DiscreteProbabilityParentOption)):
            discrete_prob = obj.discrete_probability
            if discrete_prob in handled_objects: continue

            # should cascade delete to the other parents
            session.delete(discrete_prob)
            handled_objects.add(discrete_prob)
