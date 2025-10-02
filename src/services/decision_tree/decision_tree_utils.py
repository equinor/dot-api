from __future__ import annotations

from typing import Optional, Dict, Any
from src.constants import Type, Boundary
from src.dtos.issue_dtos import IssueOutgoingDto
from src.dtos.utility_dtos import UtilityOutgoingDto
from src.dtos.node_dtos import NodeViaIssueOutgoingDto
from src.dtos.node_style_dtos import NodeStyleOutgoingDto
from src.dtos.option_dtos import OptionOutgoingDto
from src.dtos.decision_dtos import DecisionOutgoingDto
from src.dtos.outcome_dtos import OutcomeOutgoingDto
from src.dtos.uncertainty_dtos import UncertaintyOutgoingDto
from src.dtos.value_metric_dtos import ValueMetricOutgoingDto
import uuid

class DecisionTreeUtils:
    @staticmethod
    def _initialize_issue(scenario_id, name):
        issue_id, node_id, node_style_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4() 
        nodeStyleDto = NodeStyleOutgoingDto(id=node_style_id, node_id=node_id)
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
                type=Type.UNASSIGNED,
                boundary=Boundary.IN,
                node=nodeOutgoingDto,
                uncertainty=None,
                decision=None,
                utility=None,
                value_metric=None)

    @staticmethod
    def _create_dto(dto_class, **kwargs):
        return dto_class(id=uuid.uuid4(), **kwargs)
    
    @staticmethod
    def create_issue(issue_type: str, scenario_id: uuid.UUID, name: str, data: Optional[Dict[str, Any]] = None):
        issue = DecisionTreeUtils._initialize_issue(scenario_id, name)
        
        if issue_type == Type.UTILITY.value:
            utility_dict = data or {"Utility": [0]}
            key, value = next(iter(utility_dict.items()))
            issue.utility = DecisionTreeUtils._create_dto(UtilityOutgoingDto, issue_id=issue.id, values=value, name=key)
        
        elif issue_type == Type.DECISION.value:
            options_dict = data or {"option 1": 1, "option 2": 2, "option 3": 3}
            option_dtos = [DecisionTreeUtils._create_dto(OptionOutgoingDto, name=key, decision_id=issue.id, utility=value) for key, value in options_dict.items()]
            issue.decision = DecisionTreeUtils._create_dto(DecisionOutgoingDto, issue_id=issue.id, options=option_dtos)
        
        elif issue_type == Type.UNCERTAINTY.value:
            outcomes_dict = data or {
                "outcome 1": {"probability": 0.3, "utility": 150},
                "outcome 2": {"probability": 0.5, "utility": 200},
                "outcome 3": {"probability": 0.2, "utility": 80}
            }
            outcome_dtos = [DecisionTreeUtils._create_dto(OutcomeOutgoingDto, uncertainty_id=issue.id, name=key, **value) for key, value in outcomes_dict.items()]
            issue.uncertainty = DecisionTreeUtils._create_dto(UncertaintyOutgoingDto, issue_id=issue.id, outcomes=outcome_dtos)
        
        elif issue_type == Type.VALUE_METRIC.value:
            issue.value_metric = DecisionTreeUtils._create_dto(ValueMetricOutgoingDto, issue_id=issue.id, name=name or "Value metric")
        
        else:
            raise ValueError(f"Unknown issue type: {issue_type}")

        issue.type = issue_type
        return issue

class EdgeUUIDDto:
    def __init__(self, tail: uuid.UUID, head: uuid.UUID, name: str):
        self.tail = tail
        self.head = head
        self.name = name

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self, value: uuid.UUID):
        self._tail = value

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self, value: uuid.UUID):
        self._head = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value




    
