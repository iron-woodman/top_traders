## -*- coding: utf-8 -*-
import logging

import requests
from time import sleep
from src.utils.config_handler import telegram_config
import src.utils.logs as custom_logging


def handle_telegram_response(response):
    if response.status_code == 200:
        return None
    else:
        print("Error during message sending : " + response.text)
        if 'parameters' in response.json():
            if 'retry_after' in response.json()['parameters']:
                retry_after = response.json()['parameters']['retry_after']
                print(f"Retry after {retry_after} seconds")
                return retry_after
            else:
                custom_logging.add_log(
                    f"Unhandled Telegram error during message sending. Telegram response: {response.text}",
                    level=logging.ERROR)
                # raise Exception("Unhandled Telegram error during message sending")
        else:
            custom_logging.add_log(
                f"Unhandled Telegram error during message sending. Telegram response: {response.text}",
                level=logging.ERROR)
            # raise Exception("Unhandled Telegram error during message sending")


def send_telegram_message(chat_id, message_text, reply_to_message_id=None, disable_notification=False, parse_mode=None,
                          protect_content=True):
    params = {
        'chat_id': chat_id,
        'text': message_text,
        'protect_content': protect_content,
        'disable_notification': disable_notification
    }

    if reply_to_message_id:
        params['reply_to_message_id'] = reply_to_message_id
        params['allow_sending_without_reply'] = True

    if parse_mode:
        params['parse_mode'] = parse_mode

    while True:
        response = requests.get(f"https://api.telegram.org/bot{format(telegram_config['bot_api_key'])}/sendMessage",
                                params)
        retry_after = handle_telegram_response(response)

        if retry_after is None:
            return response.json()['result']['message_id']
        else:
            sleep(retry_after)
