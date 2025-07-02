#!/usr/bin/env python3
"""
Pydantic schemas for request and response validation
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class FileUploadResponse(BaseModel):
    """Response schema for file upload endpoint"""
    message: str = Field(..., description="Success message")
    filename: str = Field(..., description="Name of the uploaded file")
    file_size: Optional[int] = Field(None, description="Size of the uploaded file in bytes")
    upload_timestamp: datetime = Field(..., description="Timestamp when file was uploaded")

class HealthResponse(BaseModel):
    """Response schema for health check endpoint"""
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    uptime: Optional[float] = Field(None, description="Application uptime in seconds")

class ErrorResponse(BaseModel):
    """Response schema for error responses"""
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    timestamp: datetime = Field(..., description="Timestamp when error occurred")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")

class FileCheckRequest(BaseModel):
    """Request schema for file checking endpoint"""
    # This is a placeholder for the file upload form
    # In FastAPI, file uploads are handled via FormData, not JSON
    # This schema documents what the frontend should send
    description: str = Field(
        default="Upload a .docx file using multipart/form-data with field name 'file'",
        description="Instructions for file upload"
    )
    file_requirements: Dict[str, Any] = Field(
        default={
            "field_name": "file",
            "content_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "max_size_mb": 16,
            "allowed_extensions": [".docx"]
        },
        description="File upload requirements"
    )

class QCResultSchema(BaseModel):
    """Pydantic schema for QC result"""
    rule_name: str = Field(..., description="Name of the QC rule")
    rule_number: Optional[int] = Field(None, description="Rule number")
    passed: bool = Field(..., description="Whether the check passed")
    message: str = Field(..., description="Result message")
    violation_type: str = Field(..., description="Type of violation (error, warning, info, success)")
    details: Optional[str] = Field(None, description="Additional details")
    locations: Optional[List[Dict[str, Any]]] = Field(None, description="Violation locations")

class QCReportSchema(BaseModel):
    """Pydantic schema for QC report"""
    document_path: str = Field(..., description="Path to the checked document")
    timestamp: datetime = Field(..., description="When the check was performed")
    summary: Dict[str, Any] = Field(..., description="Summary statistics")
    checks: List[QCResultSchema] = Field(..., description="List of QC results")

class FileCheckResponse(BaseModel):
    """Response schema for file checking endpoint"""
    filename: str = Field(..., description="Name of the checked file")
    report: QCReportSchema = Field(..., description="QC report")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds") 