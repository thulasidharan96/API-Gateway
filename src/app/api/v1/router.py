from fastapi import APIRouter

from app.api.v1.admin.routes import router as admin_router
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.client.routes import router as client_api_router
from app.api.v1.clients.routes import router as clients_router
from app.api.v1.developer.routes import router as developer_router
from app.api.v1.gateway.routes import router as gateway_router
from app.api.v1.health.routes import router as health_router
from app.api.v1.users.routes import router as users_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/v1/users", tags=["users"])
api_router.include_router(clients_router, prefix="/v1/clients", tags=["clients"])
api_router.include_router(gateway_router, prefix="/v1/gateway", tags=["gateway"])
api_router.include_router(admin_router, prefix="/v1/admin", tags=["admin"])
api_router.include_router(developer_router, prefix="/v1/developer", tags=["developer"])
api_router.include_router(client_api_router, prefix="/v1/client", tags=["client"])
