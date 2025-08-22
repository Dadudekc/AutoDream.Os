# 🧪 MAKEFILE - AGENT_CELLPHONE_V2
# Foundation & Testing Specialist - TDD Integration Project
# Version: 2.0
# Status: ACTIVE - CI/CD Integration Complete

# Variables
PYTHON = python3
PIP = pip3
PYTEST = python -m pytest
COVERAGE = coverage
PROJECT_ROOT = .

# Colors for output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
PURPLE = \033[0;35m
CYAN = \033[0;36m
WHITE = \033[1;37m
NC = \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

.PHONY: help install install-testing test test-smoke test-unit test-integration test-all coverage lint validate-standards clean clean-test-results clean-coverage clean-all security performance format check-format

# Help target
help: ## Show this help message
	@echo "$(CYAN)🧪 AGENT_CELLPHONE_V2 TESTING & CI/CD COMMANDS$(NC)"
	@echo "$(CYAN)===============================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Installation:$(NC)"
	@echo "  install          Install project dependencies"
	@echo "  install-testing  Install testing dependencies"
	@echo ""
	@echo "$(YELLOW)Testing:$(NC)"
	@echo "  test             Run all tests with coverage"
	@echo "  test-smoke       Run smoke tests only"
	@echo "  test-unit        Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo "  test-all         Run all tests in parallel"
	@echo "  test-fast        Run tests without coverage (faster)"
	@echo ""
	@echo "$(YELLOW)Quality Assurance:$(NC)"
	@echo "  coverage         Generate coverage report"
	@echo "  lint             Run all linting tools"
	@echo "  validate-standards Validate V2 coding standards"
	@echo "  security         Run security vulnerability scans"
	@echo "  performance      Run performance benchmarks"
	@echo ""
	@echo "$(YELLOW)CI/CD Pipeline:$(NC)"
	@echo "  ci-local         Run local CI/CD pipeline"
	@echo "  ci-start         Start local CI/CD environment"
	@echo "  ci-stop          Stop local CI/CD environment"
	@echo "  ci-logs          View CI/CD environment logs"
	@echo "  ci-shell         Access CI/CD testing shell"
	@echo "  ci-status        Check CI/CD environment status"
	@echo ""
	@echo "$(YELLOW)Code Formatting:$(NC)"
	@echo "  format           Format code with black"
	@echo "  check-format     Check code formatting"
	@echo ""
	@echo "$(YELLOW)Cleanup:$(NC)"
	@echo "  clean            Clean all generated files"
	@echo "  clean-test-results Clean test result files"
	@echo "  clean-coverage   Clean coverage files"
	@echo "  clean-ci         Clean CI/CD environment"
	@echo ""
	@echo "$(YELLOW)Examples:$(NC)"
	@echo "  make test-smoke              # Quick smoke test"
	@echo "  make test-unit coverage      # Unit tests with coverage"
	@echo "  make test-all parallel       # All tests in parallel"
	@echo "  make validate-standards      # Check V2 compliance"
	@echo "  make ci-local                # Run local CI/CD pipeline"
	@echo "  make ci-start                # Start CI/CD environment"

# Installation targets
install: ## Install project dependencies
	@echo "$(BLUE)📦 Installing project dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Project dependencies installed$(NC)"

install-testing: ## Install testing dependencies
	@echo "$(BLUE)🧪 Installing testing dependencies...$(NC)"
	$(PIP) install -r requirements-testing.txt
	@echo "$(GREEN)✅ Testing dependencies installed$(NC)"

# Testing targets
test: ## Run all tests with coverage
	@echo "$(BLUE)🧪 Running all tests with coverage...$(NC)"
	$(PYTEST) tests/ --cov=src --cov-report=term-missing --cov-report=html:htmlcov --cov-report=xml:coverage.xml --cov-fail-under=80 --verbose
	@echo "$(GREEN)✅ All tests completed$(NC)"

test-smoke: ## Run smoke tests only
	@echo "$(BLUE)🧪 Running smoke tests...$(NC)"
	$(PYTEST) tests/smoke/ --markers=smoke --verbose --tb=short
	@echo "$(GREEN)✅ Smoke tests completed$(NC)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)🧪 Running unit tests...$(NC)"
	$(PYTEST) tests/unit/ --markers=unit --verbose --tb=short
	@echo "$(GREEN)✅ Unit tests completed$(NC)"

test-integration: ## Run integration tests only
	@echo "$(BLUE)🧪 Running integration tests...$(NC)"
	$(PYTEST) tests/integration/ --markers=integration --verbose --tb=short
	@echo "$(GREEN)✅ Integration tests completed$(NC)"

test-all: ## Run all tests in parallel
	@echo "$(BLUE)🧪 Running all tests in parallel...$(NC)"
	$(PYTEST) tests/ -n auto --verbose --tb=short
	@echo "$(GREEN)✅ All tests completed in parallel$(NC)"

test-fast: ## Run tests without coverage (faster)
	@echo "$(BLUE)🧪 Running tests without coverage...$(NC)"
	$(PYTEST) tests/ --verbose --tb=short
	@echo "$(GREEN)✅ Tests completed (no coverage)$(NC)"

# Coverage targets
coverage: ## Generate coverage report
	@echo "$(BLUE)📊 Generating coverage report...$(NC)"
	$(COVERAGE) run -m pytest tests/
	$(COVERAGE) report --show-missing
	$(COVERAGE) html
	@echo "$(GREEN)✅ Coverage report generated$(NC)"
	@echo "$(CYAN)📁 Coverage report: htmlcov/index.html$(NC)"

# Quality assurance targets
lint: ## Run all linting tools
	@echo "$(BLUE)🔍 Running code quality checks...$(NC)"
	@echo "$(YELLOW)Running pylint...$(NC)"
	-pylint src/ --output-format=json --output=test-results/pylint_report.json
	@echo "$(YELLOW)Running flake8...$(NC)"
	-flake8 src/ --format=json --output-file=test-results/flake8_report.json
	@echo "$(YELLOW)Running black check...$(NC)"
	-black --check --diff src/
	@echo "$(YELLOW)Running mypy...$(NC)"
	-mypy src/ --json-report --output=test-results/mypy_report.json
	@echo "$(GREEN)✅ Linting completed$(NC)"

validate-standards: ## Validate V2 coding standards
	@echo "$(BLUE)🔍 Validating V2 coding standards...$(NC)"
	$(PYTHON) scripts/run_tests.py --validate-standards
	@echo "$(GREEN)✅ V2 standards validation completed$(NC)"

security: ## Run security vulnerability scans
	@echo "$(BLUE)🔒 Running security scans...$(NC)"
	@echo "$(YELLOW)Running bandit...$(NC)"
	-bandit -r src/ -f json -o test-results/bandit_report.json
	@echo "$(YELLOW)Running safety...$(NC)"
	-safety check --json --output test-results/safety_report.json
	@echo "$(GREEN)✅ Security scans completed$(NC)"

performance: ## Run performance benchmarks
	@echo "$(BLUE)⚡ Running performance tests...$(NC)"
	$(PYTEST) --markers=performance --benchmark-only --verbose
	@echo "$(GREEN)✅ Performance tests completed$(NC)"

# Code formatting targets
format: ## Format code with black
	@echo "$(BLUE)🎨 Formatting code...$(NC)"
	black src/ tests/ scripts/
	@echo "$(GREEN)✅ Code formatted$(NC)"

check-format: ## Check code formatting
	@echo "$(BLUE)🔍 Checking code formatting...$(NC)"
	black --check --diff src/ tests/ scripts/
	@echo "$(GREEN)✅ Code formatting check completed$(NC)"

# Cleanup targets
clean-test-results: ## Clean test result files
	@echo "$(BLUE)🧹 Cleaning test result files...$(NC)"
	rm -rf test-results/
	rm -f *.xml
	@echo "$(GREEN)✅ Test result files cleaned$(NC)"

clean-coverage: ## Clean coverage files
	@echo "$(BLUE)🧹 Cleaning coverage files...$(NC)"
	rm -rf htmlcov/
	rm -f .coverage
	rm -f coverage.xml
	rm -f coverage-badge.svg
	@echo "$(GREEN)✅ Coverage files cleaned$(NC)"

# CI/CD Pipeline targets
ci-local: ## Run local CI/CD pipeline
	@echo "$(CYAN)🚀 Starting local CI/CD pipeline...$(NC)"
	@echo "$(YELLOW)🔍 Stage 1: Code Quality & V2 Standards$(NC)"
	$(MAKE) validate-standards
	@echo "$(YELLOW)🧪 Stage 2: Testing & Coverage$(NC)"
	$(MAKE) test-all
	@echo "$(YELLOW)🔒 Stage 3: Security Testing$(NC)"
	$(MAKE) security
	@echo "$(YELLOW)⚡ Stage 4: Performance Testing$(NC)"
	$(MAKE) performance
	@echo "$(YELLOW)📈 Stage 5: Coverage Analysis$(NC)"
	$(MAKE) coverage
	@echo "$(GREEN)🎉 Local CI/CD pipeline completed successfully!$(NC)"

ci-start: ## Start local CI/CD environment
	@echo "$(CYAN)🚀 Starting local CI/CD environment...$(NC)"
	docker-compose -f docker-compose.ci.yml up -d
	@echo "$(GREEN)✅ CI/CD environment started$(NC)"
	@echo "$(YELLOW)📊 Access web dashboard at: http://localhost:8080$(NC)"
	@echo "$(YELLOW)🔍 View logs with: make ci-logs$(NC)"

ci-stop: ## Stop local CI/CD environment
	@echo "$(YELLOW)🛑 Stopping local CI/CD environment...$(NC)"
	docker-compose -f docker-compose.ci.yml down
	@echo "$(GREEN)✅ CI/CD environment stopped$(NC)"

ci-logs: ## View CI/CD environment logs
	@echo "$(CYAN)📋 CI/CD Environment Logs$(NC)"
	docker-compose -f docker-compose.ci.yml logs -f

ci-shell: ## Access CI/CD testing shell
	@echo "$(CYAN)🐚 Accessing CI/CD testing shell...$(NC)"
	docker exec -it agent_cellphone_v2_testing bash

ci-status: ## Check CI/CD environment status
	@echo "$(CYAN)📊 CI/CD Environment Status$(NC)"
	docker-compose -f docker-compose.ci.yml ps
	@echo ""
	@echo "$(YELLOW)📈 Service Status:$(NC)"
	@docker-compose -f docker-compose.ci.yml ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

clean-ci: ## Clean CI/CD environment
	@echo "$(YELLOW)🧹 Cleaning CI/CD environment...$(NC)"
	docker-compose -f docker-compose.ci.yml down -v
	docker system prune -f
	@echo "$(GREEN)✅ CI/CD environment cleaned$(NC)"

clean-all: clean-test-results clean-coverage ## Clean all generated files
	@echo "$(BLUE)🧹 Cleaning all generated files...$(NC)"
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	@echo "$(GREEN)✅ All generated files cleaned$(NC)"

# Development workflow targets
dev-setup: install install-testing ## Complete development setup
	@echo "$(BLUE)🚀 Setting up development environment...$(NC)"
	@echo "$(GREEN)✅ Development environment ready$(NC)"
	@echo "$(CYAN)📋 Available commands:$(NC)"
	@echo "$(CYAN)  make test-smoke     # Quick validation$(NC)"
	@echo "$(CYAN)  make test-unit      # Component testing$(NC)"
	@echo "$(CYAN)  make test-all       # Full test suite$(NC)"
	@echo "$(CYAN)  make coverage       # Coverage report$(NC)"
	@echo "$(CYAN)  make lint           # Code quality$(NC)"

quick-check: test-smoke lint check-format ## Quick quality check
	@echo "$(BLUE)⚡ Running quick quality check...$(NC)"
	@echo "$(GREEN)✅ Quick check completed$(NC)"

full-check: test-all coverage lint security performance ## Full quality check
	@echo "$(BLUE)🔍 Running full quality check...$(NC)"
	@echo "$(GREEN)✅ Full quality check completed$(NC)"

# CI/CD targets
ci-test: ## Run tests for CI/CD pipeline
	@echo "$(BLUE)🔄 Running CI/CD tests...$(NC)"
	$(PYTEST) tests/ --cov=src --cov-report=xml:coverage.xml --cov-fail-under=80 --junitxml=test-results/junit.xml
	@echo "$(GREEN)✅ CI/CD tests completed$(NC)"

ci-lint: ## Run linting for CI/CD pipeline
	@echo "$(BLUE)🔄 Running CI/CD linting...$(NC)"
	pylint src/ --output-format=json --output=test-results/pylint_report.json
	flake8 src/ --format=json --output-file=test-results/flake8_report.json
	black --check --diff src/
	mypy src/ --json-report --output=test-results/mypy_report.json
	@echo "$(GREEN)✅ CI/CD linting completed$(NC)"

# Documentation targets
test-docs: ## Test documentation examples
	@echo "$(BLUE)📚 Testing documentation examples...$(NC)"
	$(PYTEST) --doctest-modules --doctest-continue-on-failure
	@echo "$(GREEN)✅ Documentation tests completed$(NC)"

# Monitoring and reporting
test-status: ## Show testing status and coverage
	@echo "$(BLUE)📊 Testing Status Report$(NC)"
	@echo "$(CYAN)=======================$(NC)"
	@if [ -f coverage.xml ]; then \
		echo "$(GREEN)✅ Coverage report available$(NC)"; \
	else \
		echo "$(RED)❌ No coverage report found$(NC)"; \
	fi
	@if [ -d test-results ]; then \
		echo "$(GREEN)✅ Test results available$(NC)"; \
	else \
		echo "$(RED)❌ No test results found$(NC)"; \
	fi
	@if [ -d htmlcov ]; then \
		echo "$(GREEN)✅ HTML coverage available$(NC)"; \
	else \
		echo "$(RED)❌ No HTML coverage found$(NC)"; \
	fi

# Special targets for V2 standards compliance
v2-compliance: validate-standards test-smoke ## Check V2 standards compliance
	@echo "$(BLUE)🔍 Checking V2 standards compliance...$(NC)"
	@echo "$(GREEN)✅ V2 standards compliance check completed$(NC)"

# Emergency targets
emergency-clean: ## Emergency cleanup (use with caution)
	@echo "$(RED)🚨 EMERGENCY CLEANUP$(NC)"
	@echo "$(RED)This will remove ALL generated files and caches$(NC)"
	@read -p "Are you sure? Type 'YES' to confirm: " confirm; \
	if [ "$$confirm" = "YES" ]; then \
		rm -rf test-results/ htmlcov/ __pycache__/ .pytest_cache/ .mypy_cache/ .coverage coverage.xml coverage-badge.svg; \
		echo "$(GREEN)✅ Emergency cleanup completed$(NC)"; \
	else \
		echo "$(YELLOW)Emergency cleanup cancelled$(NC)"; \
	fi

.PHONY: status demo test validate fmt

status:
	@python -m src --status

demo:
	@python -m src --demo

test:
	@python -m src --test

validate:
	@python -m src --validate

fmt:
	@ruff format src || true
