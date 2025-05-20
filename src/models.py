from typing import Optional
from datetime import datetime
from sqlalchemy.sql.schema import MetaData
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import (
    Mapped, 
    relationship, 
    mapped_column,
)

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(30))
    azure_id: Mapped[str] = mapped_column(unique=True)

    def __init__(self, id: Optional[int], name: str, azure_id: str):
        if id is not None:
            self.id = id
        self.name = name
        self.azure_id = azure_id

    def __repr__(self) -> str:
        return f"id: {self.id}, name: {self.name}, azure_id: {self.azure_id}"
    
class BaseAuditableEntity:
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(default=func.now())

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(default=func.now(), onupdate=func.now())

    @declared_attr
    def created_by_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey(User.id))

    @declared_attr
    def updated_by_id(cls) -> Mapped[int]:
        return mapped_column(ForeignKey(User.id))

    @declared_attr
    def created_by(cls) -> Mapped["User"]:
        return relationship(User, foreign_keys=[cls.created_by_id]) # type: ignore # reason: declared_attr does not check in time

    @declared_attr
    def updated_by(cls) -> Mapped["User"]:
        return relationship(User, foreign_keys=[cls.updated_by_id]) # type: ignore # reason: declared_attr does not check in time


class Project(Base, BaseAuditableEntity):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(60), index=True)
    description: Mapped[str] = mapped_column(String(600))

    opportunities: Mapped[list["Opportunity"]] = relationship(
        "Opportunity",
        cascade="all, delete-orphan",
    )

    objectives: Mapped[list["Objective"]] = relationship(
        "Objective",
        cascade="all, delete-orphan",
    )

    graphs: Mapped[list["Graph"]] = relationship(
        "Graph", 
        back_populates="project",
        cascade="all, delete-orphan",
    )

    def __init__(self, id: Optional[int], description: str, name: str, user_id: int, objectives: list["Objective"], opportunities: list["Opportunity"]):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.name = name
        self.description = description
        self.updated_by_id = user_id
        self.objectives=objectives
        self.opportunities=opportunities

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"
    
class Opportunity(Base, BaseAuditableEntity):
    __tablename__ = "opportunity"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey(Project.id), index=True)

    name: Mapped[str] = mapped_column(String(60), index=True, default="")
    description: Mapped[str] = mapped_column(String(600), default="")

    project: Mapped[Project] = relationship(
        Project, 
        foreign_keys=[project_id],
        back_populates="opportunities",
    )

    def __init__(self, id: Optional[int], project_id: int, description: str, name: str, user_id: int):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.project_id = project_id
        self.name = name
        self.description = description
        self.updated_by_id = user_id

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"
    
class Objective(Base, BaseAuditableEntity):
    __tablename__ = "objective"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey(Project.id), index=True)

    name: Mapped[str] = mapped_column(String(60), index=True, default="")
    description: Mapped[str] = mapped_column(String(600), default="")

    project: Mapped[Project] = relationship(
        Project, 
        foreign_keys=[project_id],
        back_populates="objectives",
    )

    def __init__(self, id: Optional[int], project_id: int, description: str, name: str, user_id: int):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.project_id = project_id
        self.name = name
        self.description = description
        self.updated_by_id = user_id

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"

class Graph(Base, BaseAuditableEntity):
    __tablename__ = "graph"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey(Project.id), index=True)

    name: Mapped[str] = mapped_column(String(60), index=True, default="")

    project: Mapped[Project] = relationship(Project, foreign_keys=[project_id])

    nodes: Mapped[list["Node"]] = relationship(
        "Node", 
        back_populates="graph", 
        cascade="all, delete-orphan",
    )

    edges: Mapped[list["Edge"]] = relationship(
        "Edge",
        cascade="all, delete-orphan",
    )

    def __init__(self, id: Optional[int], name: str, project_id: int, user_id: int):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.name = name
        self.project_id = project_id
        self.updated_by_id = user_id

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}"
    
class Decision(Base):
    __tablename__ = "decision"
    id: Mapped[int] = mapped_column(primary_key=True)

    options: Mapped[str] = mapped_column(String(60), default="")

    def __init__(self, id: Optional[int], options: str):
        if id is not None:
            self.id = id
        self.options = options
    
class Probability(Base):
    __tablename__ = "probability"
    id: Mapped[int] = mapped_column(primary_key=True)

    probabilities: Mapped[str] = mapped_column(String, default="1")

    def __init__(self, id: Optional[int], probabilities: str):
        if id is not None:
            self.id = id
        self.probabilities = probabilities

class Node(Base, BaseAuditableEntity):
    __tablename__ = "node"

    id: Mapped[int] = mapped_column(primary_key=True)
    graph_id: Mapped[int] = mapped_column(ForeignKey(Graph.id))
    decision_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Decision.id))
    probability_id: Mapped[Optional[int]] = mapped_column(ForeignKey(Probability.id))

    type: Mapped[str] = mapped_column(String(30), default="TBD")

    graph: Mapped[Graph] = relationship(Graph, foreign_keys=[graph_id], back_populates="nodes")

    decision: Mapped[Optional[Decision]] = relationship(
        Decision, 
        foreign_keys=[decision_id], 
        cascade="all, delete-orphan",
        single_parent=True,
    )
    probability: Mapped[Optional[Probability]] = relationship(
        Probability, 
        foreign_keys=[probability_id], 
        cascade="all, delete-orphan",
        single_parent=True,
    )

    higher_edges: Mapped[list["Edge"]] = relationship(
        "Edge",
        foreign_keys="[Edge.higher_id]",
        back_populates="higher_node",
        cascade="all, delete-orphan",
    )
    lower_edges: Mapped[list["Edge"]] = relationship(
        "Edge",
        foreign_keys="[Edge.lower_id]",
        back_populates="lower_node",
        cascade="all, delete-orphan",
    )

    def __init__(self, id: Optional[int], graph_id: int, type: str, user_id: int, decision_id: Optional[int] = None, probability_id: Optional[int] = None, decision: Optional[Decision] = None, probability: Optional[Probability] = None):
        if id is not None:
            self.id = id
        else:
            self.created_by_id = user_id

        self.graph_id = graph_id
        self.type = type
        self.decision_id = decision_id
        self.decision = decision
        self.probability_id = probability_id
        self.probability = probability
        self.updated_by_id = user_id

    def higher_neighbors(self) -> list["Node"]:
        # self.higher_edges: list["Edge"]
        try:
            return [x.higher_node for x in self.higher_edges]
        except:
            return []

    def lower_neighbors(self) -> list["Node"]:
        # self.lower_edges: list["Edge"]
        try:
            return [x.lower_node for x in self.lower_edges]
        except:
            return []

class Edge(Base):
    __tablename__ = "edge"

    id: Mapped[int] = mapped_column(primary_key=True)

    lower_id: Mapped[int] = mapped_column(ForeignKey(Node.id))
    higher_id: Mapped[int] = mapped_column(ForeignKey(Node.id))
    graph_id: Mapped[int] = mapped_column(ForeignKey(Graph.id))

    graph: Mapped[Graph] = relationship(Graph, foreign_keys=[graph_id])

    lower_node: Mapped[Node] = relationship(
        Node, 
        primaryjoin=lower_id == Node.id, 
        back_populates="lower_edges",
    )

    higher_node: Mapped[Node] = relationship(
        Node, 
        primaryjoin=higher_id == Node.id, 
        back_populates="higher_edges", 
    )

    def __init__(self, id: Optional[int], lower_node_id: int, higher_node_id: int, graph_id: int):
        if id is not None:
            self.id = id
        self.lower_id = lower_node_id
        self.higher_id = higher_node_id
        self.graph_id = graph_id

metadata: MetaData = Base.metadata