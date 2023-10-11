#
# Copyright (C) 2023 by t.me/stereoproject
# All rights reserved.

import importlib
from sys import version as pyver

from pyrogram import __version__ as pyrover
from pyrogram import idle
from pyrogram.errors import RPCError

from sub import LOOP, Bot, bot
from sub.config import LOG_GRP
from sub.modules import ALL_MODULES
from sub.modules.data import get_bot, remove_bot

msg = """
🔥**Bot Multisub Berhasil Di Aktifkan**
━━
➠ **Python Version** > `{}`
➠ **Pyrogram Version** > `{}`
━━
"""


async def main():
    await bot.start()

    for bt in await get_bot():
        b = Bot(**bt)
        try:
            await b.start()
            print(f"{b.me.first_name} Telah aktif")
        except RPCError:
            await remove_bot(bt["name"])
            print(f"✅ {bt['name']} Berhasil Dihapus Dari Database")
    for all_module in ALL_MODULES:
        importlib.import_module(f"sub.modules.{all_module}")
    print(f"[🤖 @{bot.me.first_name} 🤖] [🔥 BERHASIL DIAKTIFKAN! 🔥]")
    await bot.send_message(LOG_GRP, msg.format(pyver.split()[0], pyrover))
    await idle()


if __name__ == "__main__":
    print("Starting sub Bot")
    LOOP.run_until_complete(main())

