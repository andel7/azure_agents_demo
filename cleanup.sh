#!/bin/bash

# AI Tour 2025 - Cleanup Automation Wrapper Script
# This script provides easy access to the cleanup automation functionality

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if virtual environment exists
check_venv() {
    if [ ! -d "$SCRIPT_DIR/.venv" ]; then
        print_warning "Virtual environment not found at $SCRIPT_DIR/.venv"
        print_info "Creating virtual environment..."
        python3 -m venv "$SCRIPT_DIR/.venv"
        
        print_info "Activating virtual environment and installing dependencies..."
        source "$SCRIPT_DIR/.venv/bin/activate"
        pip install -r "$SCRIPT_DIR/requirements.txt"
        print_success "Virtual environment setup complete!"
    fi
}

# Function to activate virtual environment
activate_venv() {
    if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
        source "$SCRIPT_DIR/.venv/bin/activate"
        print_success "Virtual environment activated"
    else
        print_error "Virtual environment activation script not found"
        exit 1
    fi
}

# Function to check environment variables
check_env() {
    if [ ! -f "$SCRIPT_DIR/.env" ]; then
        print_error "Environment file (.env) not found!"
        print_info "Please create a .env file with your PROJECT_CONNECTION_STRING"
        exit 1
    fi
    
    # Check if PROJECT_CONNECTION_STRING exists in .env
    if ! grep -q "PROJECT_CONNECTION_STRING" "$SCRIPT_DIR/.env"; then
        print_error "PROJECT_CONNECTION_STRING not found in .env file!"
        print_info "Please add your Azure AI Project connection string to .env"
        exit 1
    fi
}

# Function to display help
show_help() {
    echo "AI Tour 2025 - Cleanup Automation"
    echo "=================================="
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  --agents                Delete all agents"
    echo "  --threads [id1] [id2]   Delete specific threads by ID (or all if no IDs)"
    echo "  --all-threads           Delete all threads"
    echo "  --full                  Full cleanup (agents + threads)"
    echo "  --session <file>        Cleanup from session tracking file"
    echo "  --list                  List current resources without deleting"
    echo "  --confirm               Skip confirmation prompts"
    echo "  --interactive           Run in interactive mode (default)"
    echo "  --help                  Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Interactive mode"
    echo "  $0 --list                            # List all resources"
    echo "  $0 --agents                          # Delete all agents (with confirmation)"
    echo "  $0 --agents --confirm                # Delete all agents (no confirmation)"
    echo "  $0 --all-threads                     # Delete all threads"
    echo "  $0 --threads                         # Delete all threads (same as --all-threads)"
    echo "  $0 --threads thread_id_1 thread_id_2 # Delete specific threads"
    echo "  $0 --session session_tracking.json  # Cleanup from session file"
    echo "  $0 --full                            # Complete cleanup"
    echo ""
}

# Main function
main() {
    print_info "AI Tour 2025 - Cleanup Automation Wrapper"
    
    # Check and setup environment
    check_venv
    activate_venv
    check_env
    
    # Change to script directory
    cd "$SCRIPT_DIR"
    
    # Parse arguments and run cleanup
    if [ $# -eq 0 ]; then
        # No arguments - run interactive mode
        python3 cleanup_automation.py
    elif [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_help
    elif [ "$1" = "--list" ]; then
        python3 cleanup_automation.py --list-only
    elif [ "$1" = "--agents" ]; then
        if [ "$2" = "--confirm" ]; then
            python3 cleanup_automation.py --agents --confirm
        else
            python3 cleanup_automation.py --agents
        fi
    elif [ "$1" = "--full" ]; then
        if [ "$2" = "--confirm" ]; then
            python3 cleanup_automation.py --full --confirm
        else
            python3 cleanup_automation.py --full
        fi
    elif [ "$1" = "--all-threads" ]; then
        if [ "$2" = "--confirm" ]; then
            python3 cleanup_automation.py --all-threads --confirm
        else
            python3 cleanup_automation.py --all-threads
        fi
    elif [ "$1" = "--threads" ]; then
        shift  # Remove --threads from arguments
        if [ $# -eq 0 ]; then
            # No thread IDs provided, delete all threads
            python3 cleanup_automation.py --threads
        else
            python3 cleanup_automation.py --threads "$@"
        fi
    elif [ "$1" = "--session" ]; then
        if [ -z "$2" ]; then
            print_error "No session file provided"
            print_info "Usage: $0 --session <session_file>"
            exit 1
        fi
        session_file="$2"
        if [ "$3" = "--confirm" ]; then
            python3 cleanup_automation.py --session "$session_file" --confirm
        else
            python3 cleanup_automation.py --session "$session_file"
        fi
    elif [ "$1" = "--interactive" ]; then
        python3 cleanup_automation.py
    else
        print_error "Unknown option: $1"
        show_help
        exit 1
    fi
}

# Run main function with all arguments
main "$@" 