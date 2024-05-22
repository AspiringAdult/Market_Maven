import yfinance as yf  # noqa
import pandas as pd  # noqa
from backtesting import BacktestingEngine  # noqa
from strategies.mean_reversion import MeanReversionStrategy  # noqa

# Define the trading parameters
start_date = '2022-01-01'
end_date = '2022-02-28'
capital = 10000
symbol = 'AAPL'

# Download the historical data
data = yf.download(symbol, start=start_date, end=end_date)

# Define the trading strategy
class MyMeanReversionStrategy(MeanReversionStrategy):
    def should_enter(self, data):
        return super().should_enter(data) and data['volume'] > 100000

# Create the backtesting engine
backtesting_engine = BacktestingEngine(MyMeanReversionStrategy, capital)

# Run the backtesting
backtesting_engine.backtest(data, start_date, end_date)

# Display the results
results = backtesting_engine.get_results()
print(results)
