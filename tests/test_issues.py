import pytest
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.issue_dtos import IssueIncomingDto, IssueOutgoingDto
from src.dtos.decision_dtos import DecisionIncomingDto
from src.dtos.uncertainty_dtos import UncertaintyIncomingDto
from src.dtos.node_dtos import NodeIncomingDto


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
async def test_update_issue(client: AsyncClient):
    issue_id=3
    example_issue=parse_response_to_dto_test(await client.get(f"/issues/{issue_id}"), IssueOutgoingDto)
    if example_issue.decision is None or example_issue.uncertainty is None:
        raise Exception("example_issue.decision should not be None")
    node=NodeIncomingDto(scenario_id=example_issue.scenario_id, id=example_issue.node.id, issue_id=example_issue.id)

    new_options=["yes", "no", "this is testing issue update"]
    new_probabilities=[0.1, 0.3, 0.6]
    new_type="Uncertainty"
    new_boundary="in"
    payload=[IssueIncomingDto(
        id=example_issue.id, 
        scenario_id=example_issue.scenario_id, 
        type=new_type,
        boundary=new_boundary,
        node=node,
        decision=DecisionIncomingDto(id=example_issue.decision.id, issue_id=example_issue.id, options=new_options),
        uncertainty=UncertaintyIncomingDto(id=example_issue.uncertainty.id, issue_id=example_issue.id, probabilities=new_probabilities)
    ).model_dump()]

    response=await client.put("/issues", json=payload)
    assert response.status_code == 200

    response_content=parse_response_to_dtos_test(response, IssueOutgoingDto)
    assert response_content[0].uncertainty is not None and response_content[0].uncertainty.probabilities==new_probabilities
    assert response_content[0].decision is not None and response_content[0].decision.options==new_options
    assert response_content[0].type==new_type

@pytest.mark.asyncio
async def test_delete_issue(client: AsyncClient):

    response=await client.delete("/issues/3")

    assert response.status_code == 200