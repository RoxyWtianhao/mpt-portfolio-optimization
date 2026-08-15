import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf


RISK_FREE_RATE = 0.035
TRADING_DAYS = 252
SIMULATIONS = 5000


def main():
    st.title("Markowitz Portfolio Optimizer")
    st.write("Simulate 5,000 portfolios using two years of daily prices.")
    ticker_text = st.text_input(
        "Tickers (separate with commas)",
        "AAPL, MSFT, GOOGL, AMZN, JPM",
    )
    tickers = [ticker.strip().upper() for ticker in ticker_text.split(",")]
    source = st.radio(
        "Data source",
        ["Yahoo Finance", "Offline demo"],
        horizontal=True,
    )
    if not st.button("Run simulation"):
        return
    if len(tickers) < 2:
        st.error("Please enter at least two ticker symbols.")
        return
    if source == "Offline demo":
        dates = pd.date_range(
            end=pd.Timestamp.today(), periods=TRADING_DAYS * 2, freq="B"
        )
        generator = np.random.default_rng(42)
        data = generator.normal(0.0004, 0.015, (len(dates), len(tickers)))
        prices = pd.DataFrame(
            100 * np.exp(np.cumsum(data, axis=0)),
            index=dates,
            columns=tickers,
        )
        st.info("Offline demo uses simulated prices, not real market data.")
    else:
        prices = yf.download(
            tickers, period="2y", auto_adjust=True, progress=False
        )["Close"].dropna()
        if prices.empty:
            st.error("Yahoo returned no data. Try Offline demo or check network.")
            return
    daily_returns = prices.pct_change().dropna()
    annual_returns = daily_returns.mean() * TRADING_DAYS
    annual_covariance = daily_returns.cov() * TRADING_DAYS
    results = np.zeros((3, SIMULATIONS))
    all_weights = []
    for index in range(SIMULATIONS):
        weights = np.random.random(len(tickers))
        weights /= weights.sum()
        portfolio_return = np.sum(annual_returns * weights)
        portfolio_risk = np.sqrt(weights @ annual_covariance.values @ weights)
        sharpe_ratio = (portfolio_return - RISK_FREE_RATE) / portfolio_risk
        results[:, index] = portfolio_return, portfolio_risk, sharpe_ratio
        all_weights.append(weights)
    portfolios = pd.DataFrame(
        results.T, columns=["Annual Return", "Volatility", "Sharpe Ratio"]
    )
    max_sharpe = portfolios["Sharpe Ratio"].idxmax()
    min_variance = portfolios["Volatility"].idxmin()

    for title, position in [("Max Sharpe", max_sharpe),
                            ("Min Variance", min_variance)]:
        st.write(f"### {title} Portfolio")
        st.write(portfolios.loc[position])
        weights = pd.Series(all_weights[position], index=tickers)
        st.write(weights.map("{:.2%}".format))

    fig, ax = plt.subplots(figsize=(9, 6))
    scatter = ax.scatter(
        portfolios["Volatility"], portfolios["Annual Return"],
        c=portfolios["Sharpe Ratio"], cmap="viridis", s=8,
    )
    for position, color, label in [
        (max_sharpe, "red", "Max Sharpe"),
        (min_variance, "blue", "Min Variance"),
    ]:
        ax.scatter(
            portfolios.loc[position, "Volatility"],
            portfolios.loc[position, "Annual Return"],
            color=color, marker="*", s=250, label=label,
        )
    fig.colorbar(scatter, label="Sharpe Ratio")
    ax.set(xlabel="Annual Volatility", ylabel="Annual Return")
    ax.set_title("Markowitz Efficient Frontier Simulation")
    ax.legend()
    st.pyplot(fig)


if __name__ == "__main__":
    main()
