# Wallpapers module by @TheRealPhoenix using wall.alphacoders.com

from random import choice
from time import sleep
from urllib.parse import quote

import requests as r
from telegram import Message, Chat, Update, Bot
from telegram.ext import run_async

from tg_bot import dispatcher, WALL_API
from tg_bot.modules.disable import DisableAbleCommandHandler


@run_async
def wall(bot: Bot, update: Update, args):
    chat_id = update.effective_chat.id
    msg = update.effective_message
    msg_id = update.effective_message.message_id
    query = " ".join(args)
    if not query:
        msg.reply_text("Please enter a query!")
        return
    else:
        caption = query
        term = quote(caption)
        json_rep = r.get(f"https://wall.alphacoders.com/api2.0/get.php?auth={WALL_API}&method=search&term={term}").json()
        if not json_rep.get("success"):
            msg.reply_text("Something went wrong...")
            return
        else:
            wallpapers = json_rep.get("wallpapers")
            if not wallpapers:
                msg.reply_text("No results found!")
                return
            else:
                wallpaper = choice(wallpapers)
                wallpaper = wallpaper.get("url_image")
                wallpaper = wallpaper.replace("\\", "")
                bot.send_photo(chat_id, photo=wallpaper, caption='Preview',
                reply_to_message_id=msg_id, timeout=60)
                bot.send_document(chat_id, document=wallpaper,
                filename='wallpaper', caption=caption, reply_to_message_id=msg_id,
                timeout=60)
                    
            
            
WALLPAPER_HANDLER = DisableAbleCommandHandler("wall", wall, pass_args=True)

dispatcher.add_handler(WALLPAPER_HANDLER)