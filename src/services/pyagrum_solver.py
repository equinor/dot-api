import pyagrum as gum
import numpy as np
from numpy.typing import NDArray
from itertools import product
from uuid import UUID
from src.constants import Type
from src.dtos.issue_dtos import IssueOutgoingDto, IssueViaNodeOutgoingDto
from src.dtos.edge_dtos import EdgeOutgoingDto
from src.dtos.option_dtos import OptionOutgoingDto
from src.dtos.model_solution_dtos import SolutionDto


class PyagrumSolver:
    def __init__(self):
        self.node_lookup: dict[UUID, int] = {}
        self.diagram = gum.InfluenceDiagram()

    def _reset_diagram(self):
        self.diagram = gum.InfluenceDiagram()

    def add_to_lookup(self, issue: IssueOutgoingDto, node_id: int) -> None:
        self.node_lookup[issue.id] = node_id

    def find_optimal_decisions(self, issues: list[IssueOutgoingDto], edges: list[EdgeOutgoingDto]):
        self.add_nodes(issues)
        self.add_edges(edges)
        self.add_utilities(issues)

        ie = gum.ShaferShenoyLIMIDInference(self.diagram)
        if not ie.isSolvable():
            raise RuntimeError("Influence diagram is not solvable")

        decision_issue_ids = [x.id.__str__() for x in issues if x.type == Type.DECISION]
        ie.addNoForgettingAssumption(decision_issue_ids)

        ie.makeInference()

        if len(decision_issue_ids) == 0:
            return SolutionDto(
                utility_mean=ie.MEU()["mean"],
                utility_variance=ie.MEU()["variance"],
                optimal_options=[],
            )

        data: list[NDArray[np.float64]] = [
            ie.optimalDecision(x).toarray() for x in decision_issue_ids
        ]

        optimal_options: list[OptionOutgoingDto] = []
        for array, decision_issue_id in zip(data, decision_issue_ids):
            issue: IssueOutgoingDto = [x for x in issues if x.id.__str__() == decision_issue_id][0]
            optimal_options.append(issue.decision.options[array.argmax()])

        solution = SolutionDto(
            utility_mean=ie.MEU()["mean"],
            utility_variance=ie.MEU()["variance"],
            optimal_options=optimal_options,
        )

        return solution

    def add_node(self, issue: IssueOutgoingDto):
        if issue.type == Type.DECISION:
            assert issue.decision is not None
            node_id = self.diagram.addDecisionNode(
                gum.LabelizedVariable(
                    issue.id.__str__(),
                    issue.description,
                    [option.id.__str__() for option in issue.decision.options],
                )
            )
            self.add_to_lookup(issue, node_id)

        if issue.type == Type.UNCERTAINTY:
            assert issue.uncertainty is not None
            node_id = self.diagram.addChanceNode(
                gum.LabelizedVariable(
                    issue.id.__str__(),
                    issue.description,
                    [outcome.id.__str__() for outcome in issue.uncertainty.outcomes],
                )
            )
            self.add_to_lookup(issue, node_id)

    def add_edge(self, edge: EdgeOutgoingDto):
        tail_id = self.node_lookup[edge.tail_node.issue_id]
        head_id = self.node_lookup[edge.head_node.issue_id]

        self.diagram.addArc(tail_id, head_id)

        self.fill_cpt(edge.head_node.issue)

    def fill_cpt(self, head_issue: IssueViaNodeOutgoingDto):
        if head_issue.type != Type.UNCERTAINTY:
            return
        assert head_issue.uncertainty is not None

        node_id = self.node_lookup[head_issue.id]

        # Get parent nodes
        parent_ids: list[int] = self.diagram.parents(node_id)
        parent_states = [self.diagram.variable(parent_id).labels() for parent_id in parent_ids]

        # Generate all combinations of parent states
        parent_combinations = list(product(*parent_states))

        # Fill the CPT for each combination of parent states
        cpt = self.diagram.cpt(node_id)
        for i, combination in enumerate(parent_combinations):
            cpt[dict(zip(parent_ids, combination))] = head_issue.uncertainty.outcomes[
                i % len(head_issue.uncertainty.outcomes)
            ].probability

    def add_utility(self, issue: IssueOutgoingDto):
        node_id = self.diagram.addUtilityNode(
            gum.LabelizedVariable(
                f"{issue.id.__str__()} utility",
                f"{issue.id.__str__()} utility",
                1,
            )
        )
        self.diagram.addArc(self.diagram.idFromName(issue.id.__str__()), node_id)

        if issue.type == Type.DECISION:
            assert issue.decision is not None

            for n, x in enumerate(issue.decision.options):
                self.diagram.utility(node_id)[{issue.id.__str__(): n}] = x.utility

        if issue.type == Type.UNCERTAINTY:
            assert issue.uncertainty is not None

            for n, x in enumerate(issue.uncertainty.outcomes):
                self.diagram.utility(node_id)[{issue.id.__str__(): n}] = x.utility

    def add_edges(self, edges: list[EdgeOutgoingDto]):
        [self.add_edge(x) for x in edges]

    def add_nodes(self, issues: list[IssueOutgoingDto]):
        [self.add_node(x) for x in issues]

    def add_utilities(self, issues: list[IssueOutgoingDto]):
        [self.add_utility(x) for x in issues]
