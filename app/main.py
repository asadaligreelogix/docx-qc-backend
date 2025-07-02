#!/usr/bin/env python3
"""
DOCX Quality Control Checker - FastAPI Application
A professional FastAPI application for checking .docx files against quality control rules.
"""

import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import Config
from app.routers import main_router, api_router
from app.utils.error_handlers import register_exception_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting DOCX Quality Control Checker...")
    
    # Ensure required directories exist
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    yield
    
    # Shutdown
    logger.info("Shutting down DOCX Quality Control Checker...")

def create_app(config_class=Config) -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="DOCX Quality Control Checker",
        description="A professional API for checking .docx files against quality control rules",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register exception handlers
    register_exception_handlers(app)
    
    # Include routers
    app.include_router(main_router, tags=["main"])
    app.include_router(api_router, prefix="/api", tags=["api"])
    
    return app

# Create the application instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 