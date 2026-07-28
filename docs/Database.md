# Database

## Core Tables
- users, roles, permissions, user_roles, role_permissions
- clients, client_keys
- refresh_tokens
- gateway_routes, service_registry
- audit_logs, rate_limits, api_logs, request_logs

## ER Diagram
```mermaid
erDiagram
  users ||--o{ refresh_tokens : owns
  users ||--o{ user_roles : mapped
  roles ||--o{ user_roles : mapped
  roles ||--o{ role_permissions : grants
  permissions ||--o{ role_permissions : includes
  clients ||--o{ client_keys : has
  clients ||--o{ request_logs : attributed
  users ||--o{ request_logs : attributed
```
