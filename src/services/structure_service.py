import uuid
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine

from src.services.edge_service import EdgeService
from src.services.issue_service import IssueService
from src.models.filters.issues_filter import IssueFilter, issue_conditions
from src.constants import Boundary, Type

from src.dtos.issue_dtos import (
    IssueOutgoingDto,
)

class StructureService:
    def __init__(self, issue_service: IssueService, edge_service: EdgeService):
        self.issue_service = issue_service
        self.edge_service = edge_service

    async def read_influence_diagramOK(self, scenario_uuid: uuid.UUID) -> list[IssueOutgoingDto]:
        filter = IssueFilter(
            scenario_id=scenario_uuid,
            #types=[Type.UNCERTAINTY, Type.DECISION, Type.VALUE_METRIC],  # List of types to filter
            #boundary=[Boundary.IN.value, Boundary.ON.value],
            boundary='out',
        )

        #issues = await self.issue_service.get_all(filter=IssueFilter(scenario_id=scenario_uuid)) #filter)
        issues = await self.issue_service.get_all(filter=filter)
        for issue in issues:
            print(issue.name, issue.type)
        #print(issues)
        #edges = self.edge_service.get_all()

        return issues
    
    
    async def read_influence_diagram(self, scenario_uuid: uuid.UUID) -> list[IssueOutgoingDto]:
        filter = IssueFilter(
            scenario_id=scenario_uuid,
            #types=[Type.UNCERTAINTY, Type.DECISION, Type.VALUE_METRIC],  # List of types to filter
            #boundary=[Boundary.IN.value, Boundary.ON.value],
            boundary='out',
        )

        #issues = await self.issue_service.get_all(filter=IssueFilter(scenario_id=scenario_uuid)) #filter)
        issues = await self.issue_service.get_all(filter=filter)
        for issue in issues:
            print(issue.name, issue.type)
        #print(issues)
        edges = self.edge_service.get_all()

        return issues, edges




        # read nodes (uncertainty, decision, valuemetric category)
        vertices = []

        # In boundary
        # for vertex_category in ["Uncertainty", "Decision", "Value Metric"]:
        #     for boundary in ["in", "on"]:
        #         filter_model = Filter(category=vertex_category, boundary=boundary)
        #         if vertex_category == "Uncertainty":
        #             filter_model.keyUncertainty = "true"
        #         elif vertex_category == "Decision":
        #             filter_model.decisionType = "Focus"
        #         vertex = self.repository.read_out_vertex(
        #             vertex_uuid=project_uuid,
        #             original_vertex_label="issue",
        #             edge_label="contains",
        #             filter_model=filter_model,
        #         )
        #         vertices.extend(vertex)

        # create list of Issue objects from vertices
        # issues_list = [
        #     IssueResponse.model_validate(v.model_dump()) for v in vertices if v
        # ]

        # edges = edge_repository.read_all_edges_from_sub_project(
        #     project_uuid=project_uuid,
        #     edge_label="influences",
        #     vertex_uuid=[issue.uuid for issue in issues_list],
        # )

        # influence_diagram = InfluenceDiagramResponse(vertices=issues_list, edges=edges)
        # return influence_diagram


    async def create_decision_tree(self, scenario_uuid: uuid.UUID) -> list[IssueOutgoingDto]:

        issues, edges = self.read_influence_diagram(scenario_uuid=scenario_uuid)
    #     influence_diagram = self.read_influence_diagram(scenario_uuid=scenario_uuid)
    #     local_id = InfluenceDiagram.from_db(influence_diagram)
    #     local_dt = local_id.convert_to_decision_tree()
    #     dt_json = json.loads(local_dt.to_json())
    #     decision_tree = DecisionTreeResponse.model_validate(dt_json)
    #     return decision_tree

   
