"""Ghost Mode Backtest Harness (skeleton).

Signal service concept from X post 2025-12-30: premium coordination signal
service built on ARC-AGI principles.

Data: public OHLCV only. No private feeds. No paid data.

Rules:
- Public data only.
- Documented assumptions.
- Published failures count as results.
- No curve-fitting on the test set.

Always add. Never take.

This file is intentionally a minimal scaffold. It does not claim validated
trading performance. The TODOs remain explicit until implemented and tested.
"""

import pandas as pd


def signal_fn(df: pd.DataFrame) -> pd.Series:
    """Placeholder ARC-AGI-inspired pattern detector on returns."""
    return pd.Series(0, index=df.index, dtype="int64")


def backtest(df: pd.DataFrame, signal: pd.Series) -> dict:
    """Placeholder backtest; metrics remain unavailable until implemented."""
    return {"sharpe": None, "max_drawdown": None, "trades": 0}


if __name__ == "__main__":
    print(
        "Ghost Mode Backtest Harness is a skeleton. "
        "Provide a public OHLCV dataset and implement transaction costs, "
        "position sizing, and drawdown calculations before interpreting results."
    )
