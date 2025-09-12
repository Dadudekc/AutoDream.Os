.PHONY: init lint test validate ci sweep overnight onboard prod-ready hooks
init:
	python -m pip install --upgrade pip
	pip install -r requirements.txt || true
	pip install -r requirements-dev.txt || true
hooks:
	chmod +x scripts/hooks/pre-push.sh
	git config core.hooksPath scripts/hooks
lint:
	ruff check .
	black --check .
	isort --check-only .
validate:
	python scripts/validate_v2_compliance.py --rules config/v2_rules.yaml
test:
	pytest -q --maxfail=1 --disable-warnings --cov=scripts --cov=src --cov-fail-under=85
ci: lint validate test
sweep:
	python tools/mode_sweep.py
overnight:
	python scripts/overnight/overnight_main.py
onboard:
	python cli.py --onboard --role-map production_ready
prod-ready:
	$(MAKE) ci && python cli.py --onboard --role-map production_ready --wrapup-only
