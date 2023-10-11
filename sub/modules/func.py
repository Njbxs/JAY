#
# Copyright (C) 2023 by stereoproject
# All rights reserved.

import asyncio
import base64
import re
from datetime import datetime
from pykeyboard import InlineKeyboard
from typing import List

from pyrogram import Client, enums, filters
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from sub.config import *
from sub.modules.data import *


async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string


async def decode(base64_string):
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    string_bytes = base64.urlsafe_b64decode(base64_bytes)
    string = string_bytes.decode("ascii")
    return string


async def is_subscribed(filter, c, m):
    if c.me.id == BOT_ID:
        return True
    for ix in await cek_owner(c.me.id):
        admin = ix["owner"]
    links = []
    jembut = await get_subs(c.me.id)
    if not jembut:
        return True
    for v in jembut:
        li = v["sub"]
        links.append(li)
    user_id = m.from_user.id
    adm = await admin_info(c.me.id, user_id)
    if user_id == int(admin):
        return True
    if adm:
        return True
    try:
        for link in links:
            member = await c.get_chat_member(link, user_id)
    except UserNotParticipant:
        return False

    return member.status in [
        enums.ChatMemberStatus.OWNER,
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.MEMBER,
    ]


async def get_messages(c, message_ids):
    messages = []
    total_messages = 0
    for ix in await cek_owner(c.me.id):
        db = ix["channel"]
    while total_messages != len(message_ids):
        temb_ids = message_ids[total_messages : total_messages + 200]
        try:
            msgs = await c.get_messages(db, temb_ids)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await c.get_messages(db, temb_ids)
        except BaseException:
            pass
        total_messages += len(temb_ids)
        messages.extend(msgs)
    return messages


async def get_message_id(c, m):
    for ix in await cek_owner(c.me.id):
        db = ix["channel"]
    if m.forward_from_chat and m.forward_from_chat.id == db:
        return m.forward_from_message_id
    elif m.forward_from_chat or m.forward_sender_name or not m.text:
        return 0
    else:
        pattern = "https://t.me/(?:c/)?(.*)/(\\d+)"
        matches = re.match(pattern, m.text)
        if not matches:
            return 0
        channel_id = matches.group(1)
        msg_id = int(matches.group(2))
        if channel_id.isdigit():
            if f"-100{channel_id}" == str(db):
                return msg_id


def expired():
    def fsub(func):
        async def maxsub(c: Client, m: Message):
            if c.me.id != BOT_ID:
                exp = await timer_info(c.me.id)
                time = datetime.now().strftime("%d-%m-%Y")
                if exp in time:
                    user_id = m.from_user.id
                    jancok = await cek_seller()
                    if user_id not in MEMBER and user_id not in jancok:
                        for X in jancok:
                            await c.resolve_peer(X)
                        buttons = InlineKeyboard(row_width=3)
                        keyboard: List[InlineKeyboardButton] = []
                        but = []
                        for i in range(len(jancok)):
                            list_admin = f"⛑️ sᴇʟʟᴇʀ {i+1}"
                            id_admin = jancok[i]
                            keyboard.append(
                                InlineKeyboardButton(
                                    list_admin,
                                    user_id=id_admin,
                                )
                            )
                        but.append(InlineKeyboardButton("Tutup", callback_data="tutup"))
                        buttons.add(*keyboard + but)
                        await c.send_message(
                            chat_id=m.from_user.id,
                            text="<b>[INFO]</b> - Masa Aktif Bot Ini Sudah Habis.\nSilahkan Hubungi Seller Dibawah Ini Jika Anda Ingin Memperpanjang Masa Aktif.",
                            reply_markup=buttons
                        )
                        return
            await func(c, m)
        return maxsub
    return fsub


subcribe = filters.create(is_subscribed)
