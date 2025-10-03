from typing import List, Optional, Union
from pydantic import BaseModel
from typing import List

class Outcome(BaseModel):
    name: str
    probability: float
    utility: float

class Option(BaseModel):
    name: str
    utility: float

class Utility(BaseModel):
    values: List[float]

class BaseNode(BaseModel):
    name: str
    type: str

class DecisionNode(BaseNode):
    options: Optional[List[Option]] = None

class UncertaintyNode(BaseNode):
    outcomes: Optional[List[Outcome]] = None

class UtilityNode(BaseNode):
    values: Optional[Utility] = None          

class DecisionTreeDTO(BaseModel):
    id: Union[UtilityNode, UncertaintyNode, DecisionNode, BaseNode]
    children: Optional[List["DecisionTreeDTO"]] = None
