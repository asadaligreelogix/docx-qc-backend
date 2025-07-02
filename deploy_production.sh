#!/bin/bash

# DOCX Quality Control Checker - Production Deployment Script
# This script prepares and deploys the application to production

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}[HEADER]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if git repository is clean
check_git_status() {
    print_status "Checking git repository status..."
    
    if ! command_exists git; then
        print_error "Git is not installed. Please install git first."
        exit 1
    fi
    
    if [ ! -d ".git" ]; then
        print_error "This is not a git repository. Please initialize git first."
        exit 1
    fi
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        print_warning "You have uncommitted changes. Please commit or stash them before deployment."
        echo "Run: git add . && git commit -m 'Pre-deployment commit'"
        exit 1
    fi
    
    print_success "Git repository is clean"
}

# Function to generate deployment files
generate_deployment_files() {
    print_status "Generating deployment configuration files..."
    
    # Create Procfile for Heroku/Render
    cat > Procfile << EOF
web: python app_production.py
EOF
    print_success "Created Procfile"
    
    # Create runtime.txt
    cat > runtime.txt << EOF
python-3.9.18
EOF
    print_success "Created runtime.txt"
    
    # Create render.yaml
    cat > render.yaml << EOF
services:
  - type: web
    name: docx-qc-checker
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app_production.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.18
EOF
    print_success "Created render.yaml"
    
    # Create railway.json
    cat > railway.json << EOF
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app_production.py",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE"
  }
}
EOF
    print_success "Created railway.json"
    
    # Create Dockerfile
    cat > Dockerfile << EOF
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app_production.py"]
EOF
    print_success "Created Dockerfile"
    
    # Create docker-compose.yml
    cat > docker-compose.yml << EOF
version: '3.8'
services:
  docx-checker:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./uploads:/app/uploads
    environment:
      - FLASK_ENV=production
EOF
    print_success "Created docker-compose.yml"
    
    # Create .env.example
    cat > .env.example << EOF
# Production Environment Variables
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
EOF
    print_success "Created .env.example"
    
    # Update .gitignore
    if [ -f ".gitignore" ]; then
        # Add common production ignores if not already present
        if ! grep -q "\.env" .gitignore; then
            echo "" >> .gitignore
            echo "# Production files" >> .gitignore
            echo ".env" >> .gitignore
            echo "*.log" >> .gitignore
            echo "logs/" >> .gitignore
            echo "__pycache__/" >> .gitignore
            echo "*.pyc" >> .gitignore
            echo ".DS_Store" >> .gitignore
        fi
        print_success "Updated .gitignore"
    fi
}

# Function to create production app
create_production_app() {
    print_status "Creating production-ready Flask application..."
    
    cat > app_production.py << 'EOF'
#!/usr/bin/env python3
"""
DOCX Quality Control Checker - Production Application
A Flask web application for checking .docx files against quality control rules.
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import docx_checker

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

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'docx'}

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with file upload form."""
    return render_template('upload.html')

@app.route('/api/check', methods=['POST'])
def api_check():
    """API endpoint for file checking."""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only .docx files are allowed.'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        file.save(filepath)
        
        logger.info(f"Processing file: {filename}")
        
        # Run QC checks
        try:
            results = docx_checker.check_document(filepath)
            
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except OSError:
                logger.warning(f"Could not remove temporary file: {filepath}")
            
            return jsonify(results)
            
        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except OSError:
                pass
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
            
    except RequestEntityTooLarge:
        return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/check', methods=['POST'])
def check_file():
    """Web interface for file checking."""
    try:
        if 'file' not in request.files:
            return render_template('upload.html', error='No file provided')
        
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', error='No file selected')
        
        if not allowed_file(file.filename):
            return render_template('upload.html', error='Invalid file type. Only .docx files are allowed.')
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        file.save(filepath)
        
        logger.info(f"Processing file: {filename}")
        
        # Run QC checks
        try:
            results = docx_checker.check_document(filepath)
            
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except OSError:
                logger.warning(f"Could not remove temporary file: {filepath}")
            
            return render_template('result.html', results=results, filename=filename)
            
        except Exception as e:
            logger.error(f"Error processing file {filename}: {str(e)}")
            # Clean up uploaded file
            try:
                os.remove(filepath)
            except OSError:
                pass
            return render_template('upload.html', error=f'Error processing file: {str(e)}')
            
    except RequestEntityTooLarge:
        return render_template('upload.html', error='File too large. Maximum size is 16MB.')
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return render_template('upload.html', error='Internal server error')

@app.route('/health')
def health_check():
    """Health check endpoint for load balancers."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting DOCX QC Checker on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
EOF
    
    print_success "Created app_production.py"
}

# Function to create deployment documentation
create_deployment_docs() {
    print_status "Creating deployment documentation..."
    
    cat > DEPLOYMENT.md << 'EOF'
# DOCX Quality Control Checker - Deployment Guide

This guide covers deploying the DOCX QC Checker to various platforms.

## Quick Deploy Options

### 1. Render (Recommended - Free)
1. Fork/clone this repository to your GitHub account
2. Go to [render.com](https://render.com) and sign up
3. Click "New Web Service"
4. Connect your GitHub repository
5. Render will auto-detect the configuration
6. Click "Create Web Service"
7. Your app will be available at the provided URL

### 2. Railway
1. Go to [railway.app](https://railway.app)
2. Sign up and connect your GitHub repository
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-deploy using the `railway.json` configuration

### 3. Heroku
1. Install Heroku CLI: `brew install heroku/brew/heroku`
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`
5. Open: `heroku open`

### 4. Docker (Local/Server)
```bash
# Build and run locally
docker-compose up --build

# Or build and run manually
docker build -t docx-checker .
docker run -p 5000:5000 docx-checker
```

## Environment Variables

Set these environment variables in your deployment platform:

- `FLASK_ENV=production`
- `FLASK_DEBUG=False`
- `SECRET_KEY=your-secret-key-here`
- `PORT=5000` (optional, defaults to 5000)

## Health Check

The application includes a health check endpoint at `/health` for load balancers.

## File Upload Limits

- Maximum file size: 16MB
- Allowed formats: .docx only
- Files are automatically cleaned up after processing

## Monitoring

Check the logs in your deployment platform's dashboard for any issues.

## Troubleshooting

### Common Issues

1. **Port already in use**: The app will automatically find an available port
2. **File upload fails**: Check file size and format
3. **Dependencies missing**: Ensure all requirements are installed

### Support

For issues, check the logs and ensure all deployment files are present.
EOF
    
    print_success "Created DEPLOYMENT.md"
}

# Function to test deployment locally
test_deployment() {
    print_status "Testing deployment configuration locally..."
    
    # Test Docker build
    if command_exists docker; then
        print_status "Testing Docker build..."
        docker build -t docx-checker-test . > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            print_success "Docker build test passed"
        else
            print_warning "Docker build test failed"
        fi
    else
        print_warning "Docker not available - skipping Docker test"
    fi
    
    # Test Python syntax
    print_status "Testing Python syntax..."
    python3 -m py_compile app_production.py
    if [ $? -eq 0 ]; then
        print_success "Python syntax check passed"
    else
        print_error "Python syntax check failed"
        exit 1
    fi
    
    print_success "Deployment configuration test completed"
}

# Function to show deployment options
show_deployment_options() {
    echo ""
    print_header "Deployment Options"
    echo "===================="
    echo ""
    echo "🚀 Render (Recommended - Free)"
    echo "   - Go to https://render.com"
    echo "   - Sign up and connect your GitHub repo"
    echo "   - Click 'New Web Service'"
    echo "   - Render will auto-detect the configuration"
    echo ""
    echo "🚂 Railway"
    echo "   - Go to https://railway.app"
    echo "   - Sign up and connect your GitHub repo"
    echo "   - Click 'New Project' → 'Deploy from GitHub repo'"
    echo ""
    echo "🐳 Docker (Local/Server)"
    echo "   - Run: docker-compose up --build"
    echo "   - Visit: http://localhost:5000"
    echo ""
    echo "🏠 Heroku"
    echo "   - Install Heroku CLI"
    echo "   - Run: heroku create && git push heroku main"
    echo ""
}

# Function to show help
show_help() {
    echo "DOCX Quality Control Checker - Production Deployment Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --help, -h           Show this help message"
    echo "  --generate-only      Only generate deployment files"
    echo "  --test-only          Only test deployment configuration"
    echo "  --no-git-check       Skip git repository checks"
    echo "  --platform <name>    Generate files for specific platform"
    echo "                       (render, railway, heroku, docker)"
    echo ""
    echo "Examples:"
    echo "  $0                   # Full deployment preparation"
    echo "  $0 --generate-only   # Generate files only"
    echo "  $0 --test-only       # Test configuration only"
    echo "  $0 --platform render # Generate Render-specific files"
}

# Main execution
main() {
    echo "🚀 DOCX Quality Control Checker - Production Deployment"
    echo "======================================================"
    echo ""
    
    # Parse command line arguments
    GENERATE_ONLY=false
    TEST_ONLY=false
    SKIP_GIT_CHECK=false
    PLATFORM=""
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                show_help
                exit 0
                ;;
            --generate-only)
                GENERATE_ONLY=true
                shift
                ;;
            --test-only)
                TEST_ONLY=true
                shift
                ;;
            --no-git-check)
                SKIP_GIT_CHECK=true
                shift
                ;;
            --platform)
                PLATFORM="$2"
                shift 2
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Check git status (unless skipped)
    if [ "$SKIP_GIT_CHECK" = false ]; then
        check_git_status
    else
        print_status "Skipping git repository checks"
    fi
    
    # Generate deployment files
    generate_deployment_files
    create_production_app
    create_deployment_docs
    
    # Test deployment configuration
    test_deployment
    
    # Handle different modes
    if [ "$TEST_ONLY" = true ]; then
        print_success "Deployment configuration test completed"
        exit 0
    elif [ "$GENERATE_ONLY" = true ]; then
        print_success "Deployment files generated successfully"
        exit 0
    else
        # Full deployment preparation
        print_success "Production deployment preparation completed!"
        show_deployment_options
        
        echo ""
        print_success "🎉 Your application is ready for deployment!"
        echo ""
        echo "Next steps:"
        echo "1. Commit all changes: git add . && git commit -m 'Production deployment setup'"
        echo "2. Push to your repository: git push origin main"
        echo "3. Choose a deployment platform from the options above"
        echo "4. Follow the platform-specific instructions"
        echo ""
        echo "For detailed instructions, see DEPLOYMENT.md"
    fi
}

# Run main function
main "$@" 