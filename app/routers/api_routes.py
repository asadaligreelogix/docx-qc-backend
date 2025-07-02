#!/usr/bin/env python3
"""
API routes for programmatic access - converted to FastAPI
"""

import os
import logging
import time
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, UploadFile, File

from app.routers import api_router
from app.services.docx_checker import DocxChecker
from app.utils.file_utils import allowed_file
from app.config import Config
from app.models.schemas import FileCheckResponse, HealthResponse, ErrorResponse

logger = logging.getLogger(__name__)

@api_router.post("/check", response_model=FileCheckResponse)
async def api_check(file: UploadFile = File(...)):
    """API endpoint for file checking."""
    start_time = time.time()
    
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file selected")
        
        if not allowed_file(file.filename):
            raise HTTPException(
                status_code=400, 
                detail="Invalid file type. Only .docx files are allowed."
            )
        
        # Save file temporarily
        filename = file.filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, safe_filename)
        
        # Save uploaded file
        with open(filepath, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"Processing file: {filename}")
        
        # Run QC checks
        try:
            checker = DocxChecker(filepath, Config())
            report = checker.run_all_checks()
            
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except OSError:
                logger.warning(f"Could not remove temporary file: {filepath}")
            
            processing_time = time.time() - start_time
            
            return FileCheckResponse(
                filename=filename,
                report=report.to_dict(),
                processing_time=round(processing_time, 2)
            )
            
        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except OSError:
                pass
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@api_router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for load balancers."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    ) 