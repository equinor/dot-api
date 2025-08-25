"""Module defining the DecisionTree class

A DecisionTree is a sub-class of ProbabilisticGraphModel.

    Raises:
        RootNodeNotFound: When trying to define a decision tree without giving the root
                          node

"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

import networkx as nx

from src.services.decision_tree.probabilistic_graph_model import ProbabilisticGraphModelABC

if TYPE_CHECKING:  # pragma: no cover
    from src.dtos.node_dtos import NodeOutgoingDto
    #from ..decision_diagrams.node import NodeABC


logger = logging.getLogger(__name__)


class RootNodeNotFound(Exception):
    def __init__(self):
        error_message = "Decision tree has no defined root node"
        super().__init__(error_message)
        logger.critical(error_message)


class DecisionTree(ProbabilisticGraphModelABC):
    """Decision tree class"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = kwargs.get("root", None)
        if self.root is not None:
            self.nx.add_node(self.root)

    @classmethod
    def initialize_diagram(cls, data: dict):
        roots = []
        g = nx.DiGraph([(arc.endpoint_start, arc.endpoint_end) for arc in data["edges"]])
        roots = [node for node in g.nodes if not list(g.predecessors(node))]
        if not len(roots) == 1:
            raise RootNodeNotFound
        return cls(root=roots[0])

    def set_root(self, root: NodeABC):
        self.root = root
        if not self.nx.has_node(root):
            self.add_node(root)

    def parent(self, node: NodeABC) -> NodeABC | None:
        parents = self.get_parents(node)
        return parents[0] if len(parents) > 0 else None

    def _to_json_stream(self) -> dict:
        """convert the decision tree instance into a dictionary
            It uses the method `networkx.readwrite.json_graph.tree_data()`

        Raises:
            RootNodeNotFound: Raised when no root has been set in the decision tree

        Returns:
            Dict: a representation of the tree
        """

        def propagate_branch_name(self, node, names):
            predecessor = self.parent(node)
            if not predecessor:
                return ""
            n = names[(predecessor, node)]
            return n if isinstance(n, str) else "-".join(n)

        if self.root is None:
            raise RootNodeNotFound

        edges_name = nx.get_edge_attributes(self.nx, "name")
        tg = nx.readwrite.json_graph.tree_data(self.nx, self.root)
        json_object = json.dumps(
            tg,
            default=lambda o: {
                **o.to_dict(),
                **{"branch_name": propagate_branch_name(self, o, edges_name)},
            },
            indent=2,
        )
        return json_object
