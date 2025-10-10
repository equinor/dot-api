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
    DiscreteProbability,
    DiscreteProbabilityParentOption,
)
from typing import Protocol, TypeVar, Any, Union, Dict, Tuple, List
from src.constants import Type, Boundary, ObjectiveTypes


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

def create_decision_issue(
        scenario_id: uuid.UUID,
        decision_id: uuid.UUID,
        issue_id: uuid.UUID,
        user_id: int,
        name: str,
        order: int,
    ) -> list[Union[Decision, Node, NodeStyle, Uncertainty]]:
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
        scenario_id: uuid.UUID,
        uncertainty_id: uuid.UUID,
        issue_id: uuid.UUID,
        user_id: int,
        name: str,
        order: int,
    ) -> list[Union[Uncertainty, Node, NodeStyle, Issue]]:
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

def create_utility_issue(
        scenario_id: uuid.UUID,
        utility_id: uuid.UUID,
        issue_id: uuid.UUID,
        user_id: int,
        name: str,
        order: int,
    ) -> list[Union[Utility, Node, NodeStyle, Issue]]:
        """Helper function to create an utility issue and its related entities."""
        utility = Utility(id=utility_id, values='', issue_id=issue_id)
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
            type=Type.UTILITY.value,
            order=order,
            boundary=Boundary.IN.value,
            name=name,
            description=str(uuid.uuid4()),  # Example description
            user_id=user_id,
            node=node,
        )
        return [utility, node, node_style, issue]

async def create_single_project_with_scenario(conn: AsyncConnection):
    # Define all IDs at the beginning of the function
    user_id = 3
    project_id = GenerateUuid.as_uuid("test_project_1")
    scenario_id = GenerateUuid.as_uuid("test_scenario_1")
    decision_issue_id = GenerateUuid.as_uuid("test_decision_issue_1")
    decision_issue_id_2 = GenerateUuid.as_uuid("test_decision_issue_2")
    decision_issue_id_3 = GenerateUuid.as_uuid("test_decision_issue_3")
    uncertainty_issue_id = GenerateUuid.as_uuid("test_uncertainty_issue_1")
    option_id_1 = uuid.uuid4()
    option_id_2 = uuid.uuid4()
    option_id_3 = uuid.uuid4()
    option_id_4 = uuid.uuid4()
    option_id_5 = uuid.uuid4()
    option_id_6 = uuid.uuid4()
    outcome_id_1 = uuid.uuid4()
    outcome_id_2 = uuid.uuid4()

    edge_id = GenerateUuid.as_uuid("test_edge_1")
    edge_id_2 = GenerateUuid.as_uuid("test_edge_2")

    # Create a user
    user = User(
        id=user_id,
        name="test_user_3",
        azure_id="28652cc8-c5ed-43c7-a6b0-c2a4ce3d7185",
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
            scenario_id,
            decision_issue_id,
            decision_issue_id,
            user_id,
            "Decision Issue 1",
            order=0)
    )
    entities.extend(
        create_decision_issue(
            scenario_id,
            decision_issue_id_2,
            decision_issue_id_2,
            user_id,
            "Decision Issue 2",
            order=1,
        )
    )
    entities.extend(
        create_decision_issue(
            scenario_id,
            decision_issue_id_3,
            decision_issue_id_3,
            user_id,
            "Decision Issue 3",
            order=1,
        )
    )

    # Add uncertainty issues
    entities.extend(
        create_uncertainty_issue(
            scenario_id,
            uncertainty_issue_id,
            uncertainty_issue_id,
            user_id,
            "Uncertainty Issue 1",
            order=2,
        )
    )

    entities.append(
        Option(
            id=option_id_1,
            decision_id=decision_issue_id,
            name="yes",
            utility=0,
        )
    )
    entities.append(
        Option(
            id=option_id_2,
            decision_id=decision_issue_id,
            name="no",
            utility=0,
        )
    )
    entities.append(
        Option(
            id=option_id_3,
            decision_id=decision_issue_id_2,
            name="yes2",
            utility=0,
        )
    )
    entities.append(
        Option(
            id=option_id_4,
            decision_id=decision_issue_id_2,
            name="no2",
            utility=0,
        )
    )
    entities.append(
        Option(
            id=option_id_5,
            decision_id=decision_issue_id_3,
            name="yes",
            utility=0,
        )
    )
    entities.append(
        Option(
            id=option_id_6,
            decision_id=decision_issue_id_3,
            name="no",
            utility=0,
        )
    )
    entities.append(
        Outcome(
            id=outcome_id_1,
            uncertainty_id=uncertainty_issue_id,
            name="Outcome 1",
            utility=-105,
        )
    )
    entities.append(
        Outcome(
            id=outcome_id_2,
            uncertainty_id=uncertainty_issue_id,
            name="Outcome 2",
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

    discrete_probability_id_1 = uuid.uuid4()

    discrete_probability_1=DiscreteProbability(
        id=discrete_probability_id_1,
        child_outcome_id=outcome_id_1,
        uncertainty_id=uncertainty_issue_id,
        probability=0.8,
        parent_options=[DiscreteProbabilityParentOption(discrete_probability_id=discrete_probability_id_1, parent_option_id=option_id_1)] 
    )

    discrete_probability_id_2 = uuid.uuid4()

    discrete_probability_2=DiscreteProbability(
        id=discrete_probability_id_2,
        child_outcome_id=outcome_id_1,
        uncertainty_id=uncertainty_issue_id,
        probability=0.7,
        parent_options=[DiscreteProbabilityParentOption(discrete_probability_id=discrete_probability_id_2, parent_option_id=option_id_2)]
    )

    discrete_probability_id_3 = uuid.uuid4()

    discrete_probability_3=DiscreteProbability(
        id=discrete_probability_id_3,
        child_outcome_id=outcome_id_2,
        uncertainty_id=uncertainty_issue_id,
        probability=0.2,
        parent_options=[DiscreteProbabilityParentOption(discrete_probability_id=discrete_probability_id_3, parent_option_id=option_id_1)] 
    )

    discrete_probability_id_4 = uuid.uuid4()

    discrete_probability_4=DiscreteProbability(
        id=discrete_probability_id_4,
        child_outcome_id=outcome_id_2,
        uncertainty_id=uncertainty_issue_id,
        probability=0.3,
        parent_options=[DiscreteProbabilityParentOption(discrete_probability_id=discrete_probability_id_4, parent_option_id=option_id_2)]
    )

    entities.extend([discrete_probability_1, discrete_probability_2, discrete_probability_3, discrete_probability_4])

    discrete_probability_id_1 = uuid.uuid4()

    discrete_probability_1=DiscreteProbability(
        id=discrete_probability_id_1,
        child_outcome_id=outcome_id_1,
        uncertainty_id=uncertainty_issue_id,
        probability=0.8,
        parent_options=[DiscreteProbabilityParentOption(discrete_probability_id=discrete_probability_id_1, parent_option_id=option_id_1)] 
    )

    discrete_probability_id_2 = uuid.uuid4()

    discrete_probability_2=DiscreteProbability(
        id=discrete_probability_id_2,
        child_outcome_id=outcome_id_1,
        uncertainty_id=uncertainty_issue_id,
        probability=0.7,
        parent_options=[DiscreteProbabilityParentOption(discrete_probability_id=discrete_probability_id_2, parent_option_id=option_id_2)]
    )

    discrete_probability_id_3 = uuid.uuid4()

    discrete_probability_3=DiscreteProbability(
        id=discrete_probability_id_3,
        child_outcome_id=outcome_id_2,
        uncertainty_id=uncertainty_issue_id,
        probability=0.2,
        parent_options=[DiscreteProbabilityParentOption(discrete_probability_id=discrete_probability_id_3, parent_option_id=option_id_1)] 
    )

    discrete_probability_id_4 = uuid.uuid4()

    discrete_probability_4=DiscreteProbability(
        id=discrete_probability_id_4,
        child_outcome_id=outcome_id_2,
        uncertainty_id=uncertainty_issue_id,
        probability=0.3,
        parent_options=[DiscreteProbabilityParentOption(discrete_probability_id=discrete_probability_id_4, parent_option_id=option_id_2)]
    )

    entities.extend([discrete_probability_1, discrete_probability_2, discrete_probability_3, discrete_probability_4])

    # Commit all entities to the database
    async with AsyncSession(conn) as session:
        session.add_all(entities)
        await session.commit()


async def create_decision_tree_symmetry_DT_from_ID(conn: AsyncConnection):
    # Define all IDs at the beginning of the function
    user_id = 5
    project_id = GenerateUuid.as_uuid("dt_from_id_project")
    scenario_id = GenerateUuid.as_uuid("dt_from_id_scenario")
    decision_T_id = GenerateUuid.as_uuid("dt_from_id_decision_T")
    uncertainty_S_id = GenerateUuid.as_uuid("dt_from_id_uncertainty_S")
    uncertainty_D_id = GenerateUuid.as_uuid("dt_from_id_uncertainty_D")
    uncertainty_P_id = GenerateUuid.as_uuid("dt_from_id_uncertainty_P")
    utility_id = GenerateUuid.as_uuid("dt_from_id_utility")
    edge_uuids = [GenerateUuid.as_uuid(f"dt_from_id_edge_{i}") for i in range(6)]

    # Create a user
    user = User(id=user_id, name="test_user_3", azure_id=str(uuid4()))
    entities: list[Any] = [user]

    # Create a project
    project = Project(
        id=project_id,
        name="Test Project decision tree symmetry",
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
        name="Scenario symmetry decision tree from influence diagram",
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
            scenario_id,
            decision_T_id,
            decision_T_id,
            user_id,
            "Treat for disease",
            order=0))

    # Add uncertainty issues
    entities.extend(
        create_uncertainty_issue(
            scenario_id,
            uncertainty_S_id,
            uncertainty_S_id,
            user_id,
            "Symptom",
            order=1))

    entities.extend(
        create_uncertainty_issue(
            scenario_id,
            uncertainty_D_id,
            uncertainty_D_id,
            user_id,
            "Disease",
            order=1))

    entities.extend(
        create_uncertainty_issue(
            scenario_id,
            uncertainty_P_id,
            uncertainty_P_id,
            user_id,
            "Pathological state",
            order=1))

    # Add utility issues
    entities.extend(
        create_utility_issue(
            scenario_id,
            utility_id,
            utility_id,
            user_id,
            "Utility",
            order=1))

    entities.append(
        Option(
            id=uuid.uuid4(),
            decision_id=decision_T_id,
            name="yes",
            utility=0))
    entities.append(
        Option(
            id=uuid.uuid4(),
            decision_id=decision_T_id,
            name="no",
            utility=0))
    entities.append(
        Outcome(
            id=uuid.uuid4(),
            uncertainty_id=uncertainty_S_id,
            name="yes",
            utility=0))
    entities.append(
        Outcome(
            id=uuid.uuid4(),
            uncertainty_id=uncertainty_S_id,
            name="no",
            utility=0))
    entities.append(
        Outcome(
            id=uuid.uuid4(),
            uncertainty_id=uncertainty_D_id,
            name="yes",
            utility=0))
    entities.append(
        Outcome(
            id=uuid.uuid4(),
            uncertainty_id=uncertainty_D_id,
            name="no",
            utility=0))
    entities.append(
        Outcome(
            id=uuid.uuid4(),
            uncertainty_id=uncertainty_P_id,
            name="yes",
            utility=0))
    entities.append(
        Outcome(
            id=uuid.uuid4(),
            uncertainty_id=uncertainty_P_id,
            name="no",
            utility=0))

    #Add edges
    edges_data = [
        (edge_uuids[0], uncertainty_S_id, decision_T_id),
        (edge_uuids[1], uncertainty_P_id, uncertainty_S_id),
        (edge_uuids[2], uncertainty_D_id, uncertainty_P_id),
        (edge_uuids[3], decision_T_id, utility_id),
        (edge_uuids[4], uncertainty_P_id, utility_id),
        (edge_uuids[5], uncertainty_D_id, utility_id),
    ]
    for edge_id, tail_node_id, head_node_id in edges_data:
        entities.append(
            Edge(
                id=edge_id,
                tail_node_id=tail_node_id,
                head_node_id=head_node_id,
                scenario_id=scenario_id))

    # Commit all entities to the database
    async with AsyncSession(conn) as session:
        session.add_all(entities)
        await session.commit()


async def create_decision_tree_symmetry_DT(conn: AsyncConnection):
    # Define all IDs at the beginning of the function
    user_id = 6
    project_uuid = GenerateUuid.as_uuid("dt_project")
    scenario_uuid = GenerateUuid.as_uuid("dt_scenario")
    uncertainty_S_uuids = [GenerateUuid.as_uuid("dt_uncertainty_S")]
    uncertainty_P_uuids = [GenerateUuid.as_uuid(f"dt_uncertainty_P_{i}") for i in range(4)]
    uncertainty_D_uuids = [GenerateUuid.as_uuid(f"dt_uncertainty_D_{i}") for i in range(8)]
    decision_uuids = [GenerateUuid.as_uuid(f"dt_decision_T_{i}") for i in range(2)]
    utility_uuids = [GenerateUuid.as_uuid(f"dt_utility_{i}") for i in range(16)]
    edge_uuids = [GenerateUuid.as_uuid(f"dt_edge_{i}") for i in range(30)]

    # Define strings
    treat_for_disease = "Treat for disease"
    pathological_state = "Pathological state"
    disease = "Disease"
    symptom = "Symptom"

    # Create a user
    user = User(id=user_id, name="test_user_5", azure_id=str(uuid4()))
    entities: list[Any] = [user]

    # Create a project
    project = Project(
        id=project_uuid,
        name="Test Project decision tree symmetry",
        description="A test project with minimal data",
        user_id=user.id,
        project_role=[],
        scenarios=None,
    )
    project = add_auditable_fields(project, user)
    entities.append(project)

    # Create a scenario
    scenario = Scenario(
        id=scenario_uuid,
        is_default=True,
        name="Scenario symmetry decision tree",
        project_id=project.id,
        user_id=project.created_by_id,
        objectives=[],
        opportunities=[],
    )
    scenario = add_auditable_fields(scenario, user)
    entities.append(scenario)

    # Add decision issues
    decision_issues = [
        (decision_uuids[0], treat_for_disease),
        (decision_uuids[1], treat_for_disease)
    ]
    for decision_id, name in decision_issues:
        entities.extend(
            create_decision_issue(
                scenario_uuid,
                decision_id,
                decision_id,
                user_id,
                name,
                order=1))

    # Add uncertainty issues
    uncertainty_issues = [
        (uncertainty_S_uuids[0], symptom),
        (uncertainty_P_uuids[0], pathological_state),
        (uncertainty_P_uuids[1], pathological_state),
        (uncertainty_P_uuids[2], pathological_state),
        (uncertainty_P_uuids[3], pathological_state),
        (uncertainty_D_uuids[0], disease),
        (uncertainty_D_uuids[1], disease),
        (uncertainty_D_uuids[2], disease),
        (uncertainty_D_uuids[3], disease),
        (uncertainty_D_uuids[4], disease),
        (uncertainty_D_uuids[5], disease),
        (uncertainty_D_uuids[6], disease),
        (uncertainty_D_uuids[7], disease)
    ]
    for uncertainty_id, name in uncertainty_issues:
        entities.extend(
            create_uncertainty_issue(
                scenario_uuid,
                uncertainty_id,
                uncertainty_id,
                user_id,
                name,
                order=1))

    # Add utility issues
    for utility_id in utility_uuids:
        entities.extend(
            create_utility_issue(
                scenario_uuid,
                utility_id,
                utility_id,
                user_id,
                "Utility",
                order=1))

    # Add decision issues
    options = ["yes", "no"]

    for decision_id in decision_uuids:
        for option in options:
            entities.append(
                Option(
                    id=uuid.uuid4(),
                    decision_id=decision_id,
                    name=option,
                    utility=0))

    # Add uncertainty issues
    def create_outcome(uncertainty_id: uuid.UUID, probability_name: str):
        return Outcome(
            id=uuid.uuid4(),
            uncertainty_id=uncertainty_id,
            name=probability_name,
            utility=0)

    probabilities: Dict[str, List[Tuple[str, float]]] = {
        'S': [('yes', 0.7), ('no', 0.3)],
        'P': [('yes', 0.2), ('no', 0.8)],
        'D': [('yes', 0.1), ('no', 0.9)]
    }

    uncertainty_uuids : dict[str, list[uuid.UUID]] = {
        'S': uncertainty_S_uuids,
        'P': uncertainty_P_uuids,
        'D': uncertainty_D_uuids
    }

    for key, probability_list in probabilities.items():
        if key == 'S':
            entities.append(
                create_outcome(
                    uncertainty_uuids[key][0],
                    probability_list[0][0]))
            entities.append(
                create_outcome(
                    uncertainty_uuids[key][0],
                    probability_list[1][0]))
        else:
            for uncertainty_uuid in uncertainty_uuids[key]:
                for probability in probability_list:
                    entities.append(
                        create_outcome(
                            uncertainty_uuid,
                            probability[0]))

    #Add edges
    edges_data = [
        (edge_uuids[0], uncertainty_S_uuids[0], decision_uuids[0]),
        (edge_uuids[1], decision_uuids[0], uncertainty_P_uuids[0]),
        (edge_uuids[2], uncertainty_P_uuids[0], uncertainty_D_uuids[0]),
        (edge_uuids[3], uncertainty_D_uuids[0], utility_uuids[0]),
        (edge_uuids[4], uncertainty_D_uuids[0], utility_uuids[1]),
        (edge_uuids[5], uncertainty_P_uuids[0], uncertainty_D_uuids[1]),
        (edge_uuids[6], uncertainty_D_uuids[1], utility_uuids[2]),
        (edge_uuids[7], uncertainty_D_uuids[1], utility_uuids[3]),
        (edge_uuids[8], decision_uuids[0], uncertainty_P_uuids[1]),
        (edge_uuids[9], uncertainty_P_uuids[1], uncertainty_D_uuids[2]),
        (edge_uuids[10], uncertainty_D_uuids[2], utility_uuids[4]),
        (edge_uuids[11], uncertainty_D_uuids[2], utility_uuids[5]),
        (edge_uuids[12], uncertainty_P_uuids[1], uncertainty_D_uuids[3]),
        (edge_uuids[13], uncertainty_D_uuids[3], utility_uuids[6]),
        (edge_uuids[14], uncertainty_D_uuids[3], utility_uuids[7]),
        (edge_uuids[15], uncertainty_S_uuids[0], decision_uuids[1]),
        (edge_uuids[16], decision_uuids[1], uncertainty_P_uuids[2]),
        (edge_uuids[17], uncertainty_P_uuids[2], uncertainty_D_uuids[4]),
        (edge_uuids[18], uncertainty_D_uuids[4], utility_uuids[8]),
        (edge_uuids[19], uncertainty_D_uuids[4], utility_uuids[9]),
        (edge_uuids[20], uncertainty_P_uuids[2], uncertainty_D_uuids[5]),
        (edge_uuids[21], uncertainty_D_uuids[5], utility_uuids[10]),
        (edge_uuids[22], uncertainty_D_uuids[5], utility_uuids[11]),
        (edge_uuids[23], decision_uuids[1], uncertainty_P_uuids[3]),
        (edge_uuids[24], uncertainty_P_uuids[3], uncertainty_D_uuids[6]),
        (edge_uuids[25], uncertainty_D_uuids[6], utility_uuids[12]),
        (edge_uuids[26], uncertainty_D_uuids[6], utility_uuids[13]),
        (edge_uuids[27], uncertainty_P_uuids[3], uncertainty_D_uuids[7]),
        (edge_uuids[28], uncertainty_D_uuids[7], utility_uuids[14]),
        (edge_uuids[29], uncertainty_D_uuids[7], utility_uuids[15])
    ]
    for edge_id, tail_node_id, head_node_id in edges_data:
        entities.append(
            Edge(id=edge_id,
                 tail_node_id=tail_node_id,
                 head_node_id=head_node_id,
                 scenario_id=scenario_uuid))

    # Commit all entities to the database
    async with AsyncSession(conn) as session:
        session.add_all(entities)
        await session.commit()

async def seed_database(
    conn: AsyncConnection,
    num_projects: int,
    num_scenarios: int,
    num_nodes: int,
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
            role=ProjectRoleType.FACILITATOR,
        )
        project_role = add_auditable_fields(project_role, user)
        entities.append(project_role)

        objective = Objective(
            id=project_id,
            scenario_id=project_id,
            description=str(uuid4()),
            name=str(uuid4()),
            type=ObjectiveTypes.FUNDAMENTAL.value,
            user_id=project.created_by_id,
        )
        objective = add_auditable_fields(objective, user)
        entities.append(objective)

        opportunity = Opportunity(
            id=project_id,
            scenario_id=project_id,
            description=str(uuid4()),
            user_id=project.created_by_id,
        )
        opportunity = add_auditable_fields(opportunity, user)
        entities.append(opportunity)
        former_node_id = None
        default_scenario = True
        for scenario_index in range(num_scenarios):
            scenario_id = GenerateUuid.as_uuid(project_index * num_scenarios + scenario_index + 1)
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
                            id=uuid4(),
                            decision_id=issue_node_id,
                            name="no",
                            utility=30,
                        ),
                    ],
                )
                entities.append(decision)

                # Create outcome IDs to reference consistently
                outcome1_id = issue_node_id
                outcome2_id = uuid4()
                
                # Create unique IDs for outcome probabilities
                outcome_prob1_id = GenerateUuid.as_uuid(f"{project_index}_{scenario_index}_{issue_node_index}_op1")
                outcome_prob2_id = GenerateUuid.as_uuid(f"{project_index}_{scenario_index}_{issue_node_index}_op2")
                
                uncertainty = Uncertainty(
                    id=issue_node_id,
                    issue_id=issue_node_id,
                    outcomes=[
                        Outcome(
                            id=outcome1_id,
                            uncertainty_id=issue_node_id,
                            name="outcome 1",
                            utility=4,
                        ),
                        Outcome(
                            id=outcome2_id,
                            uncertainty_id=issue_node_id,
                            name="outcome 2",
                            utility=2,
                        ),
                    ],
                    discrete_probabilities=[
                        DiscreteProbability(
                            id=outcome_prob1_id,
                            uncertainty_id=issue_node_id,
                            child_outcome_id=outcome1_id,
                            probability=0.6,
                            parent_outcomes=[],
                            parent_options=[],
                        ),
                        DiscreteProbability(
                            id=outcome_prob2_id,
                            uncertainty_id=issue_node_id,
                            child_outcome_id=outcome2_id,
                            probability=0.4,
                            parent_outcomes=[],
                            parent_options=[],
                        ),
                    ],
                )
                entities.append(uncertainty)

                utility = Utility(id=issue_node_id, issue_id=issue_node_id, values="200,150")
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
