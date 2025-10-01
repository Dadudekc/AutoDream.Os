##############################################################################
# Memory Audit Runner - Phase 4 (PowerShell)
# ===========================================
#
# PowerShell wrapper for memory monitoring CLI.
# Windows-compatible version of run_memory_audit.sh
#
# Author: Agent-7 (Web Development Expert)
# License: MIT
# V2 Compliance: Simple, focused, no overengineering
##############################################################################

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$RemainingArgs
)

# Script configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$PythonCmd = if ($env:PYTHON) { $env:PYTHON } else { "python" }
$CLIModule = "src.observability.memory.cli"

##############################################################################
# Helper Functions
##############################################################################

function Print-Header {
    Write-Host "========================================" -ForegroundColor Blue
    Write-Host "  Memory Audit Runner - Phase 4" -ForegroundColor Blue
    Write-Host "========================================" -ForegroundColor Blue
    Write-Host ""
}

function Print-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Print-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Print-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Print-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Blue
}

function Show-Usage {
    Write-Host @"
Usage: .\run_memory_audit.ps1 [COMMAND] [OPTIONS]

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
    .\run_memory_audit.ps1 report                       # Generate JSON report
    .\run_memory_audit.ps1 report -o report.json        # Save report to file
    .\run_memory_audit.ps1 report -f text               # Generate text report
    .\run_memory_audit.ps1 watch -i 30 -d 300           # Watch for 5 min
    .\run_memory_audit.ps1 cleanup                      # Run memory cleanup
    .\run_memory_audit.ps1 status                       # Show current status

"@
}

##############################################################################
# Main Execution
##############################################################################

# Change to project root
Set-Location $ProjectRoot

# Check if Python is available
if (-not (Get-Command $PythonCmd -ErrorAction SilentlyContinue)) {
    Print-Error "Python not found. Please install Python 3.7+"
    exit 1
}

switch ($Command.ToLower()) {
    "report" {
        Print-Header
        Print-Info "Generating memory leak report..."
        & $PythonCmd -m $CLIModule report $RemainingArgs
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Report generation complete"
        }
    }
    
    "watch" {
        Print-Header
        Print-Info "Starting memory watch..."
        & $PythonCmd -m $CLIModule watch $RemainingArgs
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Memory watch complete"
        }
    }
    
    "cleanup" {
        Print-Header
        Print-Info "Running memory cleanup..."
        & $PythonCmd -m $CLIModule cleanup
        if ($LASTEXITCODE -eq 0) {
            Print-Success "Cleanup complete"
        }
    }
    
    "status" {
        Print-Header
        & $PythonCmd -m $CLIModule status
    }
    
    "help" {
        Show-Usage
    }
    
    default {
        Print-Error "Unknown command: $Command"
        Write-Host ""
        Show-Usage
        exit 1
    }
}

