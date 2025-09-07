import pathlib
import sys

from scipy import stats
import numpy as np
import pandas as pd

from common_algorithms import (
import importlib.util


# Import module directly to avoid executing package-level side effects
MODULE_PATH = pathlib.Path(__file__).resolve().parents[2] / "src/services/financial/portfolio/common_algorithms.py"
spec = importlib.util.spec_from_file_location("common_algorithms", MODULE_PATH)
common_algorithms = importlib.util.module_from_spec(spec)
sys.modules["common_algorithms"] = common_algorithms
spec.loader.exec_module(common_algorithms)

    calculate_var,
    calculate_max_drawdown,
    calculate_beta,
    calculate_alpha,
)


def test_calculate_var():
    weights = {"A": 0.5, "B": 0.5}
    returns = pd.Series({"A": 0.01, "B": 0.02})
    covariance = pd.DataFrame(
        [[0.0004, 0.0002], [0.0002, 0.0003]], index=["A", "B"], columns=["A", "B"]
    )
    var = calculate_var(weights, returns, covariance, 0.95)

    weight_array = np.array(list(weights.values()))
    portfolio_return = np.sum(returns * weight_array)
    portfolio_volatility = np.sqrt(
        np.dot(weight_array.T, np.dot(covariance, weight_array))
    )
    expected = portfolio_return - stats.norm.ppf(1 - 0.95) * portfolio_volatility
    assert np.isclose(var, expected)


def test_calculate_max_drawdown():
    returns = pd.Series([0.1, -0.2, 0.05, 0.03])
    drawdown = calculate_max_drawdown(returns)
    assert np.isclose(drawdown, 0.2)


def test_calculate_beta_and_alpha():
    portfolio_returns = pd.Series([0.02, 0.03, 0.015])
    benchmark_returns = pd.Series([0.01, 0.02, 0.005])
    beta = calculate_beta(portfolio_returns, benchmark_returns)
    covariance = np.cov(portfolio_returns, benchmark_returns)[0, 1]
    variance = np.var(benchmark_returns)
    expected_beta = covariance / variance
    assert np.isclose(beta, expected_beta)

    alpha = calculate_alpha(portfolio_returns, benchmark_returns, 0.01)
    port_mean = portfolio_returns.mean() * 252
    bench_mean = benchmark_returns.mean() * 252
    expected_alpha = port_mean - (0.01 + expected_beta * (bench_mean - 0.01))
    assert np.isclose(alpha, expected_alpha)
