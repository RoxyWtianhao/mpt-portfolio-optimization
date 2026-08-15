# Markowitz MPT Monte Carlo Explorer

A minimal Streamlit application that uses historical market prices and Monte
Carlo simulation to explore long-only portfolios under Markowitz's Modern
Portfolio Theory (MPT).

This is a compact educational project for demonstrating practical Python,
financial data handling, and quantitative portfolio-analysis skills in an
academic CV or GitHub portfolio.

## Features

- Downloads two years of daily adjusted closing prices with `yfinance`.
- Accepts user-entered ticker symbols (default: AAPL, MSFT, GOOGL, AMZN, JPM).
- Simulates 5,000 long-only, fully invested portfolios with random NumPy
  weights.
- Identifies the maximum-Sharpe and minimum-volatility portfolios.
- Visualizes the simulated risk-return space with Matplotlib.

## Mathematical Background

Modern Portfolio Theory treats a portfolio as a vector of weights
`$w = (w_1, \ldots, w_n)$`, where `$\sum_i w_i = 1$`. Given annualized expected
asset returns `$\mu$` and annualized covariance matrix `$\Sigma$`, the expected
portfolio return and volatility are:

$$
R_p = w^T\mu
$$

$$
\sigma_p = \sqrt{w^T\Sigma w}
$$

The Sharpe Ratio measures excess return per unit of total risk:

$$
\text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}
$$

where `$R_f$` is the risk-free rate. This application uses a 3.5% annual
risk-free rate and selects the simulated portfolio with the highest ratio.

## Run in PyCharm

1. Clone or download this repository and open the `markowitz-mpt-streamlit`
   folder as a PyCharm project.
2. Go to **File > Settings > Project > Python Interpreter**, choose
   **Add Interpreter**, and create a new virtual environment named `.venv`.
3. Open PyCharm's built-in **Terminal** and install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application from the same terminal:

   ```bash
   streamlit run app.py
   ```

5. Streamlit will print a local URL (normally `http://localhost:8501`) to open
   in a browser. To debug the Python file in PyCharm, open `app.py` and use the
   standard Debug action; Streamlit itself should still be launched with the
   command above for the interactive web interface.

## Project Structure

```text
markowitz-mpt-streamlit/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Acknowledgments and References

The implementation adapts the standard Markowitz Monte Carlo workflow widely
used in open-source Python-finance tutorials. It is inspired by
Yves Hilpisch's [Python for Finance code repository](https://github.com/yhilpisch/py4fi),
which accompanies the O'Reilly book *Python for Finance*.

- Markowitz, H. (1952). *Portfolio Selection*. The Journal of Finance, 7(1),
  77-91.
- [yfinance](https://github.com/ranaroussi/yfinance), for access to Yahoo
  Finance market data.
- [Streamlit](https://streamlit.io/), for the open-source Python web-app
  framework.

## Disclaimer

This project is for education only. Historical data and simulated portfolios do
not constitute investment advice or a recommendation to buy or sell securities.
