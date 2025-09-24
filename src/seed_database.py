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
from src.constants import Type, Boundary


class AuditableEntityProtocol(Protocol):
    created_by_id: int
    updated_by_id: int


T = TypeVar("T", bound=AuditableEntityProtocol)


def add_auditable_fields(entity: T, user: User) -> T:
    entity.created_by_id = user.id
    entity.updated_by_id = user.id
    return entity


class GenerateUuid:
    @staticmethod
    def as_string(x: int | str) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{x}"))

    @staticmethod
    def as_uuid(x: int | str) -> uuid.UUID:
        return uuid.uuid5(uuid.NAMESPACE_DNS, f"{x}")


async def create_single_project_with_scenario(conn: AsyncConnection):
    # Define all IDs at the beginning of the function
    user_id = 3
    project_id = GenerateUuid.as_uuid("test_project_1")
    scenario_id = GenerateUuid.as_uuid("test_scenario_1")
    decision_issue_id = GenerateUuid.as_uuid("test_decision_issue_1")
    decision_issue_id_2 = GenerateUuid.as_uuid("test_decision_issue_2")
    decision_issue_id_3 = GenerateUuid.as_uuid("test_decision_issue_3")
    uncertainty_issue_id = GenerateUuid.as_uuid("test_uncertainty_issue_1")

    edge_id = GenerateUuid.as_uuid("test_edge_1")
    edge_id_2 = GenerateUuid.as_uuid("test_edge_2")

    def create_decision_issue(
        decision_id: uuid.UUID, issue_id: uuid.UUID, name: str, order: int,
    ):
        """Helper function to create a decision issue and its related entities."""
        decision = Decision(id=decision_id, issue_id=issue_id, options=[])
        node = Node(
            id=issue_id,
            scenario_id=scenario_id,
            issue_id=issue_id,
            name=name,
            node_style=None,
        )
        node_style = NodeStyle(id=issue_id, node_id=node.id)
        issue = Issue(
            id=issue_id,
            scenario_id=scenario_id,
            type=Type.DECISION.value,
            order=order,
            boundary=Boundary.ON.value,
            name=name,
            description=str(uuid.uuid4()),  # Example description
            user_id=user_id,
            node=node,
        )
        return [decision, node, node_style, issue]

    def create_uncertainty_issue(
        uncertainty_id: uuid.UUID, issue_id: uuid.UUID, name: str, order: int,
    ):
        """Helper function to create an uncertainty issue and its related entities."""
        uncertainty = Uncertainty(id=uncertainty_id, issue_id=issue_id, outcomes=[])
        node = Node(
            id=issue_id,
            scenario_id=scenario_id,
            issue_id=issue_id,
            name=name,
            node_style=None,
        )
        node_style = NodeStyle(id=issue_id, node_id=node.id)
        issue = Issue(
            id=issue_id,
            scenario_id=scenario_id,
            type=Type.UNCERTAINTY.value,
            order=order,
            boundary=Boundary.IN.value,
            name=name,
            description=str(uuid.uuid4()),  # Example description
            user_id=user_id,
            node=node,
        )
        return [uncertainty, node, node_style, issue]

    # Create a user
    user = User(
        id=user_id, name="test_user_3", azure_id="28652cc8-c5ed-43c7-a6b0-c2a4ce3d7185"
    )
    entities: list[Any] = [user]

    # Create a project
    project = Project(
        id=project_id,
        name="Test Project 1",
        description="A test project with minimal data",
        user_id=user.id,
        project_role=[],
        scenarios=None,
    )
    project = add_auditable_fields(project, user)
    entities.append(project)

    # Create a scenario
    scenario = Scenario(
        id=scenario_id,
        is_default=True,
        name="Test Scenario 1",
        project_id=project.id,
        user_id=project.created_by_id,
        objectives=[],
        opportunities=[],
    )
    scenario = add_auditable_fields(scenario, user)
    entities.append(scenario)

    # Add decision issues
    entities.extend(
        create_decision_issue(
            decision_issue_id, decision_issue_id, "Decision Issue 1", order=0
        )
    )
    entities.extend(
        create_decision_issue(
            decision_issue_id_2, decision_issue_id_2, "Decision Issue 2", order=1
        )
    )
    entities.extend(
        create_decision_issue(
            decision_issue_id_3, decision_issue_id_3, "Decision Issue 3", order=1
        )
    )

    # Add uncertainty issues
    entities.extend(
        create_uncertainty_issue(
            uncertainty_issue_id, uncertainty_issue_id, "Uncertainty Issue 1", order=2
        )
    )

    entities.append(
        Option(id=uuid.uuid4(), decision_id=decision_issue_id, name="yes", utility=10)
    )
    entities.append(
        Option(id=uuid.uuid4(), decision_id=decision_issue_id, name="no", utility=-5)
    )
    entities.append(
        Option(
            id=uuid.uuid4(), decision_id=decision_issue_id_2, name="yes2", utility=-100
        )
    )
    entities.append(
        Option(
            id=uuid.uuid4(), decision_id=decision_issue_id_2, name="no2", utility=1.1
        )
    )
    entities.append(
        Option(
            id=uuid.uuid4(), decision_id=decision_issue_id_3, name="yes", utility=-100
        )
    )
    entities.append(
        Option(id=uuid.uuid4(), decision_id=decision_issue_id_3, name="no", utility=1.1)
    )
    entities.append(
        Outcome(
            id=uuid.uuid4(),
            uncertainty_id=uncertainty_issue_id,
            name="Outcome 1",
            probability=0.7,
            utility=15,
        )
    )
    entities.append(
        Outcome(
            id=uuid.uuid4(),
            uncertainty_id=uncertainty_issue_id,
            name="Outcome 2",
            probability=0.3,
            utility=5,
        )
    )

    # Add edges
    edge_1 = Edge(
        id=edge_id,
        tail_node_id=decision_issue_id,
        head_node_id=uncertainty_issue_id,
        scenario_id=scenario_id,
    )
    edge_2 = Edge(
        id=edge_id_2,
        tail_node_id=uncertainty_issue_id,
        head_node_id=decision_issue_id_2,
        scenario_id=scenario_id,
    )
    edge_3 = Edge(
        id=uuid.uuid4(),
        tail_node_id=uncertainty_issue_id,
        head_node_id=decision_issue_id_3,
        scenario_id=scenario_id,
    )
    entities.extend([edge_1, edge_2, edge_3])

    # Commit all entities to the database
    async with AsyncSession(conn) as session:
        session.add_all(entities)
        await session.commit()


async def seed_database(
    conn: AsyncConnection, num_projects: int, num_scenarios: int, num_nodes: int
):
    user1 = User(id=1, name=str("test_user_1"), azure_id=GenerateUuid.as_string(15))
    user2 = User(id=2, name=str("test_user_2"), azure_id=GenerateUuid.as_string(12))
    entities: list[Any] = [user1, user2]
    for project_index in range(num_projects):
        user = user1 if project_index % 2 == 0 else user2
        # Create a project with a UUID name and description
        project_id = GenerateUuid.as_uuid(project_index)
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
            role=ProjectRoleType.OWNER,
        )
        project_role = add_auditable_fields(project_role, user)
        entities.append(project_role)

        objective = Objective(
            id=project_id,
            scenario_id=project_id,
            description=str(uuid4()),
            name=str(uuid4()),
            user_id=project.created_by_id,
        )
        objective = add_auditable_fields(objective, user)
        entities.append(objective)

        opportunity = Opportunity(
            id=project_id,
            scenario_id=project_id,
            description=str(uuid4()),
            name=str(uuid4()),
            user_id=project.created_by_id,
        )
        opportunity = add_auditable_fields(opportunity, user)
        entities.append(opportunity)
        former_node_id = None
        default_scenario = True
        for scenario_index in range(num_scenarios):
            scenario_id = GenerateUuid.as_uuid(
                project_index * num_scenarios + scenario_index + 1
            )
            scenario = Scenario(
                id=scenario_id,
                name=str(uuid4()),
                is_default=default_scenario,
                project_id=project.id,
                user_id=project.created_by_id,
                objectives=[],
                opportunities=[],
            )
            scenario = add_auditable_fields(scenario, user)
            entities.append(scenario)
            default_scenario = False

            for issue_node_index in range(num_nodes):
                issue_node_id = GenerateUuid.as_uuid(
                    project_index * num_scenarios * num_nodes
                    + scenario_index * num_nodes
                    + issue_node_index
                    + 1
                )
                decision = Decision(
                    id=issue_node_id,
                    issue_id=issue_node_id,
                    options=[
                        Option(
                            id=issue_node_id,
                            decision_id=issue_node_id,
                            name="yes",
                            utility=-3,
                        ),
                        Option(
                            id=uuid4(), decision_id=issue_node_id, name="no", utility=30
                        ),
                    ],
                )
                entities.append(decision)

                uncertainty = Uncertainty(
                    id=issue_node_id,
                    issue_id=issue_node_id,
                    outcomes=[
                        Outcome(
                            id=issue_node_id,
                            uncertainty_id=issue_node_id,
                            name="outcome 1",
                            probability=0.4,
                            utility=4,
                        ),
                        Outcome(
                            id=uuid4(),
                            uncertainty_id=issue_node_id,
                            name="outcome 2",
                            probability=0.6,
                            utility=2,
                        ),
                    ],
                )
                entities.append(uncertainty)

                utility = Utility(
                    id=issue_node_id, issue_id=issue_node_id, values="200,150"
                )
                entities.append(utility)

                value_metric = ValueMetric(
                    id=issue_node_id, issue_id=issue_node_id, name=str(uuid4())
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
                    id=issue_node_id, node_id=node.id, x_position=40, y_position=50,
                )

                issue = Issue(
                    id=issue_node_id,
                    scenario_id=scenario.id,
                    name=str(uuid4()),
                    description=str(uuid4()),
                    node=node,
                    type=Type.DECISION.value,
                    boundary=Boundary.OUT.value,
                    order=0,
                    user_id=scenario.created_by_id,
                )

                issue = add_auditable_fields(issue, user)
                entities.append(node)
                entities.append(node_style)
                entities.append(issue)

                if issue_node_index > 0 and former_node_id is not None:
                    edge = Edge(
                        id=issue_node_id,
                        tail_node_id=former_node_id,
                        head_node_id=issue_node_id,
                        scenario_id=scenario.id,
                    )
                    entities.append(edge)
                former_node_id = issue_node_id

    async with AsyncSession(conn, autoflush=True) as session:
        session.add_all(entities)
        await session.commit()
