from __future__ import annotations

import logging
from pathlib import Path
from src.constants import Type
from typing import Optional, Dict, Any
import networkx as nx
from fastapi import HTTPException
from src.dtos.issue_dtos import IssueOutgoingDto
from src.dtos.edge_dtos import EdgeOutgoingDto
from src.services.decision_tree.decision_tree_utils import EdgeUUIDDto
from src.services.decision_tree.decision_tree_utils import DecisionTreeUtils
import uuid
import copy

logger = logging.getLogger(__name__)

class PartialOrderOutputModeError(Exception):
    def __init__(self, mode):
        self.mode = mode
        error_message = (
            f"output mode should be [view|copy] and have been entered as {mode}"
        )
        super().__init__(error_message)
        logger.critical(error_message)

class DecisionTreeGraph():
    """Decision tree class"""

    def __init__(self, *args, **kwargs):
        self.nx = nx.DiGraph(*args, **kwargs)
        self.root = kwargs.get("root", None)
        if self.root is not None:
            self.nx.add_node(self.root)

    async def add_node(self, node: uuid.UUID):
        self.nx.add_node(node)
    
    async def add_edge(self, edge: EdgeUUIDDto):
        attr = {'name': edge.name}
        self.nx.add_edge(edge.tail, edge.head, **attr)

class DecisionTreeCreator():
    def __init__(self, *args, **kwargs):
        self.nx = nx.DiGraph(*args, **kwargs)
        self.scenario_id = None
        self.data = {}
        self.node_lookup = {}

    @classmethod
    async def initialize(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        nodes = kwargs.get("issues", [])
        edges = kwargs.get("edges", [])
        instance.scenario_id = kwargs.get("scenario_id", None)
        instance.data = await instance.create_data_struct(nodes, edges)
        instance.node_lookup = await instance.populate_node_lookup(nodes)
        await instance.data_to_networkx(instance.data)
        return instance    

    async def populate_node_lookup(self, nodes):
        return {str(node.id): node for node in nodes}

    async def create_decision_tree(self):
        dt = await self.convert_to_decision_tree(scenario_id=self.scenario_id)
        return dt

    async def create_data_struct(self, nodes:list[IssueOutgoingDto], edges:list[EdgeOutgoingDto]):
        return {
            "nodes": [node.id for node in nodes],
            "edges": [await self.to_arc_dto(nodes, edge) for edge in edges]
        }
    
    async def to_arc_dto(self, nodes: list[IssueOutgoingDto], edge: EdgeOutgoingDto):
        tail_node = [x for x in nodes if x.id==edge.tail_node.issue_id][0]
        head_node = [x for x in nodes if x.id==edge.head_node.issue_id][0]
        return EdgeUUIDDto(tail_node.id, head_node.id, '')
    
    async def data_to_networkx(self, data: dict):
        for node in data["nodes"]:
            await self.add_node(node)
        for edge in data.get("edges", []): {
            await self.add_edge(edge)
        }        

    async def add_node(self, node: uuid.UUID):
        try:
            self.nx.add_node(node)
        except Exception as e:
            print("Exception Add_node",str(e))
            raise HTTPException(status_code=500, detail=str(e))    

    async def add_edge(self, edge: EdgeUUIDDto):
        attr = {'name': edge.name}
        self.nx.add_edge(edge.tail, edge.head, **attr)

    async def copy(self):
        new_id = type(self)()  # Need to instance from the concrete class
        new_id.nx = self.nx.copy()
        new_id.scenario_id = copy.deepcopy(self.scenario_id)
        new_id.node_lookup = copy.deepcopy(self.node_lookup)
        return new_id

    async def get_parents(self, node: uuid.UUID) -> list[uuid.UUID]:
        return list(self.nx.predecessors(node))

    async def get_children(self, node: uuid.UUID) -> list[uuid.UUID]:
        return list(self.nx.successors(node))
 
    async def get_node_from_uuid(self, uuid: uuid.UUID) -> IssueOutgoingDto:
        id = uuid.__str__()
        issue = self.node_lookup[id]
        return issue

    async def get_type_from_id(self, id: uuid.UUID) -> str:
        node = await self.get_node_from_uuid(id)
        return node.type

    async def get_nodes_from_type(self, node_type_string: str) -> list[uuid.UUID]:
        node_list = []
        for node in list(self.nx.nodes(data=True)):
            if (await self.get_type_from_id(node[0]) == node_type_string):
                node_list.append(node[0])
        return node_list

    async def has_children(self, node: uuid.UUID) -> bool:
        return len(await self.get_children(node)) > 0
    
    async def to_json(self, filepath: Path = None) -> str:
        json_object = self.to_json_stream()
        if filepath:
            with open(filepath, "w") as outfile:
                outfile.write(json_object)
        return json_object
    
    async def get_decision_nodes(self) -> list[uuid.UUID]:
        return await self.get_nodes_from_type(Type.DECISION.value)

    async def get_uncertainty_nodes(self) -> list [uuid.UUID]:
        return await self.get_nodes_from_type(Type.UNCERTAINTY.value)

    async def get_utility_nodes(self) -> list[uuid.UUID]:
        return await self.get_nodes_from_type(Type.UTILITY.value)

    @property
    async def decision_count(self) -> int:
        return len(await self.get_decision_nodes())

    @property
    async def uncertainty_count(self) -> int:
        return len(await self.get_uncertainty_nodes())

    @property
    async def utility_count(self) -> int:
        return len(await self.get_utility_nodes())
    
    async def decision_elimination_order(self) -> list[uuid.UUID]:
        cid_copy = await self.copy()
     
        decisions = []
        decisions_count = await cid_copy.decision_count
        while decisions_count > 0:
            nodes = list(cid_copy.nx.nodes())
            for node in nodes:
                if not await cid_copy.has_children(node):
                    if await self.get_type_from_id(node) == Type.DECISION.value:
                        decisions.append(node)
                        decisions_count -= 1
                    cid_copy.nx.remove_node(node)
        return decisions
    
    async def calculate_partial_order(self, mode="view") -> list[uuid.UUID]:
        """Partial order algorithm
        TODO: handle utility nodes
        """
        if mode not in ["view", "copy"]: #will we use copy mode?
            raise PartialOrderOutputModeError(mode)

        # get all chance nodes
        uncertainty_nodes = await self.get_uncertainty_nodes()
        elimination_order = await self.decision_elimination_order()
        # TODO: Add utility nodes
        partial_order = []

        while elimination_order:
            decision = elimination_order.pop()
            parent_decision_nodes = []
            for parent in await self.get_parents(decision):
                if not await self.get_type_from_id(parent) == Type.DECISION.value:
                    if parent in uncertainty_nodes:
                        parent_decision_nodes.append(parent)
                        uncertainty_nodes.remove(parent)

            if len(parent_decision_nodes) > 0:
                partial_order += parent_decision_nodes
            partial_order.append(decision)

        partial_order += uncertainty_nodes

        if mode == "copy":
            partial_order = [node.copy() for node in partial_order]

        return partial_order
    

    async def output_branches_from_node(
        self, node_id: uuid.UUID, node_in_partial_order_id: uuid.UUID, flip=True
        ) -> list[tuple[EdgeUUIDDto, uuid.UUID]]:
        node = await self.get_node_from_uuid(node_id) 
        if node.type == Type.UTILITY:
            tree_stack = [EdgeUUIDDto(node_id, None, name='utility') for utility in node.utility]
        if node.type == Type.DECISION:
            tree_stack = [
                EdgeUUIDDto(node_id, None, name=option.name) for option in node.decision.options
            ]
        if node.type == Type.UNCERTAINTY:
            # This needs to be re-written according to the way we deal with probabilities
            tree_stack = [EdgeUUIDDto(node_id, None, name=outcome.name) for outcome in node.uncertainty.outcomes]
        if flip:
            tree_stack.reverse()

        return zip(tree_stack, [node_in_partial_order_id] * len(tree_stack), strict=False)
    

    async def convert_to_decision_tree(self, scenario_id:uuid.UUID):
        #TODO: Update ID2DT according to way we deal with probabilities
        partial_order = await self.calculate_partial_order()
        root_node = partial_order[0]
        decision_tree = DecisionTreeGraph(root=root_node)
        # tree_stack contains views of the partial order nodes
        # decision_tree contains copy of the nodes (as they appear several times)
        tree_stack = [(root_node, root_node)]

        while tree_stack:
            element = tree_stack.pop()

            if isinstance(element[0], uuid.UUID):
                tree_stack += await self.output_branches_from_node(*element)

            else:  # element is a branch
                endpoint_start_index = partial_order.index(element[1])

                if endpoint_start_index < len(partial_order) - 1:
                    endpoint_end = await self.copy_node(partial_order[endpoint_start_index + 1])
                    tree_stack.append(
                        (endpoint_end, partial_order[endpoint_start_index + 1])
                    )
                else:
                    endpoint_end = await self.create_node(issue_type=Type.UTILITY.value, scenario_id=scenario_id, name='')

                element[0].head = endpoint_end
                await decision_tree.add_edge(
                    element[0]
                )  # node is added when the branch is added

        return decision_tree
    
    async def to_json_stream(self, tree: DecisionTreeGraph):
        tg = nx.readwrite.json_graph.tree_data(tree.nx, tree.root)
        id = tg['id']
        tree_structure = await self.create_dtos_from_tree(tg)
        return tree_structure

    async def get_tree_node_dto(self, id, children=None):
        return {
            'id': id.get_dict(),
            **({'children': children} if children is not None else {})
        }
    
    async def create_dtos_from_tree(self, tree_data):
        # Base case: if the tree data is empty, return None
        if not tree_data:
            return None

        # Create the DTO for the current node
        node_id = await self.get_node_from_uuid(tree_data['id'])

        # Recursively create DTOs for child nodes
        children_dtos = []
        for child in tree_data.get('children', []):
            child_dto = await self.create_dtos_from_tree(child)
            if child_dto:
                children_dtos.append(child_dto)
        return await self.get_tree_node_dto(id=node_id, children=children_dtos if children_dtos else None)
    
    async def copy_node(self, node_id):
        node = self.node_lookup[node_id.__str__()]
        copy_node = copy.deepcopy(node)
        copy_node.id = uuid.uuid4()
        self.node_lookup[copy_node.id.__str__()]=copy_node
        return copy_node.id
    
    async def create_node(self, issue_type: str, scenario_id: uuid.UUID, name: str, data: Optional[Dict[str, Any]] = None):
        node = DecisionTreeUtils.create_issue(issue_type=issue_type, scenario_id=scenario_id, name=name, data=data)
        self.node_lookup[node.id.__str__()]=node
        return node.id