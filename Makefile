.PHONY: audit audit-force audit-ci hooks

audit:
	python tools/audit_cleanup.py

audit-force:
	python tools/audit_cleanup.py --force || true

audit-ci:
	python tools/audit_cleanup.py || true

hooks:
	bash tools/install_hooks.sh
