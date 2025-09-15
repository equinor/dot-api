from pydantic import BaseModel
from typing import List
from src.dtos.option_dtos import OptionOutgoingDto

class SolutionDto(BaseModel):
    optimal_options: List[OptionOutgoingDto]
    utility_mean: float
    utility_variance: float