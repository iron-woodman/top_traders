import requests, requests.exceptions
import json
import random
from time import sleep
import logging
import src.database.db_functions as sql
import src.utils.logs as custom_logging
HEADERS = {
    'Content-Type': 'application/json'
}


def handle_error(trader_uid,e="Not provided"):
    print(f"Error while fetching trades for trader: {trader_uid}, Error : {e}")
    custom_logging.add_log(f"Error while fetching trades for trader: {trader_uid}, Error : {e}", logging.ERROR)

def fetch_top_traders(limit, trade_type="PERPETUAL", statisticsType="ROI"):
    """
    Fetch the top traders from Binance Futures.

    :param limit: The number of top traders to fetch
    :param trade_type: The type of trade, defaults to "PERPETUAL"
    :return: A list of top traders
    """

    traders = []
    url = "https://www.binance.com/bapi/futures/v3/public/future/leaderboard/getLeaderboardRank"
    payload = {
        "isShared": True,
        "isTrader": False,
        "periodType": "ALL", #"MONTHLY",
        "statisticsType": statisticsType, #"ROI" or "PNL"
        "tradeType": trade_type
    }
    headers = HEADERS

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    response_data = response.json()['data']
    for trader in response_data[:limit]:
        traders.append([trader['encryptedUid'], trader['nickName']])
    return traders

def fetch_trader_trades(trader_uid, trade_type="PERPETUAL"):
    """
    Fetch a list of trades for the given trader UID.

    :param trader_uid: The UID of the trader
    :param trade_type: The type of trade, defaults to "PERPETUAL"
    :return: A list of trades in JSON format
    """

    url = "https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition"
    payload = {
        "encryptedUid": trader_uid,
        "tradeType": trade_type
    }
    headers = HEADERS
    try:
        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    except requests.exceptions.RequestException as e:
        handle_error(trader_uid,e)
        return []

    if response.status_code != 200:
        handle_error(trader_uid, f"ответ сервера: {response.status_code}")
        sleep(random.uniform(7.6, 11.4))
        return fetch_trader_trades(trader_uid, trade_type)

    return response.json()['data']['otherPositionRetList']

def fetch_trader_info(trader_uid):
    """
    Fetch information about the trader with the given UID.

    :param trader_uid: The UID of the trader
    :return: Trader information in JSON format
    """

    url = "https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherLeaderboardBaseInfo"
    payload = {
        "encryptedUid": trader_uid
    }
    headers = HEADERS
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    trader_info = response.json()['data']

    sql.insert_trader(trader_info['encryptedUid'], trader_info['nickName'])
    return trader_info

def fetch_trader_username(trader_uid):
    """
    Fetch the trader's username using the given UID.

    :param trader_uid: The UID of the trader
    :return: The trader's username
    """

    url = "https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherLeaderboardBaseInfo"
    payload = {
        "encryptedUid": trader_uid
    }
    headers = HEADERS
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    trader_info = response.json()['data']

    return trader_info['nickName']
