import os

from dotenv import load_dotenv
from telebot import TeleBot

from core import Downloader


load_dotenv()

Token = os.getenv('TOKEN')

if not Token:
    raise ValueError("No TOKEN provided. Please set the TOKEN environment variable.")

bot = TeleBot(Token)

downloader_bot = Downloader(bot)

if __name__ == "__main__":
    print("The bot is Running ...")
    downloader_bot.run_bot()