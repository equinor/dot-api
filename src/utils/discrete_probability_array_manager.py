import xarray as xr
from typing import List

from src.dtos.discrete_probability_dtos import DiscreteProbabilityOutgoingDto

class DiscreteProbabilityArrayManager:
    """
    Manages a multidimensional array of discrete probabilities using xarray.
    """
    PARENT_IDS_DIM = 'parent_ids'
    CHILD_OUTCOMES_DIM = 'child_outcomes'
    PROBABILITY_GRID_NAME = 'probability_grid'
    PARENT_SEPARATOR = ','
    all_parent_ids: set[str] = set()
    
    def __init__(self, probabilities: List[DiscreteProbabilityOutgoingDto]) -> None:
        self.array: xr.DataArray = self.create_xarray_grid(probabilities)
    
    def _create_parents_label(self, parents: List[str]|tuple[str]|set[str]):
        """
        Create a unique label for a combination of parent IDs.
        """
        return f"{self.PARENT_SEPARATOR.join(sorted(parents))}"
    
    def create_xarray_grid(self, probabilities: List[DiscreteProbabilityOutgoingDto]) -> xr.DataArray:
        """
        Create an xarray DataArray to hold probabilities based on parent outcome combinations and child outcomes.
        """
        self.all_parent_ids = set()
        if not probabilities:
            return xr.DataArray([])
        
        # Get all unique child outcomes
        child_outcomes = sorted(set(p.child_outcome_id.__str__() for p in probabilities))
        
        # Create parent combinations
        parent_labels: list[str] = []
        probability_dict: dict[tuple[str, str], float] = {}
        
        for prob in probabilities:
            parent_ids = [id.__str__() for id in prob.parent_outcome_ids]+[id.__str__() for id in prob.parent_option_ids]
            self.all_parent_ids.update(parent_ids)
            parent_label = self._create_parents_label(parent_ids)
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
            dims=[self.PARENT_IDS_DIM, self.CHILD_OUTCOMES_DIM],
            coords={
                self.PARENT_IDS_DIM: parent_labels,
                self.CHILD_OUTCOMES_DIM: child_outcomes
            },
            name=self.PROBABILITY_GRID_NAME
        )
        
        return self.array
    
    def get_probabilities_for_combination(self, parents: List[str]|tuple[str]|set[str]) -> list[float]:
        """
        Retrieve probabilities for a given combination of parent IDs.
        """
        parents = self._filter_to_parent_ids(parents)
        return self.array.sel(**{self.PARENT_IDS_DIM: self._create_parents_label(parents)}).values.tolist()
    
    def _filter_to_parent_ids(self, parents: List[str]|tuple[str]|set[str]) -> List[str]:
        """
        Filter the input parents to only include those that are in the set of all parent IDs.
        """
        parents = set(parents)
        return [p for p in parents if p in self.all_parent_ids]