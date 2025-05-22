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

async def seed_database(conn: AsyncConnection, num_projects: int, num_graphs: int, num_nodes: int):
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
            objectives=[],
            opportunities=[]
        )
        project = add_auditable_fields(project, user)
        entities.append(project)

        objective=Objective(
            id=project_index + 1,
            project_id=project.id,
            description=str(uuid4()),
            name=str(uuid4()),
            user_id=project.created_by_id
        )
        objective = add_auditable_fields(objective, user)
        entities.append(objective)

        opportunity=Opportunity(
            id=project_index + 1,
            project_id=project.id,
            description=str(uuid4()),
            name=str(uuid4()),
            user_id=project.created_by_id
        )
        opportunity = add_auditable_fields(opportunity, user)
        entities.append(opportunity)
        former_node_id=None
        for graph_index in range(num_graphs):
            graph_id=project_index * num_graphs + graph_index + 1
            graph = Graph(
                id=graph_id,
                name=str(uuid4()),
                project_id=project.id,
                user_id=project.created_by_id
            )
            graph = add_auditable_fields(graph, user)
            entities.append(graph)

            for node_index in range(num_nodes):
                node_id=project_index * num_graphs*num_nodes + graph_index * num_nodes + node_index + 1
                decision = Decision(
                    id=node_id,
                    options="yes,no"
                )
                entities.append(decision)

                probability = Probability(
                    id=node_id,
                    probabilities="0.5,0.5"
                )
                entities.append(probability)

                node = Node(
                    id=node_id,
                    graph_id=graph.id,
                    type="Decision",
                    user_id=graph.created_by_id,
                    decision_id=decision.id,
                    probability_id=probability.id  
                )
                node = add_auditable_fields(node, user)
                entities.append(node)

                if node_index > 0 and former_node_id is not None:
                    edge=Edge(
                        id=node_id-1, 
                        lower_node_id=former_node_id, 
                        higher_node_id=node_id, 
                        graph_id=graph.id
                    )
                    entities.append(edge)
                former_node_id=node_id

    async with AsyncSession(conn) as session:
        session.add_all(entities)    
        await session.commit()
