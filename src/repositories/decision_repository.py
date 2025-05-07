from src.models import Decision
from sqlalchemy.orm import Session

class DecisionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, decisions: list[Decision]) -> list[Decision]:
        self.session.add_all(decisions)
        self.session.flush()
        return decisions

    def retrieve(self, ids: list[int]) -> list[Decision]:
        return (
            self.session
                .query(Decision)
                .where(Decision.id.in_(ids))
                .all()
        )
    
