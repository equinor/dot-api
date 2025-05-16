from sqlalchemy.orm.strategy_options import _AbstractLoad # # type: ignore
from sqlalchemy.orm import selectinload
from src.models import *

def load_project_relations_basic() -> list[_AbstractLoad]:
    return [
        selectinload(Project.opportunities),
        selectinload(Project.objectives),
    ]

def load_project_relations_all() -> list[_AbstractLoad]:
    return [
        selectinload(Project.opportunities),
        selectinload(Project.objectives),
        selectinload(Project.graphs).options(*load_graph_relations())
    ]

def load_graph_relations() -> list[_AbstractLoad]:
    return [
        selectinload(Graph.edges),
        selectinload(Graph.nodes).options(*load_node_relations())
    ]

def load_node_relations() -> list[_AbstractLoad]:
    return [
        selectinload(Node.decision),
        selectinload(Node.probability),
    ]