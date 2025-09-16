import uuid
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from src.constants import ProjectRoleType
from src.models.project_role import ProjectRole
from src.models import (
    User,
    Project,
    Scenario,
    Issue,
    Node,
    NodeStyle,
    Objective,
    Opportunity,
    Uncertainty,
    Utility,
    ValueMetric,
    Decision,
    Edge,
    Option,
    Outcome,
)
from typing import Protocol, TypeVar, Any

class AuditableEntityProtocol(Protocol):
    created_by_id: int
    updated_by_id: int

T = TypeVar('T', bound=AuditableEntityProtocol)

def add_auditable_fields(entity: T, user: User) -> T:
    entity.created_by_id = user.id
    entity.updated_by_id = user.id
    return entity

class GenerateUuid:
    @staticmethod
    def as_string(index: int) -> str: 
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{index}"))
    @staticmethod
    def as_uuid(index: int) -> uuid.UUID:
        return uuid.uuid5(uuid.NAMESPACE_DNS, f"{index}")

async def seed_database(conn: AsyncConnection, num_projects: int, num_scenarios: int, num_nodes: int):
    user1 = User(id=1, name=str("test_user_1"), azure_id=GenerateUuid.as_string(15))
    user2 = User(id=2, name=str("test_user_2"), azure_id=GenerateUuid.as_string(12))
    entities: list[Any]=[user1, user2]
    for project_index in range(num_projects):
        user = user1 if project_index % 2 == 0 else user2
        # Create a project with a UUID name and description
        project_id=GenerateUuid.as_uuid(project_index)
        project = Project(
            id=project_id,
            name=str(uuid4()),
            description=str(uuid4()),
            user_id=user.id,
            scenarios=None,
            project_role=[],
        )
        project = add_auditable_fields(project, user)
        entities.append(project)
        project_role = ProjectRole(
            id=project_id, 
            project_id=project_id,
            user_id=user.id,
            role=ProjectRoleType.OWNER
        )
        project_role = add_auditable_fields(project_role, user)
        entities.append(project_role)

        objective=Objective(
            id=project_id,
            scenario_id=project_id,
            description=str(uuid4()),
            name=str(uuid4()),
            user_id=project.created_by_id
        )
        objective = add_auditable_fields(objective, user)
        entities.append(objective)

        opportunity=Opportunity(
            id=project_id,
            scenario_id=project_id,
            description=str(uuid4()),
            name=str(uuid4()),
            user_id=project.created_by_id
        )
        opportunity = add_auditable_fields(opportunity, user)
        entities.append(opportunity)
        former_node_id=None
        default_scenario=True
        for scenario_index in range(num_scenarios):
            scenario_id=GenerateUuid.as_uuid(project_index * num_scenarios + scenario_index + 1)
            scenario = Scenario(
                id=scenario_id,
                name=str(uuid4()),
                is_default=default_scenario,
                project_id=project.id,
                user_id=project.created_by_id,
                objectives=[],
                opportunities=[]
            )
            scenario = add_auditable_fields(scenario, user)
            entities.append(scenario)
            default_scenario=False
            
            for issue_node_index in range(num_nodes):
                issue_node_id=GenerateUuid.as_uuid(project_index * num_scenarios*num_nodes + scenario_index * num_nodes + issue_node_index + 1)
                decision = Decision(
                    id=issue_node_id,
                    issue_id=issue_node_id,
                    options=[
                        Option(id = issue_node_id, decision_id=issue_node_id, name="yes", utility=-3),
                        Option(id = uuid4(), decision_id=issue_node_id, name="no", utility=30),
                    ]
                )
                entities.append(decision)

                uncertainty = Uncertainty(
                    id=issue_node_id,
                    issue_id=issue_node_id,
                    outcomes=[
                        Outcome(id=issue_node_id,uncertainty_id=issue_node_id,name="outcome 1",probability=0.4,utility=4),
                        Outcome(id=uuid4(),uncertainty_id=issue_node_id,name="outcome 2",probability=0.6,utility=2),
                    ]
                )
                entities.append(uncertainty)

                utility=Utility(
                    id=issue_node_id,
                    issue_id=issue_node_id,
                    values="200,150"
                )
                entities.append(utility)

                value_metric=ValueMetric(
                    id=issue_node_id,
                    issue_id=issue_node_id,
                    name=str(uuid4())
                )
                entities.append(value_metric)

                node = Node(
                    id=issue_node_id,
                    scenario_id=scenario.id,
                    issue_id=issue_node_id,
                    name=str(uuid4()),
                    node_style=None,
                )

                node_style = NodeStyle(
                    id=issue_node_id,
                    node_id=node.id,
                    x_position=40,
                    y_position=50,
                )

                issue = Issue(
                    id=issue_node_id,
                    scenario_id=scenario.id,
                    name=str(uuid4()),
                    description=str(uuid4()),
                    node=node,
                    type="Decision",
                    boundary="out",
                    order=0,
                    user_id=scenario.created_by_id,
                )

                issue = add_auditable_fields(issue, user)
                entities.append(node)
                entities.append(node_style)
                entities.append(issue)

                if issue_node_index > 0 and former_node_id is not None:
                    edge=Edge(
                        id=issue_node_id, 
                        tail_node_id=former_node_id, 
                        head_node_id=issue_node_id, 
                        scenario_id=scenario.id
                    )
                    entities.append(edge)
                former_node_id=issue_node_id

    async with AsyncSession(conn, autoflush=True) as session:
        session.add_all(entities)    
        await session.commit()
