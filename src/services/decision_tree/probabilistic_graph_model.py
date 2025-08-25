"""Module defining the ProbabilisticGraphModel Abstract class"""

from __future__ import annotations

import importlib
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

import networkx as nx

if TYPE_CHECKING:  # pragma: no cover
    #from ..decision_diagrams.edge import Edge
    from src.dtos.issue_dtos import IssueOutgoingDto
    from src.dtos.edge_dtos import EdgeOutgoingDto


logger = logging.getLogger(__name__)


class ProbabilisticGraphModelABC(ABC):
    def __init__(self, *args, **kwargs):
        self.nx = nx.DiGraph(*args, **kwargs)

    @classmethod
    def from_dict(cls, data: dict):
        diagram = cls.initialize_diagram(data)
        for node in data["nodes"]:
            diagram.add_node(node)
        for edge in data.get("edges", []):
            diagram.add_edge(edge)
        return diagram

    @classmethod
    @abstractmethod
    def initialize_diagram(cls, data):
        """Initialize a diagram with data"""
        raise NotImplementedError

    #def add_node(self, node: NodeABC):
    def add_node(self, node: IssueOutgoingDto):
        self.nx.add_node(node)

    def add_edge(self, edge: EdgeOutgoingDto):
        nx_edge, nx_attributes = edge.to_nx()
        self.nx.add_edge(nx_edge[0], nx_edge[1], **nx_attributes)

    def copy(self):
        new_id = type(self)()  # Need to instance from the concrete class
        new_id.nx = self.nx.copy()
        return new_id

    def get_parents(self, node: IssueOutgoingDto) -> list[IssueOutgoingDto]:
        return list(self.nx.predecessors(node))

    def get_children(self, node: IssueOutgoingDto) -> list[IssueOutgoingDto]:
        return list(self.nx.successors(node))

    #def _get_nodes_from_type(self, node_type_string: str) -> list[NodeABC]:
    def _get_nodes_from_type(self, node_type_string: str) -> list[IssueOutgoingDto]:
        node_list = []
        for node in list(self.nx.nodes(data=True)):
            if (node[0].type == node_type_string):
                node_list.append(node[0])
        return node_list

    def has_children(self, node: IssueOutgoingDto) -> bool:
        return len(self.get_children(node)) > 0

    def to_json(self, filepath: Path = None) -> str:
        json_object = self._to_json_stream()
        if filepath:
            with open(filepath, "w") as outfile:
                outfile.write(json_object)
        return json_object

    @abstractmethod
    def _to_json_stream(self):
        raise NotImplementedError

    def get_node_from_uuid(self, uuid: str) -> IssueOutgoingDto:
        return [node for node in self.nx if node.uuid == uuid][0]
