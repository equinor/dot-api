import pytest
import uuid
from httpx import AsyncClient
from tests.utils import (
    parse_response_to_dto_test,
    parse_response_to_dtos_test,
)
from src.dtos.discrete_probability_dtos import DiscreteProbabilityIncomingDto, DiscreteProbabilityOutgoingDto
from src.seed_database import GenerateUuid


@pytest.mark.asyncio
async def test_get_discrete_probabilities(client: AsyncClient):
    response = await client.get("/discrete_probabilities")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dtos_test(response, DiscreteProbabilityOutgoingDto)


@pytest.mark.asyncio
async def test_get_discrete_probability(client: AsyncClient):
    # Use the first outcome probability ID from seed data (project_index=0, scenario_index=0, issue_node_index=0)
    first_outcome_prob_id = GenerateUuid.as_string("0_0_0_op1")
    response = await client.get(f"/discrete_probabilities/{first_outcome_prob_id}")
    assert response.status_code == 200, f"Response content: {response.content}"

    parse_response_to_dto_test(response, DiscreteProbabilityOutgoingDto)


@pytest.mark.asyncio
async def test_create_discrete_probability(client: AsyncClient):
    new_discrete_probability_id = uuid.uuid4()
    new_uncertainty_id = GenerateUuid.as_uuid(2)
    new_child_outcome_id = GenerateUuid.as_uuid(2)
    parent_option_id = GenerateUuid.as_uuid(1)
    new_probability = 0.75
    
    payload = [
        DiscreteProbabilityIncomingDto(
            id=new_discrete_probability_id,
            uncertainty_id=new_uncertainty_id,
            child_outcome_id=new_child_outcome_id,
            probability=new_probability,
            parent_option_ids=[parent_option_id],
            parent_outcome_ids=[],
        ).model_dump(mode="json")
    ]

    response = await client.post("/discrete_probabilities", json=payload)
    assert response.status_code == 200, f"Response content: {response.content}"

    response_content = parse_response_to_dtos_test(response, DiscreteProbabilityOutgoingDto)
    assert response_content[0].probability == new_probability
    assert response_content[0].parent_option_ids[0] == parent_option_id
    assert response_content[0].id == new_discrete_probability_id


@pytest.mark.asyncio
async def test_update_discrete_probability(client: AsyncClient):
    # Use an existing outcome probability ID from seed data
    discrete_probability_id = GenerateUuid.as_uuid("0_0_0_op1")
    # Use an existing uncertainty and outcome ID from seed data
    uncertainty_id = GenerateUuid.as_uuid(2)
    child_outcome_id = GenerateUuid.as_uuid(2)
    parent_outcome_id = GenerateUuid.as_uuid(1)
    updated_probability = 0.85
    
    payload = [
        DiscreteProbabilityIncomingDto(
            id=discrete_probability_id,
            uncertainty_id=uncertainty_id,
            child_outcome_id=child_outcome_id,
            probability=updated_probability,
            parent_option_ids=[],
            parent_outcome_ids=[parent_outcome_id],
        ).model_dump(mode="json")
    ]

    response = await client.put("/discrete_probabilities", json=payload)
    assert response.status_code == 200, f"Response content: {response.content}"

    response_content = parse_response_to_dtos_test(response, DiscreteProbabilityOutgoingDto)
    assert response_content[0].probability == updated_probability
    assert response_content[0].parent_outcome_ids[0] == parent_outcome_id


@pytest.mark.asyncio
async def test_delete_discrete_probability(client: AsyncClient):
    # Create a new outcome probability first
    new_discrete_probability_id = uuid.uuid4()
    create_payload = [
        DiscreteProbabilityIncomingDto(
            id=new_discrete_probability_id,
            uncertainty_id=GenerateUuid.as_uuid(1),
            child_outcome_id=GenerateUuid.as_uuid(1),
            probability=0.5,
            parent_option_ids=[],
            parent_outcome_ids=[],
        ).model_dump(mode="json")
    ]
    
    create_response = await client.post("/discrete_probabilities", json=create_payload)
    assert create_response.status_code == 200
    
    # Now delete it
    response = await client.delete(f"/discrete_probabilities/{new_discrete_probability_id}")
    assert response.status_code == 200, f"Response content: {response.content}"


@pytest.mark.asyncio
async def test_delete_discrete_probabilities_bulk(client: AsyncClient):
    # Create two new outcome probabilities first
    id1 = uuid.uuid4()
    id2 = uuid.uuid4()
    
    create_payload = [
        DiscreteProbabilityIncomingDto(
            id=id1,
            uncertainty_id=GenerateUuid.as_uuid(1),
            child_outcome_id=GenerateUuid.as_uuid(1),
            probability=0.3,
            parent_option_ids=[],
            parent_outcome_ids=[],
        ).model_dump(mode="json"),
        DiscreteProbabilityIncomingDto(
            id=id2,
            uncertainty_id=GenerateUuid.as_uuid(1),
            child_outcome_id=GenerateUuid.as_uuid(2),
            probability=0.7,
            parent_option_ids=[],
            parent_outcome_ids=[],
        ).model_dump(mode="json")
    ]
    
    create_response = await client.post("/discrete_probabilities", json=create_payload)
    assert create_response.status_code == 200
    
    # Now delete them in bulk
    response = await client.delete(f"/discrete_probabilities?ids={id1}&ids={id2}")
    assert response.status_code == 200, f"Response content: {response.content}"