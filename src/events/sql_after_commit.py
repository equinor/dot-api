from sqlalchemy import event
from sqlalchemy.orm import Session

@event.listens_for(Session, 'after_commit')
def after_commit_event_handler(session: Session) -> None:
    # Clear the session info after successful commit
    session.info.clear()