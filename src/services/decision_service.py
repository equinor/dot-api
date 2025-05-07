from sqlalchemy.orm import Session
from sqlalchemy import Engine

from src.models import Decision
from dtos.decision_dtos import (
    DecisionIncommingDto, 
    DecisionOutgoingDto, 
    DecisionMapper
)
from repositories.decision_repository import DecisionRepository

class DecisionService:
    def __init__(self, engine: Engine):
        self.engine=engine

    def create(self, dtos: list[DecisionIncommingDto]) -> list[DecisionOutgoingDto]:
        with Session(self.engine, autoflush=True, autocommit=False) as session:
            try:
                decisions: list[Decision] = DecisionRepository(session).create(DecisionMapper.to_entities(dtos))
                session.commit()
            except Exception as e:
                session.rollback()
                raise e
        return DecisionMapper.to_outgoing_dtos(decisions)
    
    def get(self, ids: list[int]) -> list[DecisionOutgoingDto]:
        with Session(self.engine, autoflush=True, autocommit=False) as session:
            decisions: list[Decision] = DecisionRepository(session).retrieve(ids)
        return DecisionMapper.to_outgoing_dtos(decisions)