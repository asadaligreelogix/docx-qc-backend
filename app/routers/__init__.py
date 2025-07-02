# Routers package
from fastapi import APIRouter

# Create routers
main_router = APIRouter()
api_router = APIRouter()

# Import routes to register them
from . import main_routes, api_routes 