#
# Copyright (C) 2023 by stereoproject
# 
# All rights reserved.


from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton

from sub.modules.data import *


async def start_button(c):
    keyboard = []
    temp = []
    new_keyboard = []
    new_keyboard.append(
        [
            InlineKeyboardButton(
                text="ᴛᴇɴᴛᴀɴɢ sᴀʏᴀ",
                callback_data="tentang",
            )
        ]
    )
    for x in await get_subs(c.me.id):
        info = await c.get_chat(x["sub"])
        text_btn = (
            'ɢʀᴏᴜᴘ' if info.type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP
            ]
            else 'ᴄʜᴀɴɴᴇʟ' if info.type == ChatType.CHANNEL
            else 'ᴊᴏɪɴ ᴅᴜʟᴜ'
        )
        if info.username:
            link = f'https://t.me/{info.username}'
        if info.invite_link:
            link = info.invite_link
        else:
            link = await c.export_chat_invite_link(x["sub"])
        keyboard.append(InlineKeyboardButton(text_btn, url=link))
    for i, board in enumerate(keyboard, start=1):
        temp.append(board)
        if i % 2 == 0:
            new_keyboard.append(temp)
            temp = []
        if i == len(keyboard):
            new_keyboard.append(temp)
    try:
        new_keyboard.append(
            [
                InlineKeyboardButton(
                    "ᴛᴜᴛᴜᴘ",
                    callback_data="tutup",
                )
            ]
        )
    except IndexError:
        pass
    return new_keyboard


async def fsub_button(c, m):
    keyboard = []
    temp = []
    new_keyboard = []
    for x in await get_subs(c.me.id):
        info = await c.get_chat(x["sub"])
        text_btn = (
            'ɢʀᴏᴜᴘ' if info.type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP
            ]
            else 'ᴄʜᴀɴɴᴇʟ' if info.type == ChatType.CHANNEL
            else 'ᴊᴏɪɴ ᴅᴜʟᴜ'
        )
        if info.username:
            link = f'https://t.me/{info.username}'
        if info.invite_link:
            link = info.invite_link
        else:
            link = await c.export_chat_invite_link(x["sub"])
        keyboard.append(InlineKeyboardButton(text_btn, url=link))
    for i, board in enumerate(keyboard, start=1):
        temp.append(board)
        if i % 2 == 0:
            new_keyboard.append(temp)
            temp = []
        if i == len(keyboard):
            new_keyboard.append(temp)
    try:
        new_keyboard.append(
            [
                InlineKeyboardButton(
                    "ᴄᴏʙᴀ ʟᴀɢɪ",
                    url=f"https://t.me/{c.me.username}?start={m.command[1]}",
                )
            ]
        )
    except IndexError:
        pass
    return new_keyboard
