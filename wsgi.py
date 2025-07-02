#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

from app.main import app

# For WSGI servers like Gunicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 