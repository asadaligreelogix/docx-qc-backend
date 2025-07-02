#!/usr/bin/env python3
"""
Main routes for web interface - converted to FastAPI
"""

import os
import logging
import time
from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse

from app.routers import main_router
from app.services.docx_checker import DocxChecker
from app.utils.file_utils import allowed_file
from app.config import Config
from app.models.schemas import FileUploadResponse, FileCheckResponse, ErrorResponse

logger = logging.getLogger(__name__)

@main_router.get("/", response_model=Dict[str, Any])
async def index():
    """Main page - returns API documentation instead of HTML form."""
    return {
        "message": "DOCX Quality Control Checker API",
        "description": "Upload a .docx file to check it against quality control rules",
        "endpoints": {
            "upload_form": {
                "url": "/check",
                "method": "POST",
                "description": "Upload a .docx file for quality control checking",
                "content_type": "multipart/form-data",
                "field_name": "file",
                "requirements": {
                    "file_type": ".docx only",
                    "max_size": "16MB",
                    "response_format": "JSON with QC report"
                }
            },
            "api_endpoint": {
                "url": "/api/check",
                "method": "POST", 
                "description": "API endpoint for programmatic file checking",
                "content_type": "multipart/form-data",
                "field_name": "file"
            },
            "health_check": {
                "url": "/api/health",
                "method": "GET",
                "description": "Health check endpoint"
            }
        },
        "documentation": "/docs",
        "version": "1.0.0"
    }

@main_router.post("/check", response_model=FileCheckResponse)
async def check_file(file: UploadFile = File(...)):
    """Web interface for file checking - now returns JSON instead of HTML."""
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