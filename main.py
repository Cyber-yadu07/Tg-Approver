from decouple import config

API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None) 
AUTH = config("AUTH", default=None, cast=int)
CHAT = config("CHAT", default=None, cast=int)

import os, asyncio, logging
from pyrogram import Client, filters, idle
from pyrogram.types import ChatJoinRequest
from pyrogram.errors import FloodWait, MessageNotModified

bot_client = Client("APPROVEBOT", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    datefmt="[%d/%m/%Y %H:%M:%S]",
    format=" %(asctime)s - [INDOAPPROVEBOT] >> %(levelname)s << %(message)s",
    handlers=[logging.FileHandler("indoapprovebot.log"), logging.StreamHandler()])

@bot_client.on_chat_join_request(filters.chat(CHAT))
async def approve(c: Client, m: ChatJoinRequest):
    if not m.from_user:
        return
    try:
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)
    except FloodWait as e:
        logging.info(f"Sleeping for {e.x + 2} seconds due to floodwaits!")
        await asyncio.sleep(e.x + 2)
        await c.approve_chat_join_request(m.chat.id, m.from_user.id)

@bot_client.on_message(filters.user(AUTH))
async def well_yes(c, m):
    await m.reply_text(f"{c.my_bot.username} is alive!")

async def run_bot_():
    await bot_client.start()
    bot_client.my_bot = await bot_client.get_me()
    logging.log(f"Started bot as : {bot_client.my_bot.username}")
    await idle()

if __name__ == "__main__":
    bot_client.loop.run_until_complete(run_bot_())
