#!/bin/bash
##############################################################################
# Memory Audit Runner - Phase 4
# ==============================
#
# Shell script wrapper for memory monitoring CLI.
# Provides convenient interface for memory leak detection and reporting.
#
# Author: Agent-7 (Web Development Expert)
# License: MIT
# V2 Compliance: Simple, focused, no overengineering
##############################################################################

set -e  # Exit on error

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_CMD="${PYTHON:-python}"
CLI_MODULE="src.observability.memory.cli"

# Colors for output (optional, works on most terminals)
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

##############################################################################
# Helper Functions
##############################################################################

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  Memory Audit Runner - Phase 4${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
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

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

show_usage() {
    cat << EOF
Usage: $0 [COMMAND] [OPTIONS]

Commands:
    report      Generate memory leak report
    watch       Watch memory usage in real-time
    cleanup     Run manual memory cleanup
    status      Show current memory status
    help        Show this help message

Report Options:
    -o, --output FILE    Output file path
    -f, --format FORMAT  Output format (json|text)

Watch Options:
    -i, --interval SEC   Check interval in seconds (default: 60)
    -d, --duration SEC   Total duration in seconds (0 = infinite)

Examples:
    $0 report                           # Generate JSON report to stdout
    $0 report -o report.json            # Save report to file
    $0 report -f text                   # Generate text report
    $0 watch -i 30 -d 300               # Watch for 5 minutes, 30s intervals
    $0 cleanup                          # Run memory cleanup
    $0 status                           # Show current status

EOF
}

##############################################################################
# Main Execution
##############################################################################

main() {
    # Change to project root
    cd "$PROJECT_ROOT"
    
    # Check if Python is available
    if ! command -v "$PYTHON_CMD" &> /dev/null; then
        print_error "Python not found. Please install Python 3.7+"
        exit 1
    fi
    
    # Parse command
    COMMAND="${1:-help}"
    shift || true
    
    case "$COMMAND" in
        report)
            print_header
            print_info "Generating memory leak report..."
            $PYTHON_CMD -m $CLI_MODULE report "$@"
            print_success "Report generation complete"
            ;;
        
        watch)
            print_header
            print_info "Starting memory watch..."
            $PYTHON_CMD -m $CLI_MODULE watch "$@"
            print_success "Memory watch complete"
            ;;
        
        cleanup)
            print_header
            print_info "Running memory cleanup..."
            $PYTHON_CMD -m $CLI_MODULE cleanup
            print_success "Cleanup complete"
            ;;
        
        status)
            print_header
            $PYTHON_CMD -m $CLI_MODULE status
            ;;
        
        help|--help|-h)
            show_usage
            ;;
        
        *)
            print_error "Unknown command: $COMMAND"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Run main function
main "$@"

