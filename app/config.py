#!/usr/bin/env python3
"""
Configuration management for DOCX Quality Control Checker
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'docx'}
    
    # FastAPI configuration
    APP_ENV = os.environ.get('APP_ENV', 'development')
    DEBUG = os.environ.get('APP_DEBUG', 'False').lower() == 'true'
    
    # File upload settings
    UPLOAD_TIMEOUT = timedelta(minutes=5)
    
    # QC Rules constants
    REQUIRED_FONT = "Times New Roman"
    NORMAL_FONT_SIZE = 12
    TABLE_FONT_SIZE = 9
    REQUIRED_MARGIN = 1.0  # inches
    MIN_MARGIN = 0.75  # inches
    MIN_HEADER_FOOTER_DISTANCE = 0.38  # inches
    
    # Enhanced QC settings
    MARGIN_TOLERANCE = 0.01  # inches - tolerance for margin checks
    FONT_VARIANTS = ['times new roman', 'times', 'timesnewroman', 'times new roman,serif']
    
    # Hyperlink validation settings
    EXTERNAL_LINK_TIMEOUT = 10  # seconds
    EXTERNAL_LINK_MAX_REDIRECTS = 5
    EXTERNAL_LINK_USER_AGENT = 'DOCX-QC-Checker/1.0'
    
    # Acronym management - now using comprehensive database
    # The acronym database is loaded from app/utils/acronym_database.py
    # This provides professional acronym management with extensive coverage
    
    # Verb tense patterns for consistency checking
    PRESENT_TENSE_INDICATORS = ['is', 'are', 'has', 'have', 'does', 'do', 'goes', 'go', 'runs', 'run', 'works', 'work']
    PAST_TENSE_INDICATORS = ['was', 'were', 'had', 'did', 'went', 'came', 'made', 'ran', 'worked', 'went']
    FUTURE_TENSE_INDICATORS = ['will', 'shall', 'going to', 'gonna', 'about to']
    
    # Enhanced acronym definition patterns
    ACRONYM_PATTERNS = [
        r'([A-Z]{2,})\s*\(([^)]+)\)',  # API (Application Programming Interface)
        r'([^)]+)\s*\(([A-Z]{2,})\)',  # Application Programming Interface (API)
        r'([A-Z]{2,})\s*[-–]\s*([^.]*)',  # API - Application Programming Interface
        r'([A-Z]{2,})\s*stands for\s*([^.]*)',  # API stands for Application Programming Interface
        r'([A-Z]{2,})\s*means\s*([^.]*)',  # API means Application Programming Interface
        r'([A-Z]{2,})\s*refers to\s*([^.]*)',  # API refers to Application Programming Interface
        r'([A-Z]{2,})\s*is\s*([^.]*)',  # API is Application Programming Interface
        r'([A-Z]{2,})\s*denotes\s*([^.]*)',  # API denotes Application Programming Interface
        r'([A-Z]{2,})\s*represents\s*([^.]*)',  # API represents Application Programming Interface
        r'([A-Z]{2,})\s*abbreviation for\s*([^.]*)',  # API abbreviation for Application Programming Interface
        r'([A-Z]{2,})\s*short for\s*([^.]*)',  # API short for Application Programming Interface
        r'([A-Z]{2,})\s*abbreviated as\s*([^.]*)',  # API abbreviated as Application Programming Interface
    ]
    
    # TOC detection patterns
    TOC_PATTERNS = [
        r'table of contents',
        r'contents',
        r'toc',
        r'index',
        r'outline'
    ]
    
    # Internal link patterns
    INTERNAL_LINK_PATTERNS = [
        r'figure\s+\d+\.?\d*',
        r'table\s+\d+\.?\d*',
        r'section\s+\d+\.?\d*',
        r'chapter\s+\d+\.?\d*',
        r'page\s+\d+',
        r'see\s+section\s+\d+\.?\d*',
        r'refer\s+to\s+figure\s+\d+\.?\d*'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    APP_ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    APP_ENV = 'production'
    
    # Production-specific settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        SECRET_KEY = 'dev-secret-key-change-in-production'  # Fallback for testing

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Testing-specific settings
    EXTERNAL_LINK_TIMEOUT = 5  # Faster timeout for tests

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 