"""Module defining the ProbabilisticGraphModel Abstract class"""

from __future__ import annotations

import logging
import json
from pathlib import Path
from typing import TYPE_CHECKING
from src.constants import Type, Boundary
import networkx as nx
from pydantic import BaseModel
from src.dtos.issue_dtos import IssueOutgoingDto
from src.dtos.edge_dtos import EdgeOutgoingDto
from src.dtos.utility_dtos import UtilityOutgoingDto

from src.dtos.node_dtos import NodeViaIssueOutgoingDto
from src.dtos.node_style_dtos import NodeStyleOutgoingDto
from src.services.decision_tree.utils import EdgeDTDto
from src.services.decision_tree.utils import Utils
from src.services.decision_tree.decision_tree import DecisionTree

import uuid

logger = logging.getLogger(__name__)

class PartialOrderOutputModeError(Exception):
    def __init__(self, mode):
        self.mode = mode
        error_message = (
            f"output mode should be [view|copy] and have been entered as {mode}"
        )
        super().__init__(error_message)
        logger.critical(error_message)


class NetworkXWrapper():
    def __init__(self, *args, **kwargs):
        self.nx = nx.DiGraph(*args, **kwargs)
        self.cc = 0

    async def create_decision_tree(self, scenario_id:uuid.UUID, nodes:list[IssueOutgoingDto], edges:list[EdgeOutgoingDto]):
        data =  await self.create_data_struct(nodes, edges)
        #print(data)
        await self.data_to_networkx(data)

        # jj = self.id_to_json_stream()
        # print(jj)
        
        dt = await self.convert_to_decision_tree(scenario_id=scenario_id)
        return dt
        #dt_json = await dt.to_json_stream()
        #print(dt_json)



    def id_to_json_stream(self) -> dict:
        data = nx.node_link_data(self.nx, source="from", target="to", link="edges")
        print("data AA", data)
        for e in data["edges"]:
            print("e: ", e)
        # data["edges"] = [
        #     {k: v if not isinstance(v, IssueOutgoingDto) else v.id for k, v in e.items()}
        #     for e in data["edges"]
        # ]
        #print(data)
        #json_object = json.dumps(data, default=lambda o: o.json(), indent=4)
        return "json" #json_object
    

    async def create_data_struct(self, nodes:list[IssueOutgoingDto], edges:list[EdgeOutgoingDto]):
        arcs = [await self.to_arc_dto(nodes, edge) for edge in edges]
        dict = {"nodes": nodes, "edges": arcs}
        #print(dict)
        return dict
        #return self.from_dict({"nodes": nodes, "edges": arcs})
    
    async def to_arc_dto(self, nodes: list[IssueOutgoingDto], edge: EdgeOutgoingDto):
        tail_node = [x for x in nodes if x.id==edge.tail_id][0]
        head_node = [x for x in nodes if x.id==edge.head_id][0]

        edgedto = EdgeDTDto(tail_node, head_node, edge.name)
        #edgedto = EdgeDTDto(head_node, tail_node, edge.name)
        return edgedto
        #return [tail_node, head_node,""]EdgeDTDto
    
    async def data_to_networkx(self, data: dict):
        #diagram = self.initialize_diagram(data)
        for node in data["nodes"]:
            await self.add_node(node)
        for edge in data.get("edges", []): {
            await self.add_edge(edge)
        }

    async def add_node(self, node: IssueOutgoingDto):
        self.nx.add_node(node)

    async def add_edge(self, edge: EdgeDTDto):
        attr = {'name': edge.name}
        #print("add_edge", edge.tail, edge.head, edge.name)
        self.nx.add_edge(edge.tail, edge.head, **attr) 

    async def copy(self):
        new_id = type(self)()  # Need to instance from the concrete class
        new_id.nx = self.nx.copy()
        return new_id

    async def get_parents(self, node: IssueOutgoingDto) -> list[IssueOutgoingDto]:
        return list(self.nx.predecessors(node))

    async def get_children(self, node: IssueOutgoingDto) -> list[IssueOutgoingDto]:
        return list(self.nx.successors(node))
 
    async def get_nodes_from_type(self, node_type_string: str) -> list[IssueOutgoingDto]:
        node_list = []
        for node in list(self.nx.nodes(data=True)):
            if (node[0].type == node_type_string):
                node_list.append(node[0])
        return node_list

    async def has_children(self, node: IssueOutgoingDto) -> bool:
        return len(await self.get_children(node)) > 0
    
    async def to_json(self, filepath: Path = None) -> str:
        json_object = self.to_json_stream()
        if filepath:
            with open(filepath, "w") as outfile:
                outfile.write(json_object)
        return json_object

    async def get_node_from_uuid(self, uuid: str) -> IssueOutgoingDto:
        return [node for node in self.nx if node.id == uuid][0]

    async def copy(self):
        new_id = type(self)()  # Need to instance from the concrete class
        new_id.nx = self.nx.copy()
        return new_id
    
    async def get_decision_nodes(self) -> list[IssueOutgoingDto]:
        return await self.get_nodes_from_type(Type.DECISION)

    async def get_uncertainty_nodes(self) -> list[IssueOutgoingDto]:
        return await self.get_nodes_from_type(Type.UNCERTAINTY)

    async def get_utility_nodes(self) -> list[IssueOutgoingDto]:
        return await self.get_nodes_from_type(Type.UTILITY)

    @property
    async def decision_count(self) -> int:
        #decision_nodes = await self.get_decision_nodes()
        return len(await self.get_decision_nodes())

    @property
    async def uncertainty_count(self) -> int:
        return len(await self.get_uncertainty_nodes())

    @property
    async def utility_count(self) -> int:
        return len(await self.get_utility_nodes())
    
    async def decision_elimination_order(self) -> list[IssueOutgoingDto]:
        cid_copy = await self.copy()
        decisions = []
        decisions_count = await cid_copy.decision_count
        while decisions_count > 0:
            nodes = list(cid_copy.nx.nodes())
            for node in nodes:
                if not await cid_copy.has_children(node):
                    if node.type == Type.DECISION:
                        decisions.append(node)
                        decisions_count -= 1
                    cid_copy.nx.remove_node(node)
        return decisions
    
    async def calculate_partial_order(self, mode="view") -> list[IssueOutgoingDto]:
        """Partial order algorithm


        Args:
            mode (str): ["view"(default)|"copy"]
                returns a view or a copy of the nodes

        Returns
            List[NodeABC]: list of nodes (copies or vioews) sorted in decision order

        TODO: add description of what the algorithm is about
        TODO: handle utility nodes
        """
        if mode not in ["view", "copy"]:
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
                if not parent.type == Type.DECISION:    
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
        self, node: IssueOutgoingDto, node_in_partial_order: IssueOutgoingDto, flip=True
    ) -> list[tuple[EdgeDTDto, IssueOutgoingDto]]:
        if node.type == Type.UTILITY:
            tree_stack = [EdgeDTDto(node, None, name='utility') for utility in node.utility]
        if node.type == Type.DECISION:
            tree_stack = [
                EdgeDTDto(node, None, name=option.name) for option in node.decision.options
            ]
        if node.type == Type.UNCERTAINTY:
            # This needs to be re-written according to the way we deal with probabilities
            #tree_stack = [EdgeOutgoingDto(node, None, name=outcome) for outcome in node.outcomes]
            #eee = EdgeDTDto(node, None, name='outcome')
            tree_stack = [EdgeDTDto(node, None, name=outcome.name) for outcome in node.uncertainty.outcomes]
        if flip:
            tree_stack.reverse()

        return zip(tree_stack, [node_in_partial_order] * len(tree_stack), strict=False)
    

    async def convert_to_decision_tree(self, scenario_id:uuid.UUID) -> DecisionTree:
        """Convert the influence diagram into a DecisionTree object

        Returns:
            DecisionTree: The symmetric decision tree equivalent to the influence diagram

        TODO: Update ID2DT according to way we deal with probabilities
        """
        partial_order = await self.calculate_partial_order()
        root_node = partial_order[0]
        print("root_node", root_node)
        print("root_node type", root_node.type, root_node.name)
        # decision_tree = DecisionTree.initialize_with_root(root_node)
        decision_tree = DecisionTree(root=root_node)
        # tree_stack contains views of the partial order nodes
        # decision_tree contains copy of the nodes (as they appear several times)
        tree_stack = [(root_node, root_node)]

        while tree_stack:
            element = tree_stack.pop()

            if isinstance(element[0], IssueOutgoingDto):
                tree_stack += await self.output_branches_from_node(*element)

            else:  # element is a branch
                endpoint_start_index = partial_order.index(element[1])

                if endpoint_start_index < len(partial_order) - 1:
                    endpoint_end = partial_order[endpoint_start_index + 1].model_copy()
                    tree_stack.append(
                        (endpoint_end, partial_order[endpoint_start_index + 1])
                    )
                else:
                    nn = 'ut' + str(self.cc)
                    endpoint_end = Utils.create_utility_issue(scenario_id=scenario_id, name=nn)
                    self.cc += 1

                #element[0].tail = endpoint_end
                element[0].head = endpoint_end
                await decision_tree.add_edge(
                    element[0]
                )  # node is added when the branch is added

        await decision_tree.print_all()
        return decision_tree
    