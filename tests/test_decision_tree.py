from src.dtos.edge_dtos import EdgeOutgoingDto
from src.dtos.issue_dtos import IssueOutgoingDto
import uuid
from src.services.decision_tree.utils import Utils



def create_edge_dto(edge_name, tail_node, head_node, scenario_id):
    id = uuid.uuid4() #(namespace, edge_name)
    return EdgeOutgoingDto(id=id, tail_id=tail_node.id, head_id=head_node.id, scenario_id=scenario_id, name=edge_name)

def graph_as_dict(scenario_id:uuid.UUID):
    # options_dict1 = {"option 1": 1,
    #                  "option 2": 2,
    #                  "option 3": 3}
    # options_dict2 = {"option 4": 10,
    #                  "option 5": 20,
    #                  "option 6": 30}
    # outcomes_dict1 = {"outcome 1": { "probability":0.3, "utility":150 },
    #                   "outcome 2": { "probability":0.5, "utility":200 },
    #                   "outcome 3": { "probability":0.2, "utility":80 }}
    # outcomes_dict2 = {"outcome 4": { "probability":0.4, "utility":20 },
    #                   "outcome 5": { "probability":0.2, "utility":10 },
    #                   "outcome 6": { "probability":0.4, "utility":30 }}
    
    options_dict1 = {"option 1": 1,
                     "option 2": 2}
    options_dict2 = {"option 4": 10,
                     "option 5": 20}
    outcomes_dict1 = {"outcome 1": { "probability":0.3, "utility":150 },
                      "outcome 2": { "probability":0.5, "utility":200 }}
    outcomes_dict2 = {"outcome 4": { "probability":0.4, "utility":20 },
                      "outcome 5": { "probability":0.2, "utility":10 }}
    
    #scenario_id = uuid.uuid4()
    u1 = Utils.create_uncertainty_issue(scenario_id, "u1", outcomes_dict1)
    u2 = Utils.create_uncertainty_issue(scenario_id, "u2", outcomes_dict2)
    d1 = Utils.create_decision_issue(scenario_id, "d1", options_dict1)
    d2 = Utils.create_decision_issue(scenario_id, "d2", options_dict2)
    print("d1", d1)
    print("d2", d2)


    e1 = create_edge_dto("e1", d1, u1, scenario_id)
    e2 = create_edge_dto("e2", d1, d2, scenario_id)
    e3 = create_edge_dto("e3", u1, d2, scenario_id)
    e4 = create_edge_dto("e4", d2, u2, scenario_id)

    return {
        "nodes": [           
            d1,
            d2,
            u1,
            u2,
        ],
        "edges": [
            e1,
            e2,
            e3,
            e4,
        ],
    }
