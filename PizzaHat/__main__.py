import os

from core.bot import PizzaHat
from dotenv import load_dotenv
import core.bot as bot_core

load_dotenv()

logger = bot_core.logging.getLogger("bot")

if __name__ == "__main__":
    bot = PizzaHat()
    bot.run(os.getenv("TOKEN"), root_logger=True)  # type: ignore
