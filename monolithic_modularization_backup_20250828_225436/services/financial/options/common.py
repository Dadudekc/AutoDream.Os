"""Common mathematical helpers for options modules."""

import math
import numpy as np


def normal_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def normal_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * x**2)


def calculate_d1(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """Calculate the d1 term in Black-Scholes."""
    return (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))


def calculate_d2(d1: float, sigma: float, T: float) -> float:
    """Calculate the d2 term in Black-Scholes."""
    return d1 - sigma * np.sqrt(T)


def intrinsic_value(S: float, K: float, is_call: bool) -> float:
    """Return intrinsic value for call or put."""
    return max(0, S - K) if is_call else max(0, K - S)


def break_even_point(K: float, premium: float, is_call: bool) -> float:
    """Return break-even point for an option."""
    return K + premium if is_call else K - premium
