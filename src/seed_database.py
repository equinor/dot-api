from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from src.models import *
from typing import Protocol, TypeVar, Any

class AuditableEntityProtocol(Protocol):
    created_by_id: int
    updated_by_id: int

T = TypeVar('T', bound=AuditableEntityProtocol)

def add_auditable_fields(entity: T, user: User) -> T:
    entity.created_by_id = user.id
    entity.updated_by_id = user.id
    return entity

async def seed_database(conn: AsyncConnection, num_projects: int, num_scenarios: int, num_nodes: int):
    user1 = User(id=1, name=str(uuid4()), azure_id=str(uuid4()))
    user2 = User(id=2, name=str(uuid4()), azure_id=str(uuid4()))
    entities: list[Any]=[user1, user2]

    for project_index in range(num_projects):
        user = user1 if project_index % 2 == 0 else user2
        # Create a project with a UUID name and description
        project = Project(
            id=project_index + 1,
            name=str(uuid4()),
            description=str(uuid4()),
            user_id=user.id,
            scenarios=None,
        )
        project = add_auditable_fields(project, user)
        entities.append(project)

        objective=Objective(
            id=project_index + 1,
            scenario_id=project.id,
            description=str(uuid4()),
            name=str(uuid4()),
            user_id=project.created_by_id
        )
        objective = add_auditable_fields(objective, user)
        entities.append(objective)

        opportunity=Opportunity(
            id=project_index + 1,
            scenario_id=project.id,
            description=str(uuid4()),
            name=str(uuid4()),
            user_id=project.created_by_id
        )
        opportunity = add_auditable_fields(opportunity, user)
        entities.append(opportunity)
        former_node_id=None
        for scenario_index in range(num_scenarios):
            scenario_id=project_index * num_scenarios + scenario_index + 1
            scenario = Scenario(
                id=scenario_id,
                name=str(uuid4()),
                project_id=project.id,
                user_id=project.created_by_id,
                objectives=[],
                opportunities=[]
            )
            scenario = add_auditable_fields(scenario, user)
            entities.append(scenario)

            for issue_node_index in range(num_nodes):
                issue_node_id=project_index * num_scenarios*num_nodes + scenario_index * num_nodes + issue_node_index + 1
                decision = Decision(
                    id=issue_node_id,
                    options="yes,no"
                )
                entities.append(decision)

                probability = Probability(
                    id=issue_node_id,
                    probabilities="0.5,0.5"
                )
                entities.append(probability)

                node = Node(
                    id=issue_node_id,
                    scenario_id=scenario.id,
                    issue_id=None,
                    name=str(uuid4()),
                )

                issue = Issue(
                    id=issue_node_id,
                    scenario_id=scenario.id,
                    node_id=node.id,
                    node=node,
                    type="Decision",
                    boundary="out",
                    user_id=scenario.created_by_id,
                    decision_id=decision.id,
                    probability_id=probability.id,
                )

                node.issue_id=issue.id

                issue = add_auditable_fields(issue, user)
                entities.append(node)
                entities.append(issue)

                if issue_node_index > 0 and former_node_id is not None:
                    edge=Edge(
                        id=issue_node_id-1, 
                        tail_node_id=former_node_id, 
                        head_node_id=issue_node_id, 
                        scenario_id=scenario.id
                    )
                    entities.append(edge)
                former_node_id=issue_node_id

    async with AsyncSession(conn) as session:
        session.add_all(entities)    
        await session.commit()
