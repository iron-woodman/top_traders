import argparse
import random
from time import sleep, time
import datetime

import src.database.db_functions as db_functions
import src.api.binance_api as binance_api
import src.trades.trades_functions as checks
from src.messages.profit_message import send_message
from src.database.db_functions import get_closed_trade, get_traders
from src.utils.config_handler import config

parser = argparse.ArgumentParser(description='Binance Top Traders Deals')
parser.add_argument('--config', type=str, default='config/config.ini', help='Path to the config file')
args = parser.parse_args()
config.read(args.config)

top200 = []


# t.me/top_traders_bot
def main():
    for trader_id, trader_name in top200:
        trades = binance_api.fetch_trader_trades(trader_id)
        stored_trades = db_functions.get_trades(trader_id)
        checks.check_opened_trades(trades, stored_trades, trader_name, trader_id)
        checks.check_closed_trades(trades, stored_trades, trader_name)
        sleep(random.uniform(1.1, 2.1))


if __name__ == "__main__":
    try:
        working = True
        top200 = get_traders()
        last_print_time = time()
        current_date = datetime.datetime.now()

        print(f"[{current_date.strftime('%d-%m-%Y %H:%M:%S')}] [i] Bot is running. Total trades stored : " + str(
            db_functions.count_total_trades()))

        while working is True:
            current_date = datetime.datetime.now()
            closed_trades = get_closed_trade()
            if current_date.hour == 19 and current_date.minute == 00 and working is True:
                print("Time to close")
                send_message()
                # working = False
                # break
            current_time = time()
            if current_time - last_print_time >= 1800 and working is True:
                last_print_time = current_time
                # Format [DD-MM-YYYY HH:MM:SS]
                print(
                    f"[{current_date.strftime('%d-%m-%Y %H:%M:%S')}] [i] Bot is running. Total trades stored : " + str(
                        db_functions.count_total_trades()))
                top200 = get_traders()
            if working is True:
                main()
                sleep(random.uniform(10.1, 20.1))

    except KeyboardInterrupt:
        print("Exiting")
