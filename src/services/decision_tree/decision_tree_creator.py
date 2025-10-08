from __future__ import annotations

import logging
import uuid
import copy
import networkx as nx
from typing import Optional, Dict, Any, Union, List, Tuple, Iterator
from fastapi import HTTPException
from src.constants import Type
from src.dtos.issue_dtos import IssueOutgoingDto
from src.dtos.edge_dtos import EdgeOutgoingDto
from src.dtos.decision_tree_dtos import EdgeUUIDDto, EndPointNodeDto, DecisionTreeDTO

logger = logging.getLogger(__name__)


class DecisionTreeGraph():
    """Decision tree class"""
    def __init__(self, root: Optional[Any] = None, **kwargs: Dict[str, Any]) -> None:
        self.nx: nx.DiGraph = nx.DiGraph(**kwargs) # type: ignore
        self.root: Optional[Any] = root
        if self.root is not None:
            self.nx.add_node(self.root)         # type: ignore

    async def add_node(self, node: uuid.UUID) -> None:
        self.nx.add_node(node) # type: ignore

    async def add_edge(self, edge: EdgeUUIDDto) -> None:
        self.nx.add_edge(edge.tail, edge.head) # type: ignore


class DecisionTreeCreator():
    def __init__(self) -> None:
        self.nx = nx.DiGraph() # type: ignore
        self.scenario_id : uuid.UUID
        self.data :  Dict[str, List[Union[uuid.UUID, EdgeUUIDDto]]] = {}
        self.node_ids: list[uuid.UUID] = []
        self.edge_dtos: list[EdgeUUIDDto] = []
        self.node_lookup : Dict[str, IssueOutgoingDto] = {}
        self.endpoint_lookup : Dict[str, EndPointNodeDto] = {}

    @classmethod
    async def initialize(cls, scenario_id:uuid.UUID, nodes:list[IssueOutgoingDto], edges:list[EdgeOutgoingDto]) -> DecisionTreeCreator:
        instance = cls()
        instance.scenario_id = scenario_id
        instance.node_ids, instance.edge_dtos = await instance.create_data_struct(nodes, edges)
        instance.node_lookup = await instance.populate_node_lookup(nodes)
        await instance.data_to_networkx(instance.node_ids, instance.edge_dtos)
        return instance

    async def populate_node_lookup(self, nodes: list[IssueOutgoingDto]) -> Dict[str, IssueOutgoingDto]:
        return {str(node.id): node for node in nodes}

    async def create_decision_tree(self) -> DecisionTreeGraph:
        return await self.convert_to_decision_tree(scenario_id=self.scenario_id)

    async def create_data_struct(self, nodes:list[IssueOutgoingDto], edges:list[EdgeOutgoingDto]) -> Tuple[List[uuid.UUID], List[EdgeUUIDDto]]:
        node_ids = [node.id for node in nodes]
        edge_dtos = [await self.to_arc_dto(nodes, edge) for edge in edges]
        return node_ids, edge_dtos

    async def to_arc_dto(self, nodes: list[IssueOutgoingDto], edge: EdgeOutgoingDto) -> EdgeUUIDDto:
        tail_node = [x for x in nodes if x.id==edge.tail_node.issue_id][0]
        head_node = [x for x in nodes if x.id==edge.head_node.issue_id][0]
        return EdgeUUIDDto(tail=tail_node.id, head=head_node.id)

    async def data_to_networkx(self, node_ids: List[uuid.UUID], edge_dtos: List[EdgeUUIDDto]) -> None:
        for node_id in node_ids:
            await self.add_node(node_id)
        for edge_dto in edge_dtos:
            await self.add_edge(edge_dto)

    async def add_node(self, node: uuid.UUID) -> None:
        try:
            self.nx.add_node(node) # type: ignore
        except Exception as e:
            print("Exception Add_node",str(e))
            raise HTTPException(status_code=500, detail=str(e))    

    async def add_edge(self, edge: EdgeUUIDDto) -> None:
        self.nx.add_edge(edge.tail, edge.head) # type: ignore

    async def copy(self) -> DecisionTreeCreator:
        new_id = type(self)()  # Need to instance from the concrete class
        new_id.nx = self.nx.copy() # type: ignore
        new_id.scenario_id = copy.deepcopy(self.scenario_id)
        new_id.node_lookup = copy.deepcopy(self.node_lookup)
        return new_id

    async def get_parents(self, node: uuid.UUID) -> list[uuid.UUID]:
        return list(self.nx.predecessors(node)) # type: ignore

    async def get_children(self, node: uuid.UUID) -> list[uuid.UUID]:
        return list(self.nx.successors(node)) # type: ignore

    async def get_endpoint_node_from_uuid(self, uuid: uuid.UUID) -> Optional[EndPointNodeDto]:
        return self.endpoint_lookup.get(str(uuid), None)

    async def get_node_from_uuid(self, uuid: uuid.UUID) -> Optional[IssueOutgoingDto]:
        return self.node_lookup.get(str(uuid), None)    

    async def get_type_from_id(self, id: uuid.UUID) -> str:
        node = await self.get_node_from_uuid(id)
        if node is None:
            node = await self.get_endpoint_node_from_uuid(id)
        return node.type if node is not None else "Undefined"

    async def get_nodes_from_type(self, node_type_string: str) -> list[uuid.UUID]:
        node_list :list[uuid.UUID] = []
        for node in list(self.nx.nodes(data=True)): # type: ignore
            node_id = node[0] # type: ignore
            if (await self.get_type_from_id(node_id) == node_type_string): # type: ignore
                node_list.append(node_id) # type: ignore
        return node_list

    async def has_children(self, node: uuid.UUID) -> bool:
        return len(await self.get_children(node)) > 0

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

        decisions : list[uuid.UUID] = []
        decisions_count = await cid_copy.decision_count
        while decisions_count > 0:
            nodes : list[uuid.UUID] = list(cid_copy.nx.nodes())  # type: ignore
            for node in nodes:
                if not await cid_copy.has_children(node):
                    if await self.get_type_from_id(node) == Type.DECISION.value:
                        decisions.append(node)
                        decisions_count -= 1
                    cid_copy.nx.remove_node(node) # type: ignore
        return decisions

    async def calculate_partial_order(self) -> list[uuid.UUID]:
        """Partial order algorithm
        TODO: handle utility nodes
        """

        # get all chance nodes
        uncertainty_nodes = await self.get_uncertainty_nodes()
        elimination_order = await self.decision_elimination_order()
        # TODO: Add utility nodes
        partial_order : list[uuid.UUID] = []

        while elimination_order:
            decision = elimination_order.pop()
            parent_decision_nodes : list[uuid.UUID] = []
            for parent in await self.get_parents(decision):
                if not await self.get_type_from_id(parent) == Type.DECISION.value:
                    if parent in uncertainty_nodes:
                        parent_decision_nodes.append(parent)
                        uncertainty_nodes.remove(parent)

            if len(parent_decision_nodes) > 0:
                partial_order += parent_decision_nodes
            partial_order.append(decision)

        partial_order += uncertainty_nodes

        return partial_order

    async def output_branches_from_node(
        self, node_id: uuid.UUID, node_in_partial_order_id: uuid.UUID, flip: bool=True
        ) -> Iterator[Tuple[EdgeUUIDDto, uuid.UUID]]:
        tree_stack = []
        node = await self.get_node_from_uuid(node_id)
        if node is not None:
            if node.type == Type.DECISION:
                tree_stack = [
                    EdgeUUIDDto(tail=node_id, head=None) for _ in node.decision.options
                ] if node.decision else []
            elif node.type == Type.UNCERTAINTY:
                # This needs to be re-written according to the way we deal with probabilities
                tree_stack = [EdgeUUIDDto(tail=node_id, head=None) for _ in node.uncertainty.outcomes] if node.uncertainty else []
            if flip:
                tree_stack.reverse()

        return zip(tree_stack, [node_in_partial_order_id] * len(tree_stack), strict=False)

    async def convert_to_decision_tree(self, scenario_id:uuid.UUID) -> DecisionTreeGraph:
        #TODO: Update ID2DT according to way we deal with probabilities
        partial_order = await self.calculate_partial_order()
        root_node = partial_order[0]
        decision_tree = DecisionTreeGraph(root=root_node)
        # tree_stack contains views of the partial order nodes
        # decision_tree contains copy of the nodes (as they appear several times)
        tree_stack = [(root_node, root_node)]

        while tree_stack:
            element = tree_stack.pop()

            if isinstance(element[0], uuid.UUID): # type: ignore
                tree_stack += await self.output_branches_from_node(*element) # type: ignore

            else:  # element is a branch
                endpoint_start_index = partial_order.index(element[1])

                if endpoint_start_index < len(partial_order) - 1:
                    endpoint_end = await self.copy_node(partial_order[endpoint_start_index + 1])
                    tree_stack.append(
                        (endpoint_end, partial_order[endpoint_start_index + 1])
                    )
                else:
                    endpoint_end = await self.create_endpoint_node(scenario_id=scenario_id)

                element[0].head = endpoint_end
                await decision_tree.add_edge(
                    element[0]
                )  # node is added when the branch is added

        return decision_tree

    async def to_issue_dtos(self, tree: DecisionTreeGraph) -> Optional[DecisionTreeDTO]:
        tg = nx.readwrite.json_graph.tree_data(tree.nx, tree.root) # type: ignore
        tree_structure = await self.create_issues_dtos_from_tree(tg) # type: ignore
        return tree_structure

    async def get_tree_node_issue_dto(self, issue: IssueOutgoingDto | EndPointNodeDto, children: list[DecisionTreeDTO] | None = None) -> DecisionTreeDTO:
        return DecisionTreeDTO(
            id=issue,
            children=children
        )

    async def create_issues_dtos_from_tree(self, tree_data: Dict[str, Any]) -> Optional[DecisionTreeDTO]:
        # Base case: if the tree data is empty, return None
        if not tree_data:
            return None

        # Create the DTO for the current node
        node_id = await self.get_node_from_uuid(tree_data['id'])
        if node_id is None:
            node_id = await self.get_endpoint_node_from_uuid(tree_data['id'])

        if node_id is None:
            return None

        # Recursively create DTOs for child nodes
        children_dtos: list[DecisionTreeDTO] = []
        for child in tree_data.get('children', []):
            child_dto = await self.create_issues_dtos_from_tree(child)
            if child_dto:
                children_dtos.append(child_dto)
        return await self.get_tree_node_issue_dto(issue=node_id, children=children_dtos if children_dtos else None)

    async def copy_node(self, node_id: uuid.UUID) -> uuid.UUID:
        # create a copy of the node, return id of the copy
        node = self.node_lookup[node_id.__str__()]
        copy_node = copy.deepcopy(node)
        copy_node.id = uuid.uuid4()
        self.node_lookup[copy_node.id.__str__()]=copy_node
        return copy_node.id

    async def create_endpoint_node(self, scenario_id: uuid.UUID) -> uuid.UUID:
        # create endpoint node which is added to endpoint_lookup table, return id of the node
        node = EndPointNodeDto(scenario_id=scenario_id)
        self.endpoint_lookup[node.id.__str__()]=node
        return node.id
