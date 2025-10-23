import xarray as xr
from typing import List

from src.dtos.discrete_probability_dtos import DiscreteProbabilityOutgoingDto

class DiscreteProbabilityArrayManager:
    def __init__(self, probabilities: List[DiscreteProbabilityOutgoingDto]) -> None:
        self.array: xr.DataArray = self.create_xarray_grid(probabilities)
    
    def create_parents_label(self, parents: List[str]|tuple[str]|set[str]):
        return f"{','.join(sorted(parents))}"
    
    def create_parents_ono_label(self, outcome_parents: List[str], option_parents: List[str]):
        return f"{','.join(sorted(outcome_parents+option_parents))}"

    def create_xarray_grid(self, probabilities: List[DiscreteProbabilityOutgoingDto]) -> xr.DataArray:
        if not probabilities:
            return xr.DataArray([])
        
        # Get all unique child outcomes
        child_outcomes = sorted(set(p.child_outcome_id.__str__() for p in probabilities))
        
        # Create parent combinations
        parent_labels: list[str] = []
        probability_dict: dict[tuple[str, str], float] = {}
        
        for prob in probabilities:
            parent_label = self.create_parents_label([id.__str__() for id in prob.parent_outcome_ids]+[id.__str__() for id in prob.parent_option_ids])
            if parent_label not in parent_labels:
                parent_labels.append(parent_label)
            
            probability_dict[(parent_label, prob.child_outcome_id.__str__())] = prob.probability
        
        # Sort parent combinations for consistency
        parent_labels = sorted(parent_labels)
        
        # Create the data array
        data: List[List[float]] = []
        for parent_label in parent_labels:
            row: list[float] = []
            for child_outcome in child_outcomes:
                probability = probability_dict.get((parent_label, child_outcome), 0.0)
                row.append(probability)
            data.append(row)
        
        # Create xarray DataArray
        self.array = xr.DataArray(
            data,
            dims=['parent_ids', 'child_outcomes'],
            coords={
                'parent_ids': parent_labels,
                'child_outcomes': child_outcomes
            },
            name='probability_grid'
        )
        
        return self.array
    
    def get_probabilities_for_combination(self, parents: List[str]|tuple[str]|set[str]) -> list[float]:
        return self.array.sel(parent_ids=self.create_parents_label(parents)).values.tolist()