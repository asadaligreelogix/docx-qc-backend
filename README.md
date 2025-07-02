# DOCX Quality Control Checker - FastAPI

A professional FastAPI application for checking .docx files against quality control rules.

## Features

- **FastAPI Backend**: Modern, fast, and type-safe API
- **File Upload**: Upload .docx files for quality control checking
- **Comprehensive QC Rules**: Extensive quality control checks for documents
- **JSON API**: All endpoints return structured JSON responses
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Health Checks**: Built-in health monitoring
- **API Documentation**: Automatic OpenAPI/Swagger documentation

## Quick Start

### Using Docker (Recommended)

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Access the application:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/api/health

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python run.py
   ```

3. **Or use uvicorn directly:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Main Endpoints

- `GET /` - API documentation and endpoint information
- `POST /check` - Upload and check a .docx file

### API Endpoints

- `POST /api/check` - Programmatic file checking endpoint
- `GET /api/health` - Health check endpoint

### File Upload

All file upload endpoints accept multipart/form-data with a field named `file` containing a .docx file.

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/api/check" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_document.docx"
```

## Response Format

All endpoints return JSON responses. File check responses include:

```json
{
  "filename": "document.docx",
  "report": {
    "document_path": "/path/to/document.docx",
    "timestamp": "2024-01-01T12:00:00",
    "summary": {
      "total_checks": 25,
      "passed_checks": 23,
      "failed_checks": 2,
      "errors": 1,
      "warnings": 1,
      "success_rate": 92.0,
      "overall_status": "FAIL",
      "severity": "ERROR"
    },
    "checks": [
      {
        "rule_name": "Font Check",
        "rule_number": 1,
        "passed": true,
        "message": "All text uses Times New Roman font",
        "violation_type": "success",
        "details": null,
        "locations": []
      }
    ]
  },
  "processing_time": 2.34
}
```

## Configuration

Environment variables:

- `APP_ENV`: Application environment (development/production)
- `APP_DEBUG`: Enable debug mode (true/false)
- `SECRET_KEY`: Secret key for the application
- `APP_PORT`: Port to run the application on (default: 8000)

## Docker Configuration

The application includes:

- **Dockerfile**: Multi-stage build with Python 3.11
- **docker-compose.yml**: Production-ready setup with health checks
- **.dockerignore**: Optimized build context

### Docker Compose Services

- `app`: Main FastAPI application
- `postgres`: PostgreSQL database (commented out, uncomment if needed)

## CLI Usage

For command-line usage:

```bash
python cli.py path/to/document.docx
python cli.py path/to/document.docx --json
```

## Development

### Project Structure

```
app/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── models/              # Pydantic models and schemas
│   ├── qc_result.py     # QC result data models
│   └── schemas.py       # Request/response schemas
├── routers/             # FastAPI route handlers
│   ├── main_routes.py   # Main web routes
│   └── api_routes.py    # API routes
├── services/            # Business logic
│   └── docx_checker.py  # DOCX checking service
└── utils/               # Utility functions
    ├── acronym_database.py
    ├── error_handlers.py
    └── file_utils.py
```

### Adding New Endpoints

1. Create a new route file in `app/routers/`
2. Define Pydantic schemas in `app/models/schemas.py`
3. Register the router in `app/main.py`

## Migration from Flask

This application was converted from Flask to FastAPI. Key changes:

- ✅ Removed all HTML templates and `render_template` calls
- ✅ Converted Flask routes to FastAPI endpoints
- ✅ Added Pydantic models for request/response validation
- ✅ Replaced Flask blueprints with FastAPI routers
- ✅ Updated error handling for FastAPI
- ✅ Added automatic API documentation
- ✅ Updated Docker configuration for FastAPI

## License

[Add your license information here] 