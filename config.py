import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

date = {
    'bot_username': "_bot",
    'link_bot': "https://t.me/_bot",
    'BOT_TOKEN': os.getenv("BOT_TOKEN"),
    'OWM_API_KEY': os.getenv("OWM_API_KEY"),
    'PRIVAT_24_API_KEY': os.getenv("PRIVAT_24_API_KEY")
}
