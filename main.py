# (c) @AbirHasan2005

import os
from configs import Configs
from pyromod import listen
from asyncio import TimeoutError
from core.steps import StartSteps
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

app = Client(
    session_name=Configs.SESSION_NAME,
    api_id=Configs.API_ID,
    api_hash=Configs.API_HASH,
    bot_token=Configs.BOT_TOKEN
)


@app.on_message(filters.command("start") & filters.private & ~filters.edited)
async def start_command(_, m: Message):
    await m.reply_text("Hi, I am Heroku app.json maker bot.\n\n"
                       "To start making app.json for your heroku app,\n"
                       "Press /f", quote=True, disable_web_page_preview=True)


@app.on_message(filters.command("f") & ~filters.edited & filters.private)
async def f_command(bot: Client, m: Message):
    editable = await m.reply_text("Please wait ...",
                                  reply_markup=InlineKeyboardMarkup([
                                      [InlineKeyboardButton("Cancel Process", callback_data="cancelProcess")]
                                  ]))
    try:
        app_json = await StartSteps(bot, editable)
        if os.path.exists(app_json):
            await bot.send_document(
                chat_id=m.chat.id,
                document=app_json,
                caption="(c) @AbirHasan2005"
            )
            await editable.edit("Sent `app.json` !!")
            os.remove(app_json)
        else:
            await editable.edit("Failed to Make `app.json` !!\n\n"
                                "Try again.")
    except TimeoutError:
        pass


@app.on_callback_query()
async def cb_handler(_, cb: CallbackQuery):
    if "cancelProcess" in cb.data:
        await cb.message.edit("Process Cancelled!")


app.start()
print("Bot Started!")
idle()
app.stop()
print("Bot Stopped!")
