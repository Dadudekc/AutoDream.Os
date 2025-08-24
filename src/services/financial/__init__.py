"""Financial Services Module - simplified for testing.

This package exposes financial service components. During testing we avoid
importing heavy dependencies so that modules with optional third-party
requirements (e.g. `yfinance`) don't fail on import. Individual services
should be imported directly as needed.
"""

__version__ = "1.0.0"
__author__ = "Business Intelligence Agent"
__status__ = "ACTIVE"

# Intentionally avoid eager imports that may rely on optional third-party
# packages. The orchestrator is exposed lazily so that basic package imports
# remain lightweight during tests.
try:  # pragma: no cover - optional dependencies may not be present
    from .orchestrator import FinancialServicesOrchestrator

    __all__ = ["FinancialServicesOrchestrator"]
except Exception:  # pragma: no cover
    __all__: list[str] = []

