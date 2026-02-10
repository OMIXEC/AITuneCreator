#!/bin/bash

# AITuneCreator Setup Script
# This script automates the environment setup for development

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

# Functions
print_header() {
    echo -e "${BLUE}==== $1 ====${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check Python version
check_python() {
    print_header "Checking Python Installation"

    if ! command -v python3.11 &> /dev/null; then
        if ! command -v python3 &> /dev/null; then
            print_error "Python 3.11+ is required but not installed"
            exit 1
        fi
        PYTHON_CMD="python3"
        PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
        print_warning "Using $PYTHON_CMD (version $PYTHON_VERSION). Python 3.11+ recommended."
    else
        PYTHON_CMD="python3.11"
        print_success "Found Python 3.11"
    fi
}

# Create virtual environment
setup_venv() {
    print_header "Setting Up Virtual Environment"

    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists. Skipping creation."
    else
        print_warning "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    fi

    # Activate venv
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        print_success "Virtual environment activated"
    else
        print_error "Failed to activate virtual environment"
        exit 1
    fi
}

# Upgrade pip
upgrade_pip() {
    print_header "Upgrading pip"
    pip install --upgrade pip --quiet
    print_success "pip upgraded"
}

# Install dependencies
install_dependencies() {
    print_header "Installing Dependencies"

    if ! pip install -e . --quiet; then
        print_error "Failed to install dependencies"
        exit 1
    fi

    print_success "Dependencies installed"
}

# Setup environment files
setup_env_files() {
    print_header "Setting Up Environment Files"

    if [ ! -f ".env.example" ]; then
        print_error ".env.example not found"
        exit 1
    fi

    # Check which environments to create
    echo ""
    echo "Which environments do you want to set up?"
    echo "1. Development (.env.dev) - Local development"
    echo "2. Testing (.env.test) - Testing and CI/CD"
    echo "3. Production (.env.prod) - Production deployment"
    echo "4. All of the above"
    echo "5. Skip (I'll do it manually)"
    echo ""

    read -p "Enter choice [1-5]: " choice

    case $choice in
        1|4)
            if [ ! -f ".env.dev" ]; then
                cp .env.example .env.dev
                print_success ".env.dev created from .env.example"
                echo ""
                print_warning "Please edit .env.dev and add your GROQ_API_KEY"
                echo "Get your key from: https://console.groq.com"
            else
                print_warning ".env.dev already exists"
            fi
            ;;
    esac

    case $choice in
        2|4)
            if [ ! -f ".env.test" ]; then
                cp .env.example .env.test
                # Pre-fill test values
                sed -i 's/ENVIRONMENT=dev/ENVIRONMENT=test/' .env.test
                sed -i 's/STREAMLIT_SERVER_PORT=8501/STREAMLIT_SERVER_PORT=8502/' .env.test
                sed -i 's/LOG_LEVEL=DEBUG/LOG_LEVEL=INFO/' .env.test
                sed -i 's/ENABLE_CACHING=false/ENABLE_CACHING=true/' .env.test
                print_success ".env.test created with test defaults"
                echo ""
                print_warning "Add a test GROQ_API_KEY to .env.test (can be a dummy value)"
            else
                print_warning ".env.test already exists"
            fi
            ;;
    esac

    case $choice in
        3|4)
            if [ ! -f ".env.prod" ]; then
                cp .env.example .env.prod
                # Pre-fill prod values
                sed -i 's/ENVIRONMENT=dev/ENVIRONMENT=prod/' .env.prod
                sed -i 's/LOG_LEVEL=DEBUG/LOG_LEVEL=WARNING/' .env.prod
                sed -i 's/ENABLE_CACHING=false/ENABLE_CACHING=true/' .env.prod
                print_success ".env.prod created with prod defaults"
                echo ""
                print_warning "Configure .env.prod on the production server only!"
            else
                print_warning ".env.prod already exists"
            fi
            ;;
    esac
}

# Verify installation
verify_installation() {
    print_header "Verifying Installation"

    echo "Checking Python imports..."
    python -c "
import sys
modules = ['streamlit', 'langchain', 'groq', 'music21']
missing = []
for module in modules:
    try:
        __import__(module)
        print(f'  ✓ {module}')
    except ImportError:
        print(f'  ✗ {module}')
        missing.append(module)

if missing:
    print(f'\nMissing: {', '.join(missing)}')
    sys.exit(1)
" || exit 1

    print_success "All critical dependencies found"
}

# Provide next steps
print_next_steps() {
    print_header "Setup Complete!"
    echo ""
    echo "Next steps:"
    echo "1. Edit your .env files with appropriate API keys:"
    echo "   ${YELLOW}.env.dev${NC} - Your development Groq API key"
    echo "   ${YELLOW}.env.test${NC} - Test API key (can be dummy)"
    echo "   ${YELLOW}.env.prod${NC} - Configure on production server"
    echo ""
    echo "2. Run the application:"
    echo "   ${YELLOW}export ENV=dev${NC}"
    echo "   ${YELLOW}streamlit run app.py${NC}"
    echo ""
    echo "3. Visit: ${BLUE}http://localhost:8501${NC}"
    echo ""
    echo "For more information, see:"
    echo "  - DEVELOPER_GUIDE.md (Quick reference)"
    echo "  - CLAUDE.md (Detailed technical guide)"
    echo ""
}

# Main execution
main() {
    clear
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║   AITuneCreator Developer Setup       ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""

    check_python
    setup_venv
    upgrade_pip
    install_dependencies
    verify_installation
    setup_env_files
    print_next_steps
}

# Run main function
main
