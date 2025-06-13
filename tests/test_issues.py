import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.constants import (
    Type,
    Boundary,
)
from src.dtos.issue_dtos import IssueIncomingDto, IssueOutgoingDto
from src.dtos.decision_dtos import DecisionIncomingDto
from src.dtos.uncertainty_dtos import UncertaintyIncomingDto
from src.dtos.node_dtos import NodeIncomingDto
from src.dtos.node_style_dtos import NodeStyleIncomingDto
from src.dtos.decision_dtos import DecisionIncomingDto


@pytest.mark.asyncio
async def test_get_issues(client: AsyncClient):
    response = await client.get("/issues")
    assert response.status_code == 200

    parse_response_to_dtos_test(response, IssueOutgoingDto)

@pytest.mark.asyncio
async def test_get_issue(client: AsyncClient):
    response = await client.get("/issues/20")
    assert response.status_code == 200

    parse_response_to_dto_test(response, IssueOutgoingDto)

@pytest.mark.asyncio
async def test_create_issue(client: AsyncClient):
    scenario_id=4
    alternatives=["alt1", "alt2"]
    x_position=600
    node=NodeIncomingDto(scenario_id=scenario_id, id=None, issue_id=None, node_style=NodeStyleIncomingDto(x_position=x_position))
    
    payload=[IssueIncomingDto(
        id=None,
        decision=DecisionIncomingDto(id=None, issue_id=None, alternatives=alternatives),
        scenario_id=4,
        type=Type.DECISION,
        boundary=Boundary.OUT,
        order=2,
        node=node,
        uncertainty=None,
        utility=None,
        value_metric=None,
    ).model_dump()]

    response=await client.post("/issues", json=payload)
    assert response.status_code == 200
    response_content=parse_response_to_dtos_test(response, IssueOutgoingDto)

    assert response_content[0].decision is not None and response_content[0].decision.alternatives==alternatives
    assert response_content[0].node is not None and response_content[0].node.node_style is not None and response_content[0].node.node_style.x_position==x_position


@pytest.mark.asyncio
async def test_update_issue(client: AsyncClient):
    issue_id=3
    example_issue=parse_response_to_dto_test(await client.get(f"/issues/{issue_id}"), IssueOutgoingDto)
    if example_issue.decision is None or example_issue.uncertainty is None:
        raise Exception("example_issue.decision should not be None")
    node=NodeIncomingDto(scenario_id=example_issue.scenario_id, id=example_issue.node.id, issue_id=example_issue.id, node_style=None)

    new_options=["yes", "no", "this is testing issue update"]
    new_probabilities=[0.1, 0.3, 0.6]
    new_type=Type.UNCERTAINTY
    new_boundary=Boundary.IN
    payload=[IssueIncomingDto(
        id=example_issue.id, 
        scenario_id=example_issue.scenario_id, 
        type=new_type,
        boundary=new_boundary,
        order=0,
        node=node,
        decision=DecisionIncomingDto(id=example_issue.decision.id, issue_id=example_issue.id, alternatives=new_options),
        uncertainty=UncertaintyIncomingDto(id=example_issue.uncertainty.id, issue_id=example_issue.id, probabilities=new_probabilities),
        utility=None,
        value_metric=None,
    ).model_dump()]

    response=await client.put("/issues", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos_test(response, IssueOutgoingDto)
    assert response_content[0].uncertainty is not None and response_content[0].uncertainty.probabilities==new_probabilities
    assert response_content[0].decision is not None and response_content[0].decision.alternatives==new_options
    assert response_content[0].type==new_type

@pytest.mark.asyncio
async def test_delete_issue(client: AsyncClient):

    response=await client.delete("/issues/3")

    assert response.status_code == 200