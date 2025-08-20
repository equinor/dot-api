# dot-api

## Architecture and Guidelines
This API follows a service/repositories pattern. The main components are entities (SQLAlchemy declarative base) and Data Transfer Objects (DTOs, Pydantic classes). Here are some guidelines:

1. Each entity should have a dedicated repository to manage SQL queries using SQLAlchemy.
1. Repositories should handle entities or related parameters as both input and output.
1. Services are responsible for coordinating interactions between repositories.
1. Services should accept incoming DTOs as input and return outgoing DTOs.
1. Routes should primarily call a series of services and contain minimal logic.
1. Each entity should have one or more DTOs representing versions that can be processed in the code.
1. Transformation between entities and DTOs should be managed by a DTO mapper specific to each entity.

## Get Started

### Add Secrets

The secrets for this application are managed as environment variables. To add secrets locally, follow these steps:

1. Create a `.env` file in the root of this repository.
2. Add your secrets to the file. For example:
   ```
   CLIENT_SECRET=your_key
   ```

Environment variables used can be found in ``src/config.py``

## Alembic

### Usefull commands

- Create migration: ``alembic revision --autogenerate -m "Create a baseline migrations"``
- Display the current revision for a database: ``alembic current``
- View migrations history: ``alembic history --verbose``
- Revert all migrations: ``alembic downgrade base``
- Apply all migrations:``alembic upgrade head``
- Revert migrations one by one: ``alembic downgrade -1``
- Apply migrations one by one: ``alembic upgrade +1``
- Display all raw SQL: ``alembic upgrade head --sql``
- Reset the database: ``alembic downgrade base && alembic upgrade head``