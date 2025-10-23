import pyagrum as gum
import numpy as np
from numpy.typing import NDArray
from itertools import product
from uuid import UUID
from pydantic import BaseModel
from src.constants import Type
from utils.discrete_probability_array_manager import DiscreteProbabilityArrayManager
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

    def build_influance_diagram(self, issues: list[IssueOutgoingDto], edges: list[EdgeOutgoingDto]):
        self.add_nodes(issues)
        self.add_edges(edges)
        self.fill_cpts(issues)
        self.add_utilities(issues)

    def find_optimal_decisions(self, issues: list[IssueOutgoingDto], edges: list[EdgeOutgoingDto]):
        self.build_influance_diagram(issues, edges)

        ie = gum.ShaferShenoyLIMIDInference(self.diagram)

        decision_issue_ids = [x.id.__str__() for x in issues if x.type == Type.DECISION]
        if len(decision_issue_ids) > 1:
            ie.addNoForgettingAssumption(decision_issue_ids)

        if not ie.isSolvable():
            raise RuntimeError("Influence diagram is not solvable")

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
                    sorted([option.id.__str__() for option in issue.decision.options]),
                )
            )
            self.add_to_lookup(issue, node_id)

        if issue.type == Type.UNCERTAINTY:
            assert issue.uncertainty is not None
            node_id = self.diagram.addChanceNode(
                gum.LabelizedVariable(
                    issue.id.__str__(),
                    issue.description,
                    sorted([outcome.id.__str__() for outcome in issue.uncertainty.outcomes]),
                )
            )
            self.add_to_lookup(issue, node_id)

    def add_edge(self, edge: EdgeOutgoingDto):
        tail_id = self.node_lookup[edge.tail_node.issue_id]
        head_id = self.node_lookup[edge.head_node.issue_id]

        self.diagram.addArc(tail_id, head_id)

    def fill_cpts(self, issues: list[IssueOutgoingDto]):
        [self.fill_cpt(x) for x in issues]

    def fill_cpt(self, issue: IssueOutgoingDto):
        if issue.type != Type.UNCERTAINTY:
            return
        assert issue.uncertainty is not None

        node_id = self.node_lookup[issue.id]
        parent_ids = self.diagram.parents(node_id)
        parent_labels = [self.diagram.variable(pid).labels() for pid in parent_ids]

        # Build all parent state combinations
        parent_combinations = list(product(*parent_labels))

        x_array_handler = DiscreteProbabilityArrayManager(issue.uncertainty.discrete_probabilities)

        cpt = self.diagram.cpt(node_id)
        if len(parent_ids) == 0:
            probabilities = x_array_handler.get_probabilities_for_combination([])
            probabilities = self._probability_scaling(probabilities)
            cpt[:] = probabilities
            return cpt
        
        for parent_state in parent_combinations:
            probabilities = x_array_handler.get_probabilities_for_combination(parent_state)
            probabilities = self._probability_scaling(probabilities)
            assign = {self.diagram.variable(parent_id).name(): outcome_id for parent_id, outcome_id in zip(parent_ids, parent_state)}
            cpt[assign] = probabilities
        return cpt
    
    def _probability_scaling(self, probabilities: list[float]):
        total = sum(probabilities)
        if total > 0:
            probabilities = [p / total for p in probabilities]
        else:
            probabilities = [1.0 / len(probabilities)] * len(probabilities)
        return probabilities

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
