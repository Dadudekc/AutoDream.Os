#!/usr/bin/env python3
"""
Options Pricing Module - Agent Cellphone V2
===========================================

Black-Scholes pricing models and Greeks calculations for options trading.
Follows V2 standards: ≤300 LOC, SRP, OOP principles.
"""

import logging
import numpy as np
from typing import Dict, Optional
from enum import Enum

from src.utils.stability_improvements import stability_manager, safe_import
from .common import (
    normal_cdf,
    normal_pdf,
    calculate_d1,
    calculate_d2,
    intrinsic_value,
    break_even_point,
)

logger = logging.getLogger(__name__)


class OptionType(Enum):
    """Option types"""

    CALL = "CALL"
    PUT = "PUT"


class Greeks(Enum):
    """Option Greeks"""

    DELTA = "DELTA"
    GAMMA = "GAMMA"
    THETA = "THETA"
    VEGA = "VEGA"
    RHO = "RHO"


class OptionsPricingEngine:
    """
    Advanced options pricing engine using Black-Scholes model
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.OptionsPricingEngine")

    def calculate_black_scholes(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: OptionType,
    ) -> Dict[str, float]:
        """Calculate Black-Scholes option pricing and Greeks"""
        try:
            # Black-Scholes formula components
            d1 = calculate_d1(S, K, T, r, sigma)
            d2 = calculate_d2(d1, sigma, T)

            if option_type == OptionType.CALL:
                price = S * normal_cdf(d1) - K * np.exp(-r * T) * normal_cdf(d2)
                delta = normal_cdf(d1)
            else:  # PUT
                price = K * np.exp(-r * T) * normal_cdf(-d2) - S * normal_cdf(-d1)
                delta = normal_cdf(d1) - 1

            # Greeks
            gamma = normal_pdf(d1) / (S * sigma * np.sqrt(T))
            theta = (-S * sigma * normal_pdf(d1)) / (2 * np.sqrt(T)) - r * K * np.exp(
                -r * T
            ) * normal_cdf(d2)
            vega = S * np.sqrt(T) * normal_pdf(d1)
            rho = K * T * np.exp(-r * T) * normal_cdf(d2)

            return {
                "price": price,
                "delta": delta,
                "gamma": gamma,
                "theta": theta,
                "vega": vega,
                "rho": rho,
            }

        except Exception as e:
            self.logger.error(f"Error calculating Black-Scholes: {e}")
            return {}

    def calculate_implied_volatility(
        self,
        market_price: float,
        S: float,
        K: float,
        T: float,
        r: float,
        option_type: OptionType,
    ) -> float:
        """Calculate implied volatility using Newton-Raphson method"""
        try:
            sigma = 0.5  # Initial guess
            tolerance = 1e-5
            max_iterations = 100

            for i in range(max_iterations):
                price = self.calculate_black_scholes(
                    S, K, T, r, sigma, option_type
                ).get("price", 0)
                vega = self.calculate_black_scholes(S, K, T, r, sigma, option_type).get(
                    "vega", 0
                )

                if abs(price - market_price) < tolerance:
                    return sigma

                if abs(vega) < 1e-10:
                    break

                sigma = sigma - (price - market_price) / vega
                sigma = max(0.001, min(5.0, sigma))  # Bounds

            return sigma

        except Exception as e:
            self.logger.error(f"Error calculating implied volatility: {e}")
            return 0.0

    def calculate_greeks(
        self,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: OptionType,
    ) -> Dict[str, float]:
        """Calculate option Greeks"""
        try:
            d1 = calculate_d1(S, K, T, r, sigma)
            d2 = calculate_d2(d1, sigma, T)

            if option_type == OptionType.CALL:
                delta = normal_cdf(d1)
            else:  # PUT
                delta = normal_cdf(d1) - 1

            gamma = normal_pdf(d1) / (S * sigma * np.sqrt(T))
            theta = (-S * sigma * normal_pdf(d1)) / (2 * np.sqrt(T)) - r * K * np.exp(
                -r * T
            ) * normal_cdf(d2)
            vega = S * np.sqrt(T) * normal_pdf(d1)
            rho = K * T * np.exp(-r * T) * normal_cdf(d2)

            return {
                "delta": delta,
                "gamma": gamma,
                "theta": theta,
                "vega": vega,
                "rho": rho,
            }

        except Exception as e:
            self.logger.error(f"Error calculating Greeks: {e}")
            return {}

    def calculate_time_value(
        self,
        option_price: float,
        intrinsic_value: float,
    ) -> float:
        """Calculate time value of an option"""
        return max(0, option_price - intrinsic_value)

    def calculate_intrinsic_value(
        self,
        S: float,
        K: float,
        option_type: OptionType,
    ) -> float:
        """Calculate intrinsic value of an option"""
        return intrinsic_value(S, K, option_type == OptionType.CALL)

    def calculate_breakeven_point(
        self,
        K: float,
        premium: float,
        option_type: OptionType,
    ) -> float:
        """Calculate breakeven point for an option strategy"""
        return break_even_point(K, premium, option_type == OptionType.CALL)
