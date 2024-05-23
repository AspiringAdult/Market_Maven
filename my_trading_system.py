# main.py
import argparse
# my_trading_strategy.py
from config import config
from data_processing import fetch_historical_data, preprocess_data
from risk_management import set_stop_loss, set_take_profit
from monitoring import log_trades, generate_reports
from historical_data import fetch_historical_data
from data_preprocessing import preprocess_data
from strategy_evaluation import backtest, optimize_strategy
from execution import create_order, manage_positions
from risk_management import set_stop_loss, set_take_profit

def main():
    parser = argparse.ArgumentParser(description='Algo Trading Bot')
    parser.add_argument('--mode', choices=['backtest', 'live_trading'], required=True,
                        help='Select the mode: backtest or live_trading')
    args = parser.parse_args()

    # 1. Fetch historical data
    historical_data = fetch_historical_data(config.HISTORICAL_DATA_DIR, config.TIMEFRAME,
                                            config.START_DATE, config.END_DATE)

    # 2. Preprocess data
    preprocessed_data = preprocess_data(historical_data)

    if args.mode == 'backtest':
        # 3. Evaluate and optimize strategy
        backtest_results = backtest(preprocessed_data, config.INITIAL_CAPITAL, config.TRADING_FEE)
        optimized_strategy = optimize_strategy(preprocessed_data, backtest_results)

    elif args.mode == 'live_trading':
        # 3. Set up risk management
        stop_loss = set_stop_loss(config.STOP_LOSS_PERCENTAGE)
        take_profit = set_take_profit(config.TAKE_PROFIT_PERCENTAGE)

        # 4. Connect to exchange and authenticate
        exchange = connect_to_exchange(config.BYBIT_API_KEY, config.BYBIT_SECRET_KEY, config.USE_TESTNET)

        # 5. Execute trading strategy
        while True:
            signals = generate_trading_signals(preprocessed_data)
            for signal in signals:
                order = create_order(exchange, signal)
                manage_positions(exchange, order)

            # 6. Monitor and log trades
            log_trades(exchange)
            generate_reports(exchange)

if __name__ == '__main__':
    main()
