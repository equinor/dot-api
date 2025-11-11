import uuid

from sqlalchemy.orm import Session
from pydantic import BaseModel

class SessionInfo(BaseModel):
    affected_uncertainties: set[uuid.UUID] = set()

class SessionInfoHandler:
    @staticmethod
    def get_session_info(session: Session) -> SessionInfo:
        return SessionInfo(**session.info)

    @staticmethod
    def update_session_info(session: Session, session_info: SessionInfo):
        session.info.update(session_info)