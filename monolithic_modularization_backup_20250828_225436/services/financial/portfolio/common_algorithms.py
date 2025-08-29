"""Common portfolio analytics algorithms.

This module centralizes basic financial algorithms that were
previously duplicated across portfolio components. Each function
is designed to operate on simple ``pandas`` series and make a best
attempt at returning a sensible default when provided with empty
inputs.
"""

from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd
from scipy import stats


def calculate_var(
    weights: Dict[str, float],
    returns: pd.Series,
    covariance: pd.DataFrame,
    confidence_level: float,
) -> float:
    """Calculate portfolio Value at Risk using a parametric approach.

    Args:
        weights: Mapping of asset symbols to portfolio weights.
        returns: Series of mean asset returns.
        covariance: Covariance matrix of asset returns.
        confidence_level: Desired confidence level (e.g. ``0.95``).

    Returns:
        Estimated Value at Risk. ``0.0`` is returned when inputs are
        incomplete or invalid.
    """
    try:
        if returns is None or covariance is None:
            return 0.0

        weight_array = np.array(list(weights.values()))
        portfolio_return = np.sum(returns * weight_array)
        portfolio_volatility = np.sqrt(
            np.dot(weight_array.T, np.dot(covariance, weight_array))
        )

        z_score = stats.norm.ppf(1 - confidence_level)
        return float(portfolio_return - z_score * portfolio_volatility)
    except Exception:
        return 0.0


def calculate_max_drawdown(returns: pd.Series) -> float:
    """Compute the maximum drawdown for a series of returns.

    The algorithm converts returns to a cumulative performance series and
    measures the greatest peak-to-trough decline.
    """
    try:
        if returns.empty:
            return 0.0

        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return float(abs(drawdown.min()))
    except Exception:
        return 0.0


def calculate_beta(
    portfolio_returns: pd.Series, benchmark_returns: pd.Series
) -> float:
    """Calculate portfolio beta relative to a benchmark.

    Args:
        portfolio_returns: Series of portfolio returns.
        benchmark_returns: Series of benchmark returns.

    Returns:
        Beta value. Defaults to ``1.0`` when insufficient data is supplied.
    """
    try:
        if portfolio_returns.empty or benchmark_returns.empty:
            return 1.0

        aligned = pd.concat([portfolio_returns, benchmark_returns], axis=1).dropna()
        if len(aligned) < 2:
            return 1.0

        port = aligned.iloc[:, 0]
        bench = aligned.iloc[:, 1]
        covariance = np.cov(port, bench)[0, 1]
        variance = np.var(bench)
        return float(covariance / variance) if variance != 0 else 1.0
    except Exception:
        return 1.0


def calculate_alpha(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
    risk_free_rate: float,
) -> float:
    """Calculate annualized portfolio alpha relative to a benchmark.

    Args:
        portfolio_returns: Series of portfolio returns.
        benchmark_returns: Series of benchmark returns.
        risk_free_rate: Annualized risk-free rate expressed as a decimal.

    Returns:
        Alpha value. ``0.0`` is returned when inputs are insufficient.
    """
    try:
        if portfolio_returns.empty or benchmark_returns.empty:
            return 0.0

        beta = calculate_beta(portfolio_returns, benchmark_returns)
        aligned = pd.concat([portfolio_returns, benchmark_returns], axis=1).dropna()
        if len(aligned) < 2:
            return 0.0

        port = aligned.iloc[:, 0]
        bench = aligned.iloc[:, 1]
        port_mean = port.mean() * 252
        bench_mean = bench.mean() * 252
        return float(port_mean - (risk_free_rate + beta * (bench_mean - risk_free_rate)))
    except Exception:
        return 0.0
