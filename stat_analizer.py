## -*- coding: utf-8 -*-
import mysql.connector
from src.utils.config_handler import database_config, settings_config
from contextlib import contextmanager


@contextmanager
def get_connection():
    conn = mysql.connector.connect(
        host        =   database_config['host'],
        user        =   database_config['user'],
        password    =   database_config['password'],
        database    =   database_config['database'],
        auth_plugin =   database_config['auth_plugin']
        )
    try:
        yield conn
    finally:
        conn.close()


def get_winning_losing_trades():
    """
    Get all winning and losing trades from the database
    """
    with get_connection() as conn:
        cursor = conn.cursor(buffered=True)
        cursor.execute("SELECT * FROM all_trades WHERE profit > 0 ORDER BY profit DESC;")
        winning_trades = cursor.fetchall()
        cursor.execute("SELECT * FROM all_trades WHERE profit < 0 ORDER BY profit ASC;")
        losing_trades = cursor.fetchall()
        return [winning_trades,losing_trades]


def main():
    trades = get_winning_losing_trades()
    winning_trades = []
    losing_trades = []

    for trade in trades[0]:
        winning_trades.append({'message_id': trade[4], 'pair': trade[1], 'opened': trade[2], 'closed': trade[3],
                               'profit': round(trade[5], 3)})
    for trade in trades[1]:
        losing_trades.append({'message_id': trade[4], 'pair': trade[1], 'opened': trade[2], 'closed': trade[3],
                              'profit': round(trade[5], 3)})

    return ([winning_trades, losing_trades])

if __name__ == "__main__":
    main()