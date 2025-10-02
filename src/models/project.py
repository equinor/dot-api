import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean
from src.models.guid import GUID
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.event import listens_for
from typing import Optional, TYPE_CHECKING
from src.models.base import Base
from src.models.base_entity import BaseEntity
from src.models.base_auditable_entity import BaseAuditableEntity
from src.constants import DatabaseConstants

if TYPE_CHECKING:
    from models.scenario import Scenario
    from models.project_role import ProjectRole
from sqlalchemy import DateTime
from datetime import timedelta

def default_endtime() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=30)

class Project(Base, BaseEntity, BaseAuditableEntity):
    __tablename__ = "project"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True)
    name: Mapped[str] = mapped_column(
        String(DatabaseConstants.MAX_SHORT_STRING_LENGTH.value), index=True
    )
    description: Mapped[str] = mapped_column(String(DatabaseConstants.MAX_LONG_STRING_LENGTH.value))

    public: Mapped[bool] = mapped_column(Boolean, default=False)

    scenarios: Mapped[list["Scenario"]] = relationship(
        "Scenario",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    project_role: Mapped[list["ProjectRole"]] = relationship(
        "ProjectRole",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    end_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=default_endtime()
    )

    def __init__(
        self,
        id: uuid.UUID,
        description: str,
        name: str,
        project_role: list["ProjectRole"],
        user_id: int,
        scenarios: Optional[list["Scenario"]],
        public: bool = False,
        end_date: datetime = default_endtime(),
    ):
        self.id = id

        if scenarios is not None:
            self.scenarios = scenarios

        self.project_role = project_role
        self.name = name
        self.description = description
        self.updated_by_id = user_id
        self.public=public
        self.end_date=end_date

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"


@listens_for(Project, "before_insert")
def set_created_by_id(mapper, connection, target: Project):  # type: ignore
    target.created_by_id = target.updated_by_id
