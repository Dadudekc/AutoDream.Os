"""Utilities for preparing and validating market data used by trading
strategies."""

from __future__ import annotations

import logging
from typing import Iterable

import pandas as pd

logger = logging.getLogger(__name__)


def prepare_market_data(df: pd.DataFrame, required_columns: Iterable[str] | None = None) -> pd.DataFrame:
    """Validate that *df* contains the expected columns and return a copy.

    Parameters
    ----------
    df:
        The raw market data.
    required_columns:
        Columns that must exist on the dataframe.  If ``None`` the columns
        ``{"Close", "Volume"}`` are required.

    Returns
    -------
    pandas.DataFrame
        A copy of *df* that is safe for strategy analysis.
    """
    required = set(required_columns or {"Close", "Volume"})
    logger.info("Preparing market data with %d rows", len(df))
    missing = required - set(df.columns)
    if missing:
        logger.error("Market data missing columns: %s", ", ".join(sorted(missing)))
        raise ValueError(f"Missing columns: {missing}")
    return df.copy()
