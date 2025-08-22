import uuid
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from src.models.project_contributors import ProjectContributors
from src.models.project_owners import ProjectOwners
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
    def as_string(x: int|str) -> str: 
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{x}"))
    @staticmethod
    def as_uuid(x: int|str) -> uuid.UUID:
        return uuid.uuid5(uuid.NAMESPACE_DNS, f"{x}")
    
async def create_single_project_with_scenario(conn: AsyncConnection):
    # Define all IDs at the beginning of the function
    user_id = 3
    project_id = GenerateUuid.as_uuid("test_project_1")
    scenario_id = GenerateUuid.as_uuid("test_scenario_1")
    decision_issue_id = GenerateUuid.as_uuid("test_decision_issue_1")
    decision_issue_id_2 = GenerateUuid.as_uuid("test_decision_issue_2")
    uncertainty_issue_id = GenerateUuid.as_uuid("test_uncertainty_issue_1")
    decision_option_yes_id = GenerateUuid.as_uuid("test_decision_option_yes")
    decision_option_no_id = GenerateUuid.as_uuid("test_decision_option_no")
    decision_option_2_yes_id = GenerateUuid.as_uuid("test_decision_option_yes_2")
    decision_option_2_no_id = GenerateUuid.as_uuid("test_decision_option_no_2")
    uncertainty_outcome_1_id = GenerateUuid.as_uuid("test_uncertainty_outcome_1")
    uncertainty_outcome_2_id = GenerateUuid.as_uuid("test_uncertainty_outcome_2")
    decision_node_id = GenerateUuid.as_uuid("test_decision_node_1")
    decision_node_id_2 = GenerateUuid.as_uuid("test_decision_node_2")
    uncertainty_node_id = GenerateUuid.as_uuid("test_uncertainty_node_1")
    edge_id = GenerateUuid.as_uuid("test_edge_1")
    edge_id_2 = GenerateUuid.as_uuid("test_edge_2")

    # Create a user
    user = User(id=user_id, name="test_user_3", azure_id="28652cc8-c5ed-43c7-a6b0-c2a4ce3d7185")
    entities: list[Any] = [user]

    # Create a project
    project = Project(
        id=project_id,
        name="Test Project 1",
        description="A test project with minimal data",
        user_id=user.id,
        scenarios=None,
    )
    project = add_auditable_fields(project, user)
    entities.append(project)

    # Create a scenario
    scenario = Scenario(
        id=scenario_id,
        name="Test Scenario 1",
        project_id=project.id,
        user_id=project.created_by_id,
        objectives=[],
        opportunities=[],
    )
    scenario = add_auditable_fields(scenario, user)
    entities.append(scenario)

    # Create a decision issue
    decision = Decision(
        id=decision_issue_id,
        issue_id=decision_issue_id,
        options=[
            Option(id=decision_option_yes_id, decision_id=decision_issue_id, name="yes", utility=10),
            Option(id=decision_option_no_id, decision_id=decision_issue_id, name="no", utility=-5),
        ],
    )
    entities.append(decision)

    decision_2 = Decision(
        id=decision_issue_id_2,
        issue_id=decision_issue_id_2,
        options=[
            Option(id=decision_option_2_yes_id, decision_id=decision_issue_id_2, name="yes2", utility=-100),
            Option(id=decision_option_2_no_id, decision_id=decision_issue_id_2, name="no2", utility=1.1),
        ],
    )
    entities.append(decision_2)

    # Create an uncertainty issue
    uncertainty = Uncertainty(
        id=uncertainty_issue_id,
        issue_id=uncertainty_issue_id,
        outcomes=[
            Outcome(id=uncertainty_outcome_1_id, uncertainty_id=uncertainty_issue_id, name="Outcome 1", probability=0.7, utility=15),
            Outcome(id=uncertainty_outcome_2_id, uncertainty_id=uncertainty_issue_id, name="Outcome 2", probability=0.3, utility=5),
        ],
    )
    entities.append(uncertainty)

    # Create a node for the decision issue
    decision_node = Node(
        id=decision_node_id,
        scenario_id=scenario.id,
        issue_id=decision_issue_id,
        name="Decision Node 1",
        node_style=None,
    )
    decision_node_style = NodeStyle(
        id=decision_node_id,
        node_id=decision_node.id,
        x_position=40,
        y_position=50,
    )
    entities.append(decision_node)
    entities.append(decision_node_style)

    # Create a node for the decision issue
    decision_node_2 = Node(
        id=decision_node_id_2,
        scenario_id=scenario.id,
        issue_id=decision_issue_id_2,
        name="Decision Node 1",
        node_style=None,
    )
    decision_node_style_2 = NodeStyle(
        id=decision_node_id_2,
        node_id=decision_node_2.id,
        x_position=50,
        y_position=40,
    )
    entities.append(decision_node_2)
    entities.append(decision_node_style_2)


    # Create a node for the uncertainty issue
    uncertainty_node = Node(
        id=uncertainty_node_id,
        scenario_id=scenario.id,
        issue_id=uncertainty_issue_id,
        name="Uncertainty Node 1",
        node_style=None,
    )
    uncertainty_node_style = NodeStyle(
        id=uncertainty_node_id,
        node_id=uncertainty_node.id,
        x_position=40,
        y_position=50,
    )
    entities.append(uncertainty_node)
    entities.append(uncertainty_node_style)

    # Create an edge between the decision node and the uncertainty node
    edge = Edge(
        id=edge_id,
        tail_node_id=decision_node.id,
        head_node_id=uncertainty_node.id,
        scenario_id=scenario.id,
    )
    entities.append(edge)

    edge_2 = Edge(
        id=edge_id_2,
        tail_node_id=uncertainty_node.id,
        head_node_id=decision_node_2.id,
        scenario_id=scenario.id,
    )
    entities.append(edge_2)

    # Create the decision issue entity
    decision_issue = Issue(
        id=decision_issue_id,
        scenario_id=scenario.id,
        name="Decision Issue 1",
        description="A test decision issue",
        node=decision_node,
        type="Decision",
        boundary="on",
        order=0,
        user_id=scenario.created_by_id,
    )
    decision_issue = add_auditable_fields(decision_issue, user)
    entities.append(decision_issue)

    decision_issue_2 = Issue(
        id=decision_issue_id_2,
        scenario_id=scenario.id,
        name="Decision Issue 2",
        description="A test decision issue",
        node=decision_node_2,
        type="Decision",
        boundary="on",
        order=1,
        user_id=scenario.created_by_id,
    )
    decision_issue = add_auditable_fields(decision_issue_2, user)
    entities.append(decision_issue_2)

    # Create the uncertainty issue entity
    uncertainty_issue = Issue(
        id=uncertainty_issue_id,
        scenario_id=scenario.id,
        name="Uncertainty Issue 1",
        description="A test uncertainty issue",
        node=uncertainty_node,
        type="Uncertainty",
        boundary="in",
        order=1,
        user_id=scenario.created_by_id,
    )
    uncertainty_issue = add_auditable_fields(uncertainty_issue, user)
    entities.append(uncertainty_issue)

    # Commit all entities to the database
    async with AsyncSession(conn) as session:
        session.add_all(entities)
        await session.commit()



async def seed_database(conn: AsyncConnection, num_projects: int, num_scenarios: int, num_nodes: int):
    user1 = User(id=1, name=str("test_user_1"), azure_id=str(uuid4()))
    user2 = User(id=2, name=str("test_user_2"), azure_id=str(uuid4()))
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
        )
        project = add_auditable_fields(project, user)
        entities.append(project)
        project_contributors = ProjectContributors(
            project_id=project_id,
            user_id=user.id
        )
        project_contributors = add_auditable_fields(project_contributors, user)
        entities.append(project_contributors)
        project_owners = ProjectOwners(
            project_id=project_id,
            user_id= user.id
        )
        project_owners = add_auditable_fields(project_owners, user)
        entities.append(project_owners)

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
        for scenario_index in range(num_scenarios):
            scenario_id=GenerateUuid.as_uuid(project_index * num_scenarios + scenario_index + 1)
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

    async with AsyncSession(conn) as session:
        session.add_all(entities)    
        await session.commit()
