
from __future__ import annotations

from typing import TYPE_CHECKING
from src.constants import Type, Boundary
from src.dtos.issue_dtos import IssueOutgoingDto
from src.dtos.edge_dtos import EdgeOutgoingDto
from src.dtos.utility_dtos import UtilityOutgoingDto

from src.dtos.node_dtos import NodeViaIssueOutgoingDto
from src.dtos.node_style_dtos import NodeStyleOutgoingDto
from src.dtos.option_dtos import OptionOutgoingDto
from src.dtos.decision_dtos import DecisionOutgoingDto
from src.dtos.outcome_dtos import OutcomeOutgoingDto
from src.dtos.uncertainty_dtos import UncertaintyOutgoingDto
from src.dtos.value_metric_dtos import ValueMetricOutgoingDto

import uuid


class Utils:
    @staticmethod
    def _initialize_issue(scenario_id, name):
        issue_id = uuid.uuid4()
        node_id = uuid.uuid4()
        node_style_id = uuid.uuid4()
        nodeStyleDto = NodeStyleOutgoingDto(id=node_style_id,
                                            node_id=node_id)

        nodeOutgoingDto = NodeViaIssueOutgoingDto(id=node_id,
                                scenario_id=scenario_id,
                                issue_id=issue_id,
                                name="",
                                head_edges=[],
                                tail_edges=[],
                                node_style=nodeStyleDto
                                )
        
        return IssueOutgoingDto(
                id=issue_id,
                scenario_id=scenario_id,
                name=name,
                order=0,
                type=Type.UNDECIDED,
                boundary=Boundary.IN,
                node=nodeOutgoingDto,
                uncertainty=None,
                decision=None,
                utility=None,
                value_metric=None)


    @staticmethod
    def create_utility_issue(scenario_id: uuid.UUID, name: str, utility_dict=None):
        issue = Utils._initialize_issue(scenario_id, name)

        if utility_dict == None:
            utility_dict = {"Utility": [2, 5, 12]}

        key, value = next(iter(utility_dict.items()))
        utility_outgoing_dto = UtilityOutgoingDto(
            id=uuid.uuid4(),
            issue_id=issue.id,
            values=value,
            name=key
        )
        issue.type = Type.UTILITY
        issue.utility=utility_outgoing_dto
        return issue
    


    @staticmethod
    def _create_option_dtos(decision_id, options_dict):
        option_dtos = []
        for key, value in options_dict.items():
            option_dto = OptionOutgoingDto(
                id = uuid.uuid4(),
                name = key,
                decision_id = decision_id,
                utility = value
            )
            option_dtos.append(option_dto)
        return option_dtos    
 
    @staticmethod
    def create_decision_issue(scenario_id: uuid.UUID, name: str, options_dict=None):
        issue = Utils._initialize_issue(scenario_id, name)
        decision_id = uuid.uuid4()

        if options_dict is None:
            options_dict = {"option 1": 1,
                            "option 2": 2,
                            "option 3": 3}
            
        option_dtos = Utils._create_option_dtos(decision_id, options_dict)
        decision_outgoing_dto = DecisionOutgoingDto(
            id=decision_id,
            issue_id=issue.id,
            options=option_dtos
        )
        issue.type = Type.DECISION
        issue.decision=decision_outgoing_dto
        return issue
    

    @staticmethod
    def _create_outcome_dtos(uncertainty_id, outcomes_dict):
        option_dtos = []
        for key, value in outcomes_dict.items():
            outcome_dto = OutcomeOutgoingDto(
                id = uuid.uuid4(),
                name=key,
                uncertainty_id=uncertainty_id,
                probability=value['probability'],
                utility=value['utility']
            )
            option_dtos.append(outcome_dto)
        return option_dtos
    
    @staticmethod
    def create_uncertainty_issue(scenario_id: uuid.UUID, name: str, outcomes_dict=None):
        issue = Utils._initialize_issue(scenario_id, name)
        uncertainty_id = uuid.uuid4()

        if outcomes_dict is None:
            outcomes_dict = {"outcome 1": { "probability":0.3, "utility":150 },
                             "outcome 2": { "probability":0.5, "utility":200 },
                             "outcome 3": { "probability":0.2, "utility":80 }}
            
        outcome_dtos = Utils._create_outcome_dtos(uncertainty_id, outcomes_dict)
        uncertainty_outgoing_dto = UncertaintyOutgoingDto(
            id=uncertainty_id, 
            issue_id=issue.id,
            outcomes=outcome_dtos
        )
        issue.type = Type.UNCERTAINTY
        issue.uncertainty=uncertainty_outgoing_dto
        return issue

    @staticmethod
    def create_value_metric_issue(scenario_id: uuid.UUID, name=None):
        issue = Utils._initialize_issue(scenario_id, name)

        if name is None:
            name = "Value metric"

        value_metric_dto = ValueMetricOutgoingDto(
                id=uuid.uuid4(),
                issue_id=issue.id,
                name=name
            )
        issue.type = Type.VALUE_METRIC
        issue.value_metric=value_metric_dto
        return issue



class EdgeDTDto:
    def __init__(self, tail: IssueOutgoingDto, head: IssueOutgoingDto, name: str):
        self.tail = tail
        self.head = head
        self.name = name

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, value: IssueOutgoingDto):
        self._tail = value

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, value: IssueOutgoingDto):
        self._head = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value