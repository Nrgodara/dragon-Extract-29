import os
from config import Config
from pyrogram import Client, idle
import asyncio, logging
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

# Configure logging
LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "log.txt", maxBytes=5000000, backupCount=10
        ),
        logging.StreamHandler(),
    ],
)

# Auth Users
AUTH_USERS = [int(chat) for chat in Config.AUTH_USERS.split(",") if chat != '']

# Prefixes 
prefixes = ["/", "~", "?", "!"]

plugins = dict(root="plugins")

class MyClient(Client):
    async def start(self, *args, **kwargs):
        await super().start(*args, **kwargs)
        
        # Manually adjust time to local time zone
        local_time_offset = timedelta(hours=5, minutes=30)  # Adjust for GMT+5:30
        await self.set_time_offset(local_time_offset.total_seconds())

if __name__ == "__main__":
    bot = MyClient(
        "StarkBot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=20,
        plugins=plugins,
        workers=50
    )
    
    async def main():
        await bot.start()
        bot_info = await bot.get_me()
        LOGGER.info(f"<--- @{bot_info.username} Started (c) STARKBOT --->")
        await idle()
    
    asyncio.get_event_loop().run_until_complete(main())
    LOGGER.info("<--- Bot Stopped --->")
