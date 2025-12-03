import uuid

from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import get_history

from src.models import (
    Edge, Issue, Outcome, Option, Utility, Decision,
    DiscreteUtility, DiscreteUtilityParentOption, DiscreteUtilityParentOutcome,
)
from src.constants import (Type, DecisionHierarchy, Boundary)

from src.repositories import option_repository, outcome_repository, edge_repository, utility_repository, issue_repository
from src.utils.session_info_handler import SessionInfoHandler

class DiscreteUtilityEventHandler:
    """Handles events that require discrete utility table recalculation."""

    subscribed_entities_delete = [Edge, DiscreteUtilityParentOption, DiscreteUtilityParentOutcome]
    subscribed_entities_modified = [Issue, Utility, Decision]
    subscribed_entities_new = [Edge, Option, Outcome]

    def process_session_changes_before_flush(self, session: Session) -> None:
        """Process all session changes and determine which utilities need recalculation."""
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
        session_info.affected_utilities.update(self._process_deletions(session, subscribed_deleted))
        session_info.affected_utilities.update(self._process_modifications(session, subscribed_dirty))
        
        SessionInfoHandler.update_session_info(session, session_info)

    def process_session_changes_after_flush(self, session: Session) -> None:
        """Process all session changes and determine which utilities need recalculation."""
        # Filter to only subscribed entities
        subscribed_new = [
            entity for entity in session.new 
            if any(isinstance(entity, entity_type) for entity_type in self.subscribed_entities_new)
        ]
        
        if not subscribed_new:
            return
        
        session_info = SessionInfoHandler.get_session_info(session)
        
        # Process changes in order of dependency
        session_info.affected_utilities.update(self._process_additions(session, subscribed_new))
        
        SessionInfoHandler.update_session_info(session, session_info)
    
    def _process_deletions(self, session: Session, deleted_entities: list[Any]) -> set[uuid.UUID]:
        """Process deleted entities and find affected utilities."""
        affected_utilities: set[uuid.UUID] = set()

        discrete_utilities_to_delete: set[uuid.UUID] = set()
        for deleted_entity in deleted_entities:
            if isinstance(deleted_entity, Edge):
                affected_utilities.update(
                    edge_repository.find_effected_utilities(session, {deleted_entity.id})
                )
            if isinstance(deleted_entity, DiscreteUtilityParentOutcome) or isinstance(deleted_entity, DiscreteUtilityParentOption):
                discrete_utilities_to_delete.add(deleted_entity.discrete_utility_id)
        
        if discrete_utilities_to_delete:
            session.execute(
                DiscreteUtilityParentOutcome.__table__.delete()
                .where(DiscreteUtilityParentOutcome.discrete_utility_id.in_(discrete_utilities_to_delete))
            )

            # Then delete all parent option relationships
            session.execute(
                DiscreteUtilityParentOption.__table__.delete()
                .where(DiscreteUtilityParentOption.discrete_utility_id.in_(discrete_utilities_to_delete))
            )

            # Finally delete the DiscreteUtility record itself
            session.execute(
                DiscreteUtility.__table__.delete()
                .where(DiscreteUtility.id.in_(discrete_utilities_to_delete))
            )

            
        
        return affected_utilities
    
    def _process_modifications(self, session: Session, modified_entities: list[Any]) -> set[uuid.UUID]:
        """Process modified entities and find affected utilities."""
        affected_utilities: set[uuid.UUID] = set()
        issues_to_search: set[uuid.UUID] = set()
        
        for modified_entity in modified_entities:
            if isinstance(modified_entity, Issue):
                if self._has_boundary_change(modified_entity):
                    issues_to_search.add(modified_entity.id)
                
                if self._has_type_change_to_or_from_utility_decision(modified_entity):
                    affected_utilities.add(modified_entity.id)
                    issues_to_search.add(modified_entity.id)
            
            elif isinstance(modified_entity, Utility):
                # Track changes to utility that might affect grid structure
                issues_to_search.add(modified_entity.issue_id)
            
            elif isinstance(modified_entity, Decision):
                if self._has_focus_type_change(modified_entity):
                    issues_to_search.add(modified_entity.issue_id)
        
        # Find affected utilities from issue changes
        if issues_to_search:
            affected_utilities.update(
                issue_repository.find_effected_utilities(session, issues_to_search)
            )
        
        return affected_utilities
    
    def _process_additions(self, session: Session, new_entities: list[Any]) -> set[uuid.UUID]:
        """Process new entities and find affected utilities."""
        affected_utilities: set[uuid.UUID] = set()
        
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
        
        # Find affected utilities from additions
        if added_edges:
            affected_utilities.update(
                edge_repository.find_effected_utilities(session, added_edges)
            )
        
        if added_options:
            affected_utilities.update(
                option_repository.find_effected_utilities(session, added_options)
            )
        
        if added_outcomes:
            affected_utilities.update(
                outcome_repository.find_effected_utilities(session, added_outcomes)
            )
        
        return affected_utilities
    
    def _has_boundary_change(self, issue: Issue) -> bool:
        """Check if issue boundary changed to/from OUT."""
        history = get_history(issue, Issue.boundary.name)
        if not history.has_changes():
            return False
        return (Boundary.OUT.value in (history.added or []) or 
                Boundary.OUT.value in (history.deleted or []))
    
    def _has_type_change_to_or_from_utility_decision(self, issue: Issue) -> bool:
        """Check if issue type changed to/from UTILITY or DECISION."""
        history = get_history(issue, Issue.type.name)
        if not history.has_changes():
            return False
        
        relevant_types = {Type.UTILITY.value, Type.DECISION.value}
        added = set(history.added or [])
        deleted = set(history.deleted or [])
        
        return bool(relevant_types.intersection(added) or relevant_types.intersection(deleted))
    
    def _has_focus_type_change(self, decision: Decision) -> bool:
        """Check if decision type changed to/from FOCUS."""
        history = get_history(decision, Decision.type.name)
        if not history.has_changes():
            return False
        return (DecisionHierarchy.FOCUS.value in (history.added or []) or 
                DecisionHierarchy.FOCUS.value in (history.deleted or []))
    
    def recalculate_affected_utilities(self, session: Session) -> None:
        """Recalculate discrete utility tables for all affected utilities."""
        session_info = SessionInfoHandler.get_session_info(session)

        if not session_info.affected_utilities:
            return
        
        for utility_id in session_info.affected_utilities:
            utility_repository.recalculate_discrete_utility_table(session, utility_id)
