from aiogram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = Bot(TOKEN)