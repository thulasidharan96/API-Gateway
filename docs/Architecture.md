# Architecture

## Bounded Contexts
- Auth Service
- Gateway Service
- Client Management
- Admin APIs
- Developer APIs
- Analytics and Audit
- Service Registry

## Layers
- API Layer (`app/api`)
- Application/Service Layer (`app/services`)
- Domain/Data Access Layer (`app/db/models`, `app/db/repositories`)
- Infrastructure/Cross-cutting (`app/core`, `app/middleware`, `app/workers`)

## Patterns
- Repository Pattern
- Service Layer
- Dependency Injection
- Factory/Strategy extension points for gateway policies
