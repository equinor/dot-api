import uuid

from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import get_history

from src.models import (
    Edge, Issue, Outcome, Option, Uncertainty, Decision,
    DiscreteProbability, DiscreteProbabilityParentOption, DiscreteProbabilityParentOutcome,
)
from src.constants import (Type, DecisionHierarchy, Boundary)

from src.repositories import option_repository, outcome_repository, edge_repository, uncertainty_repository, issue_repository
from src.utils.session_info_handler import SessionInfoHandler

class DiscreteProbabilityEventHandler:
    """Handles events that require discrete probability table recalculation."""

    subscribed_entities_delete = [Edge, DiscreteProbabilityParentOption, DiscreteProbabilityParentOutcome]
    subscribed_entities_modified = [Issue, Uncertainty, Decision]
    subscribed_entities_new = [Edge, Option, Outcome]

    def process_session_changes_before_flush(self, session: Session) -> None:
        """Process all session changes and determine which uncertainties need recalculation."""
        # Filter to only subscribed entities
        subscribed_dirty = [
            entity for entity in session.dirty
            if any(isinstance(entity, entity_type) for entity_type in self.subscribed_entities_modified)
        ]
        subscribed_deleted = [
            entity for entity in session.deleted
            if any(isinstance(entity, entity_type) for entity_type in self.subscribed_entities_delete)
        ]
        
        if not (subscribed_dirty or subscribed_deleted):
            return

        session_info = SessionInfoHandler.get_session_info(session)
        
        # Process changes in order of dependency
        session_info.affected_uncertainties.update(self._process_deletions(session, subscribed_deleted))
        session_info.affected_uncertainties.update(self._process_modifications(session, subscribed_dirty))
        
        SessionInfoHandler.update_session_info(session, session_info)

    def process_session_changes_after_flush(self, session: Session) -> None:
        """Process all session changes and determine which uncertainties need recalculation."""
        # Filter to only subscribed entities
        subscribed_new = [
            entity for entity in session.new 
            if any(isinstance(entity, entity_type) for entity_type in self.subscribed_entities_new)
        ]
        
        if not subscribed_new:
            return
        
        session_info = SessionInfoHandler.get_session_info(session)
        
        # Process changes in order of dependency
        session_info.affected_uncertainties.update(self._process_additions(session, subscribed_new))
        
        SessionInfoHandler.update_session_info(session, session_info)
    
    def _process_deletions(self, session: Session, deleted_entities: list[Any]) -> set[uuid.UUID]:
        """Process deleted entities and find affected uncertainties."""
        affected_uncertainties: set[uuid.UUID] = set()

        discrete_probabilities_to_delete: set[uuid.UUID] = set()
        for deleted_entity in deleted_entities:
            if isinstance(deleted_entity, Edge):
                affected_uncertainties.update(
                    edge_repository.find_effected_uncertainties(session, {deleted_entity.id})
                )
            if isinstance(deleted_entity, DiscreteProbabilityParentOutcome) or isinstance(deleted_entity, DiscreteProbabilityParentOption):
                discrete_probabilities_to_delete.add(deleted_entity.discrete_probability_id)
        
        if discrete_probabilities_to_delete:
            session.execute(
                DiscreteProbabilityParentOutcome.__table__.delete()
                .where(DiscreteProbabilityParentOutcome.discrete_probability_id.in_(discrete_probabilities_to_delete))
            )

            # Then delete all parent option relationships
            session.execute(
                DiscreteProbabilityParentOption.__table__.delete()
                .where(DiscreteProbabilityParentOption.discrete_probability_id.in_(discrete_probabilities_to_delete))
            )

            # Finally delete the DiscreteProbability record itself
            session.execute(
                DiscreteProbability.__table__.delete()
                .where(DiscreteProbability.id.in_(discrete_probabilities_to_delete))
            )

            
        
        return affected_uncertainties
    
    def _process_modifications(self, session: Session, modified_entities: list[Any]) -> set[uuid.UUID]:
        """Process modified entities and find affected uncertainties."""
        affected_uncertainties: set[uuid.UUID] = set()
        issues_to_search: set[uuid.UUID] = set()
        
        for modified_entity in modified_entities:
            if isinstance(modified_entity, Issue):
                if self._has_boundary_change(modified_entity):
                    issues_to_search.add(modified_entity.id)
                
                if self._has_type_change_to_or_from_uncertainty_decision(modified_entity):
                    affected_uncertainties.add(modified_entity.id)
                    issues_to_search.add(modified_entity.id)
            
            elif isinstance(modified_entity, Uncertainty):
                if self._has_key_change(modified_entity):
                    issues_to_search.add(modified_entity.issue_id)
            
            elif isinstance(modified_entity, Decision):
                if self._has_focus_type_change(modified_entity):
                    issues_to_search.add(modified_entity.issue_id)
        
        # Find affected uncertainties from issue changes
        if issues_to_search:
            affected_uncertainties.update(
                issue_repository.find_effected_uncertainties(session, issues_to_search)
            )
        
        return affected_uncertainties
    
    def _process_additions(self, session: Session, new_entities: list[Any]) -> set[uuid.UUID]:
        """Process new entities and find affected uncertainties."""
        affected_uncertainties: set[uuid.UUID] = set()
        
        added_edges: set[uuid.UUID] = set()
        added_options: set[Option] = set()
        added_outcomes: set[Outcome] = set()
        
        for new_entity in new_entities:
            if isinstance(new_entity, Edge):
                added_edges.add(new_entity.id)
            elif isinstance(new_entity, Option):
                added_options.add(new_entity)
            elif isinstance(new_entity, Outcome):
                added_outcomes.add(new_entity)
        
        # Find affected uncertainties from additions
        if added_edges:
            affected_uncertainties.update(
                edge_repository.find_effected_uncertainties(session, added_edges)
            )
        
        if added_options:
            affected_uncertainties.update(
                option_repository.find_effected_uncertainties(session, added_options)
            )
        
        if added_outcomes:
            affected_uncertainties.update(
                outcome_repository.find_effected_uncertainties(session, added_outcomes)
            )
        
        return affected_uncertainties
    
    def _has_boundary_change(self, issue: Issue) -> bool:
        """Check if issue boundary changed to/from OUT."""
        history = get_history(issue, Issue.boundary.name)
        if not history.has_changes():
            return False
        return (Boundary.OUT.value in (history.added or []) or 
                Boundary.OUT.value in (history.deleted or []))
    
    def _has_type_change_to_or_from_uncertainty_decision(self, issue: Issue) -> bool:
        """Check if issue type changed to/from UNCERTAINTY or DECISION."""
        history = get_history(issue, Issue.type.name)
        if not history.has_changes():
            return False
        
        relevant_types = {Type.UNCERTAINTY.value, Type.DECISION.value}
        added = set(history.added or [])
        deleted = set(history.deleted or [])
        
        return bool(relevant_types.intersection(added) or relevant_types.intersection(deleted))
    
    def _has_key_change(self, uncertainty: Uncertainty) -> bool:
        """Check if uncertainty key status changed."""
        return get_history(uncertainty, Uncertainty.is_key.name).has_changes()
    
    def _has_focus_type_change(self, decision: Decision) -> bool:
        """Check if decision type changed to/from FOCUS."""
        history = get_history(decision, Decision.type.name)
        if not history.has_changes():
            return False
        return (DecisionHierarchy.FOCUS.value in (history.added or []) or 
                DecisionHierarchy.FOCUS.value in (history.deleted or []))
    
    def recalculate_affected_probabilities(self, session: Session) -> None:
        """Recalculate discrete probability tables for all affected uncertainties."""
        session_info = SessionInfoHandler.get_session_info(session)

        if not session_info.affected_uncertainties:
            return
        
        for uncertainty_id in session_info.affected_uncertainties:
            uncertainty_repository.recalculate_discrete_probability_table(session, uncertainty_id)