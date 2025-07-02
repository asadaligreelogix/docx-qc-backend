#!/bin/bash

# DOCX Quality Control Checker - Local Development Script
# This script sets up and runs the application locally

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    print_status "Checking Python version..."
    
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_error "Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
        exit 1
    fi
    
    print_success "Python $PYTHON_VERSION is compatible"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    if [ -f requirements.txt ]; then
        python3 -m pip install --user -r requirements.txt
        print_success "Dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Function to create necessary directories
setup_directories() {
    print_status "Setting up project directories..."
    
    # Create uploads directory if it doesn't exist
    if [ ! -d "uploads" ]; then
        mkdir -p uploads
        print_success "Created uploads directory"
    fi
    
    # Create logs directory if it doesn't exist
    if [ ! -d "logs" ]; then
        mkdir -p logs
        print_success "Created logs directory"
    fi
    
    # Set proper permissions
    chmod 755 uploads
    chmod 755 logs
    print_success "Directory permissions set"
}

# Function to generate test file
generate_test_file() {
    print_status "Generating test file with all QC violations..."
    
    if [ -f "make_test_all_violations.py" ]; then
        python3 make_test_all_violations.py
        if [ -f "test_all_violations.docx" ]; then
            print_success "Test file generated: test_all_violations.docx"
        else
            print_warning "Test file generation may have failed"
        fi
    else
        print_warning "Test file generator not found"
    fi
}

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is available
    fi
}

# Function to find available port
find_available_port() {
    local port=5000
    while check_port $port; do
        port=$((port + 1))
    done
    echo $port
}

# Function to run the application
run_application() {
    print_status "Starting the application..."
    
    # Check if port 5000 is available
    if check_port 5000; then
        print_warning "Port 5000 is in use. Finding alternative port..."
        PORT=$(find_available_port)
        print_status "Using port $PORT"
        export FLASK_APP=run.py
        export FLASK_ENV=development
        export FLASK_PORT=$PORT
        python3 run.py
    else
        print_status "Using default port 5000"
        export FLASK_APP=run.py
        export FLASK_ENV=development
        export FLASK_PORT=5000
        python3 run.py
    fi
}

# Function to run tests
run_tests() {
    print_status "Running application tests..."
    
    if [ -f "test_all_violations.docx" ]; then
        print_status "Testing with sample file..."
        python3 cli.py test_all_violations.docx
        print_success "Test completed"
    else
        print_warning "No test file found. Run with --generate-test first."
    fi
}

# Function to show help
show_help() {
    echo "DOCX Quality Control Checker - Local Development Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --help, -h           Show this help message"
    echo "  --setup-only         Only setup the environment (don't run app)"
    echo "  --test-only          Only run tests (don't start app)"
    echo "  --generate-test      Generate test file and exit"
    echo "  --no-deps            Skip dependency installation"
    echo "  --no-test-file       Skip test file generation"
    echo ""
    echo "Examples:"
    echo "  $0                   # Full setup and run"
    echo "  $0 --setup-only      # Setup only"
    echo "  $0 --test-only       # Run tests only"
    echo "  $0 --generate-test   # Generate test file only"
}

# Main execution
main() {
    echo "🚀 DOCX Quality Control Checker - Local Development"
    echo "=================================================="
    echo ""
    
    # Parse command line arguments
    SETUP_ONLY=false
    TEST_ONLY=false
    GENERATE_TEST=false
    SKIP_DEPS=false
    SKIP_TEST_FILE=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                show_help
                exit 0
                ;;
            --setup-only)
                SETUP_ONLY=true
                shift
                ;;
            --test-only)
                TEST_ONLY=true
                shift
                ;;
            --generate-test)
                GENERATE_TEST=true
                shift
                ;;
            --no-deps)
                SKIP_DEPS=true
                shift
                ;;
            --no-test-file)
                SKIP_TEST_FILE=true
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Check Python version
    check_python_version
    
    # Install dependencies (unless skipped)
    if [ "$SKIP_DEPS" = false ]; then
        install_dependencies
    else
        print_status "Skipping dependency installation"
    fi
    
    # Setup directories
    setup_directories
    
    # Generate test file (unless skipped)
    if [ "$SKIP_TEST_FILE" = false ]; then
        generate_test_file
    else
        print_status "Skipping test file generation"
    fi
    
    # Handle different modes
    if [ "$GENERATE_TEST" = true ]; then
        print_success "Test file generation completed"
        exit 0
    elif [ "$TEST_ONLY" = true ]; then
        run_tests
        print_success "Tests completed"
        exit 0
    elif [ "$SETUP_ONLY" = true ]; then
        print_success "Setup completed successfully"
        echo ""
        echo "🎉 Your environment is ready!"
        echo "To start the application, run: $0"
        echo "To run tests only: $0 --test-only"
        exit 0
    else
        # Full run mode
        echo ""
        print_status "Starting application..."
        
        # Determine the port that will be used
        if check_port 5000; then
            PORT=$(find_available_port)
            print_warning "Port 5000 is in use. Will use port $PORT"
        else
            PORT=5000
        fi
        
        echo "📱 Web interface will be available at: http://localhost:$PORT"
        echo "🔧 API endpoint: http://localhost:$PORT/api/check"
        echo "📁 Upload test file: test_all_violations.docx"
        echo ""
        echo "Press Ctrl+C to stop the server"
        echo ""
        
        run_application
    fi
}

# Run main function
main "$@" 