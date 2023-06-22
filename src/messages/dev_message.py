from datetime import datetime

from src.utils.config_handler import telegram_config
from src.api.telegram import send_telegram_message

DEV_CHANNEL_ID = telegram_config['dev_channel_id']


class DevMessage:
    def __init__(self, message_text, message_type='INFO'):
        self.message_text = message_text
        self.message_type = message_type
        current_date = datetime.now()
        self.current_time = current_date.strftime('%d-%m-%Y %H:%M:%S')

    def generate_message(self):
        message = ''
        if self.message_type == 'INFO':
            message = f"⌛️{self.current_time}\n Info: {self.message_text}"
        elif self.message_type == 'ERROR':
            message = f"⌛️{self.current_time}\n Error: {self.message_text}"
        return message

    def send_message(self):
        message = self.generate_message()
        send_telegram_message(DEV_CHANNEL_ID, message, protect_content=False, parse_mode="Markdown")

