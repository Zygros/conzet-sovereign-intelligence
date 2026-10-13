# Ghost Mode Backtest Harness (skeleton)

Signal service concept from X post 2025-12-30: premium coordination signal service built on ARC-AGI principles.
Data: public OHLCV only. No private feeds. No paid data.

```python
import pandas as pd

def signal_fn(df):
    # TODO: ARC-AGI-inspired pattern detector on returns
    return pd.Series(0, index=df.index)

def backtest(df, signal):
    # TODO: position sizing, transaction costs, max drawdown
    return {"sharpe": None, "max_drawdown": None, "trades": 0}

# Usage:
# df = pd.read_csv('public_ohlcv.csv')
# bt = backtest(df, signal_fn(df))
# print(bt)
```

## Rules

- Public data only.
- Documented assumptions.
- Published failures count as results.
- No curve-fitting on the test set.

Always add. Never take.
