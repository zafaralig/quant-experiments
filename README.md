# quant-experiments

> A consolidated home for my earlier Python quant work — originally scattered across many small standalone repos, now organized into one place so it's easier to browse, revisit, and build on.

A collection of quant-finance experiments in Python — backtesting trading ideas, computing risk metrics, modelling volatility, and pricing options. Each subfolder is a small, self-contained project with its own code, notebook, and notes.

---

## Index

### `strategies/` — backtesting trading ideas

| Folder | What it does |
|---|---|
| [macd_crossover/procedural](strategies/macd_crossover/procedural) | Backtests the MACD crossover signal on historical price data |
| [macd_crossover/oop](strategies/macd_crossover/oop) | Same MACD strategy, refactored into an object-oriented backtester |
| [sma_ema_crossover/procedural](strategies/sma_ema_crossover/procedural) | Long / short signals from SMA crossover with positions and returns |
| [sma_ema_crossover/oop](strategies/sma_ema_crossover/oop) | SMA + EMA crossover backtester in OOP style |
| [big_mondays/procedural](strategies/big_mondays/procedural) | "Big moves on Mondays" — a long-only strategy that captures large Monday moves |
| [big_mondays/oop](strategies/big_mondays/oop) | The Big Mondays strategy, rewritten as a class-based backtester |
| [atr](strategies/atr) | Tests whether price tends to follow the Average True Range, using OHLC data |
| [equal_weight_sp500](strategies/equal_weight_sp500) | Builds an equal-weighted S&P 500 portfolio using IEX Cloud data |

### `risk/` — risk metrics & portfolio simulation

| Folder | What it does |
|---|---|
| [var_cvar](risk/var_cvar) | Computes historical Value-at-Risk and Conditional VaR from Yahoo Finance data |
| [monte_carlo_portfolio](risk/monte_carlo_portfolio) | Simulates portfolio evolution using the covariance matrix and correlated random returns |

### `time_series/` — modelling

| Folder | What it does |
|---|---|
| [arima](time_series/arima) | Decomposes a series into trend / seasonal / residual and fits an ARIMA model |
| [garch](time_series/garch) | Forecasts volatility using ARCH and GARCH models |

### `options/` — pricing

| Folder | What it does |
|---|---|
| [black_scholes](options/black_scholes) | Prices European call and put options using the Black-Scholes formula |

### `misc/`

| Folder | What it does |
|---|---|
| [coin_flip_sim](misc/coin_flip_sim) | Monte Carlo simulation for the classic coin-flip problem |
| [basic_eda](misc/basic_eda) | Exploratory data analysis — common plots for understanding a dataset |

---

## Stack

Standard Python quant tooling: `pandas`, `numpy`, `matplotlib`, `yfinance`, `statsmodels`, `arch`. A mix of Jupyter notebooks and plain Python scripts.
