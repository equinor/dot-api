"""Module defining the ProbabilisticGraphModel Abstract class"""

from __future__ import annotations

import logging
import json
import networkx as nx
from src.dtos.issue_dtos import IssueOutgoingDto
from src.services.decision_tree.utils import EdgeDTDto


logger = logging.getLogger(__name__)

class RootNodeNotFound(Exception):
    def __init__(self):
        error_message = "Decision tree has no defined root node"
        super().__init__(error_message)
        logger.critical(error_message)


class DecisionTree():
    """Decision tree class"""

    def __init__(self, *args, **kwargs):
        self.nx = nx.DiGraph(*args, **kwargs)
        self.root = kwargs.get("root", None)
        print("First root", self.root)
        if self.root is not None:
            self.nx.add_node(self.root)

    async def set_root(self, root: IssueOutgoingDto):
        self.root = root
        if not self.nx.has_node(root):
            self.nx.add_node(root)

    async def add_node(self, node: IssueOutgoingDto):
        self.nx.add_node(node)
    
    async def add_edge(self, edge: EdgeDTDto):
        # print(f"Number of nodes: {self.nx.number_of_nodes()}")
        # print(f"Number of edges: {self.nx.number_of_edges()}")
        # print("Nodes in the graph:", self.nx.nodes())
        # print("Edges in the graph:", self.nx.edges())
        #print("Add edgde: ", edge.name)    
        attr = {'name': edge.name}
        self.nx.add_edge(edge.tail, edge.head, **attr)

    async def print_all(self):
        print(f"Number of nodes: {self.nx.number_of_nodes()}")
        print(f"Number of edges: {self.nx.number_of_edges()}")
        print("Nodes in the graph:", self.nx.nodes())
        print("Edges in the graph:", self.nx.edges())    

    def get_parents(self, node: IssueOutgoingDto) -> list[IssueOutgoingDto]:
        return list(self.nx.predecessors(node))        

    def parent(self, node: IssueOutgoingDto) -> IssueOutgoingDto | None:
        parents = self.get_parents(node)
        return parents[0] if len(parents) > 0 else None
    
    async def get_children(self, node: IssueOutgoingDto) -> list[IssueOutgoingDto]:
        return list(self.nx.successors(node))
    

    

    def tree_to_dict(self, tree, root):
        children = list(tree.neighbors(root))
        return {
            'node': root.get_dict(),  # Use the to_dict method of IssueOutgoingDto
            'children': [self.tree_to_dict(tree, child) for child in children]
        }
    
    async def to_json_stream2(self) -> dict:
        if self.root is None:
            raise RootNodeNotFound

        edges_name = nx.get_edge_attributes(self.nx, 'name')
        
        print("Edges_name", edges_name)
        tree_structure = self.tree_to_dict(self.nx, self.root)
        print("tree_structure", tree_structure)
        json_tree = json.dumps(tree_structure)
        print(json_tree)
        #print('edges_name', edges_name)



    def to_json_stream(self) -> dict:
        def propagate_branch_name(self, node, names):
            #print("node", node.name, node.type)
            predecessor = self.parent(node)
            if not predecessor:
                return ""
            #print("predecessor", predecessor.name, predecessor.type)
            n = names[(predecessor, node)]
            return n if isinstance(n, str) else "-".join(n)
        
        if self.root is None:
            raise RootNodeNotFound

        edges_name = nx.get_edge_attributes(self.nx, 'name')
        #print(self.root)
        tg = nx.readwrite.json_graph.tree_data(self.nx, self.root)
        
        json_object = json.dumps(
            tg,
            default=lambda o: {
                **o.get_dict(),
                **{"branch_name": propagate_branch_name(self, o, edges_name)},
            },
            indent=2,
        )
        return json_object
