import argparse
from time import sleep, time

import src.database.db_functions as db_functions
import src.api.binance_api as binance_api
from src.utils.config_handler import config


parser = argparse.ArgumentParser(description='Binance Top Traders Deals')
parser.add_argument('--config', type=str, default='config/config.ini', help='Path to the config file')
args = parser.parse_args()
config.read(args.config)

top200 = []


if __name__ == "__main__":
     try:
         print("******************* GET  ROI TOP TRADERS***********************")
         top_traders_ROI = binance_api.fetch_top_traders(100, statisticsType="ROI")

         for trader in top_traders_ROI:
             db_functions.insert_trader(trader[0], trader[1]) # ID, Nickname

         sleep(2)

         print("******************* GET PNL TOP TRADERS***********************")
         top_traders_PNL = binance_api.fetch_top_traders(100, statisticsType="PNL")

         for trader in top_traders_PNL:
             if trader not in top_traders_ROI:
                db_functions.insert_trader(trader[0], trader[1]) # ID, Nickname
         print('Top traders stored to DB.')
     except KeyboardInterrupt:
        print("Exiting")