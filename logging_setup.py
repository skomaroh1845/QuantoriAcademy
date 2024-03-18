import logging
import os
import telebot


TG_BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("ADMIN_ID")

logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s >> %(levelname)s >> %(message)s >> %(asctime)s",
    datefmt='%H:%M:%S %d.%m.%Y'
)

main_formatter = logging.Formatter(
    "%(filename)s >> %(levelname)s >> %(message)s >> %(asctime)s",
    datefmt='%H:%M:%S %d.%m.%Y'
)

class TgBotHandler(logging.Handler):
    """Handler to send telegram messages using bot"""
    def __init__(self, api_key: str, chat_id: str):
        super().__init__()
        self.api_key = api_key
        self.chat_id = chat_id

    def emit(self, record: logging.LogRecord):
        """Sends message to chat specified in .env file"""
        bot = telebot.TeleBot(self.api_key)

        bot.send_message(
            self.chat_id,
            self.format(record)
        )


class BedTimeFilter(logging.Filter):
    """Base class to filter whether or not message should be logged"""

    def filter(self, record):
        """No alarms after a bed time (cool guys go to sleep after 8 pm)"""
        return not (int(record.asctime.split(' ')[0].split(':')[0]) > 20)


console = logging.StreamHandler()
console.setLevel(logging.WARNING)
console.setFormatter(main_formatter)
console.addFilter(BedTimeFilter())

file = logging.FileHandler(filename="errors.log", mode="w")
file.setLevel(logging.ERROR)
file.setFormatter(main_formatter)

telegram = TgBotHandler(TG_BOT_TOKEN, CHAT_ID)
telegram.setLevel(logging.CRITICAL)
telegram.setFormatter(main_formatter)
telegram.addFilter(BedTimeFilter())

root_logger = logging.getLogger()
root_logger.addHandler(console)
root_logger.addHandler(file)
root_logger.addHandler(telegram)

# logging.critical('something goes wrong')
# logging.error('something goes wrong')
# logging.warning('something goes wrong')
# logging.debug('something goes wrong')
# logging.info('something goes wrong')
