from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, registration, accounts

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
# api_router.include_router(clients.router, prefix="/clients", tags=["Clients"])
api_router.include_router(registration.router, prefix="/registration", tags=["Register"])
api_router.include_router(accounts.router, prefix="/account", tags=["Account"])
# Aquí añadirás los routers de accounts, transactions, etc.