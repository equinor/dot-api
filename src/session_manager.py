import uuid

from typing import AsyncGenerator, Optional, Any

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool

from typing import Any
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import get_history

from src.models.base import Base
from src.models import (Edge, Issue, Outcome, Option, DiscreteProbabilityParentOption, DiscreteProbabilityParentOutcome, DiscreteProbability, Uncertainty, Decision)
from src.constants import (Type, DecisionHierarchy, Boundary)
from src.config import config
from src.seed_database import (
    seed_database,
    create_single_project_with_scenario,
    create_decision_tree_symmetry_DT_from_ID,
    create_decision_tree_symmetry_DT,
)
from src.database import (
    DatabaseConnectionStrings,
    get_connection_string_and_token,
    build_connection_url,
    validate_default_scenarios,
)

from src.repositories import option_repository, outcome_repository, edge_repository, uncertainty_repository, issue_repository

class SessionManager:
    """Manages asynchronous DB sessions with connection pooling."""

    def __init__(self) -> None:
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    async def _initialize_in_memory_db(self, db_connection_string: str) -> None:
        """Initialize an in-memory database, and populate with test data."""
        self.engine = create_async_engine(
            db_connection_string,
            poolclass=AsyncAdaptedQueuePool,
            pool_size=config.POOL_SIZE,
            max_overflow=config.MAX_OVERFLOW,
            pool_pre_ping=True,
            pool_recycle=config.POOL_RECYCLE,
            echo=config.DEBUG,
        )
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await seed_database(conn, num_projects=10, num_scenarios=10, num_nodes=50)
            await create_single_project_with_scenario(conn)
            await create_decision_tree_symmetry_DT_from_ID(conn)
            await create_decision_tree_symmetry_DT(conn)

    async def _initialize_persistent_db(self) -> None:
        """Initialize a persistent database."""
        (
            db_connection_string,
            token_dict,
        ) = await get_connection_string_and_token(config.APP_ENV)
        database_url = build_connection_url(db_connection_string, driver="aioodbc")

        if config.APP_ENV == "local":
            self.engine = create_async_engine(
                database_url,
                poolclass=AsyncAdaptedQueuePool,
                pool_size=config.POOL_SIZE,
                pool_timeout=None,
                max_overflow=config.MAX_OVERFLOW,
                pool_pre_ping=True,
                pool_recycle=config.POOL_RECYCLE,
                echo=config.DEBUG,
            )
        else:
            self.engine = create_async_engine(
                database_url,
                poolclass=AsyncAdaptedQueuePool,
                pool_size=config.POOL_SIZE,
                pool_timeout=None,
                max_overflow=config.MAX_OVERFLOW,
                connect_args={"attrs_before": token_dict},
                pool_pre_ping=True,
                pool_recycle=config.POOL_RECYCLE,
                echo=config.DEBUG,
            )

    def _initialize_session_factory(self) -> None:
        """Initialize the session factory."""
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            class_=AsyncSession,
        )

    async def init_db(self) -> None:
        """Initialize the database engine and session factory."""
        db_connection_string = DatabaseConnectionStrings.get_connection_string(config.APP_ENV)

        if ":memory:" in db_connection_string:
            await self._initialize_in_memory_db(db_connection_string)
        else:
            await self._initialize_persistent_db()

        self._initialize_session_factory()

        try:
            await self.run_start_task()
        except Exception:
            # implyes that a different thread is performing the start task
            pass

    async def close(self) -> None:
        """Dispose of the database engine."""
        if self.engine:
            await self.engine.dispose()

    async def run_start_task(self) -> None:
        """Run the database start task."""
        if not self.session_factory:
            raise RuntimeError("Database session factory is not initialized.")

        async for session in self.get_session():
            await validate_default_scenarios(session)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Yield a database session with the correct schema set."""
        if not self.session_factory:
            raise RuntimeError("Database session factory is not initialized.")

        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e


# Global instances
sessionmanager = SessionManager()

@event.listens_for(Session, 'before_flush')
def test_before_flush_event(session: Session, flush_context: Any, instances: Any) -> None:
    print(rf"In {test_before_flush_event.__name__}, session state: deleted: {session.deleted}, new: {session.new}, dirty: {session.dirty}")
    subscribed_entities = (Edge, DiscreteProbabilityParentOption, DiscreteProbabilityParentOutcome, Issue, Decision, Uncertainty)
    if not (session.dirty or session.new or session.deleted):
        return
    
    relevant_new: set[Edge|DiscreteProbabilityParentOption|DiscreteProbabilityParentOutcome|Issue|Decision|Uncertainty] = {obj for obj in session.new if isinstance(obj, subscribed_entities)}
    relevant_dirty: set[Edge|DiscreteProbabilityParentOption|DiscreteProbabilityParentOutcome|Issue|Decision|Uncertainty] = {obj for obj in session.dirty if isinstance(obj, subscribed_entities)}
    relevant_deleted: set[Edge|DiscreteProbabilityParentOption|DiscreteProbabilityParentOutcome]|Issue|Decision|Uncertainty = {obj for obj in session.deleted if isinstance(obj, subscribed_entities)}
    if not (relevant_new or relevant_dirty or relevant_deleted): return
    
    deleted_edges: set[uuid.UUID] = set()

    effected_uncertainties = session.info.get('effected_uncertainties', set())

    issues_to_search: set[uuid.UUID] = set()
    
    for changed_entity in relevant_dirty:
        if isinstance(changed_entity, Issue) and get_history(changed_entity, Issue.boundary.name).has_changes():
            # find effected uncertainties
            insp = get_history(changed_entity, Issue.boundary.name)
            if insp.added == [Boundary.OUT.value] or insp.deleted == [Boundary.OUT.value]:
                issues_to_search.add(changed_entity.id)
            
            insp = get_history(changed_entity, Issue.type.name)
            if insp.added == [Type.UNCERTAINTY.value] or insp.deleted == [Type.UNCERTAINTY.value]:
                effected_uncertainties.add(changed_entity.id)
            if (
                (insp.added == [Type.UNCERTAINTY.value] or insp.deleted == [Type.UNCERTAINTY.value]) or
                (insp.added == [Type.DECISION.value] or insp.deleted == [Type.DECISION.value])
            ):
                issues_to_search.add(changed_entity.id)


        if isinstance(changed_entity, Uncertainty) and get_history(changed_entity, Uncertainty.is_key.name).has_changes():
            # find effected uncertainties
            issues_to_search.add(changed_entity.issue_id)

        if isinstance(changed_entity, Decision) and get_history(changed_entity, Decision.type.name).has_changes():
            # find effected uncertainties
            insp = get_history(changed_entity, Decision.type.name)
            if insp.added == [DecisionHierarchy.FOCUS.value] or insp.deleted == [DecisionHierarchy.FOCUS.value]:
                issues_to_search.add(changed_entity.issue_id)
            
    for deleted_entity in relevant_deleted:
        if isinstance(deleted_entity, Edge):
            deleted_edges.add(deleted_entity.id)

    if issues_to_search:
        effected_uncertainties = effected_uncertainties.union(issue_repository.find_effected_uncertainties(session, issues_to_search))

    if deleted_edges:
        effected_uncertainties = effected_uncertainties.union(edge_repository.find_effected_uncertainties(session, deleted_edges))

    session.info['effected_uncertainties'] = effected_uncertainties

    return

@event.listens_for(Session, 'after_flush')
def test_after_flush_event(session: Session, flush_context: Any) -> None:
    """Log after flush event."""
    print(rf"In {test_after_flush_event.__name__}, session state: deleted: {session.deleted}, new: {session.new}, dirty: {session.dirty}")
    subscribed_entities = (Edge, Outcome, Option, Issue)
    if not (session.dirty or session.new or session.deleted):
        return
    
    relevant_new: set[Edge|Outcome|Option|Issue] = {obj for obj in session.new if isinstance(obj, subscribed_entities)}
    relevant_dirty: set[Edge|Outcome|Option|Issue] = {obj for obj in session.dirty if isinstance(obj, subscribed_entities)}
    relevant_deleted: set[Edge|Outcome|Option|Issue] = {obj for obj in session.deleted if isinstance(obj, subscribed_entities)}
    if not (relevant_new or relevant_dirty or relevant_deleted): return

    added_edges: set[uuid.UUID] = set()
    added_options: set[Option] = set()
    added_outcomes: set[Outcome] = set()

    for created_entity in relevant_new:
        if isinstance(created_entity, Edge): 
            added_edges.add(created_entity.id)
        
        if isinstance(created_entity, Outcome):
            added_outcomes.add(created_entity)
            
        if isinstance(created_entity, Option):
            added_options.add(created_entity)

    effected_uncertainties = session.info.get('effected_uncertainties', set())
    
    if added_edges:
        effected_uncertainties = effected_uncertainties.union(edge_repository.find_effected_uncertainties(session, added_edges))

    if added_options:
        effected_uncertainties = effected_uncertainties.union(option_repository.find_effected_uncertainties(session, added_options))

    if added_outcomes:
        effected_uncertainties = effected_uncertainties.union(outcome_repository.find_effected_uncertainties(session, added_outcomes))

    session.info['effected_uncertainties'] = effected_uncertainties
    return

@event.listens_for(Session, 'before_commit')
def test_before_commit_event(session: Session) -> None:
    """Log before commit event."""
    print(rf"In {test_before_commit_event.__name__}, session state: deleted: {session.deleted}, new: {session.new}, dirty: {session.dirty}")
    effected_uncertainties = session.info.get('effected_uncertainties', None)
    if effected_uncertainties is None: return 
    if effected_uncertainties:
        [uncertainty_repository.recalculate_discrete_probability_table(session, x) for x in effected_uncertainties]
    return

@event.listens_for(Session, 'after_commit')
def test_after_commit_event(session: Session) -> None:
    """Log after commit event."""
    print(rf"In {test_after_commit_event.__name__}, session state: deleted: {session.deleted}, new: {session.new}, dirty: {session.dirty}")
    return

