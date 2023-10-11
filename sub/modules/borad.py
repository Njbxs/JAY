#
# Copyright (C) 2023 by stereoproject
# All rights reserved.

import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked

from sub import bot
from sub.config import *
from sub.modules.data import *

from .func import expired


@bot.on_message(filters.command("users") & filters.private)
@expired()
async def get_users(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    adm = await admin_info(c.me.id, m.from_user.id)
    for i in cek:
        owner = i["owner"]
    if not adm and m.from_user.id != owner:
        return
    msg = await c.send_message(m.chat.id, "<code>Silahlan Tunggu ...</code>")
    users = await get_user(c.me.id)
    await msg.edit(f"{len(users)} <b>Pengguna yang menggunakan bot ini</b>")


@bot.on_message(filters.command("buser") & filters.private & filters.user(ADMINS))
async def get_users(c, m):
    if c.me.id != BOT_ID:
        return
    msg = await c.send_message(m.chat.id, "<code>Silahlan Tunggu ...</code>")
    users = await get_user(c.me.id)
    await msg.edit(f"{len(users)} <b>Pengguna yang menggunakan bot ini</b>")


@bot.on_message(filters.private & filters.command("broadcast"))
@expired()
async def send_text(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    adm = await admin_info(c.me.id, m.from_user.id)
    for i in cek:
        owner = i["owner"]
    if not adm and m.from_user.id != owner:
        return
    if not m.reply_to_message:
        return await m.reply("<code>Gunakan Perintah ini Harus Sambil Reply ke pesan telegram yang ingin di Broadcast.</code>")
    elif m.reply_to_message:
        query = await get_user(c.me.id)
        broadcast_msg = m.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await m.reply("<code>Broadcasting Message, Silahkan Tunggu Sebentar...</code>")
        for x in query:
            chat_id = x["user"]
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(c.me.id, chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(c.me.id, chat_id)
                deleted += 1
            except:
                unsuccessful += 1
            total += 1
        status = f"""<b><u>Berhasil Broadcast</u>
Jumlah Pengguna: <code>{total}</code>
Berhasil: <code>{successful}</code>
Gagal: <code>{unsuccessful}</code>
Pengguna diblokir: <code>{blocked}</code>
Akun Terhapus: <code>{deleted}</code></b>"""
        return await pls_wait.edit(status)
    else:
        msg = await m.reply("<code>Gunakan Perintah ini Harus Sambil Reply ke pesan telegram yang ingin di Broadcast.</code>")
        await asyncio.sleep(8)
        await msg.delete()


@bot.on_message(filters.private & filters.command("gcast") & filters.user(ADMINS))
async def send_text(c, m):
    if c.me.id != BOT_ID:
        return
    if not m.reply_to_message:
        return await m.reply("<code>Gunakan Perintah ini Harus Sambil Reply ke pesan telegram yang ingin di Broadcast.</code>")
    elif m.reply_to_message:
        query = await get_user(c.me.id)
        broadcast_msg = m.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await m.reply("<code>Broadcasting Message, Silahkan Tunggu Sebentar...</code>")
        for x in query:
            chat_id = x["user"]
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(c.me.id, chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(c.me.id, chat_id)
                deleted += 1
            except:
                unsuccessful += 1
            total += 1
        status = f"""<b><u>Berhasil Broadcast</u>
Jumlah Pengguna: <code>{total}</code>
Berhasil: <code>{successful}</code>
Gagal: <code>{unsuccessful}</code>
Pengguna diblokir: <code>{blocked}</code>
Akun Terhapus: <code>{deleted}</code></b>"""
        return await pls_wait.edit(status)
    else:
        msg = await m.reply("<code>Gunakan Perintah ini Harus Sambil Reply ke pesan telegram yang ingin di Broadcast.</code>")
        await asyncio.sleep(8)
        await msg.delete()


@bot.on_message(filters.command("addadmin"))
@expired()
async def add_admin_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "<b>Silahkan kombinasikan dengan id\ncontoh : /addadmin 883761960</b>"
        )
    ids = int(m.command[1])
    adm = await admin_info(c.me.id, ids)
    if not adm:
        await add_admin(int(c.me.id), ids)
        await m.reply(f"{ids} Telah di tambahkan jadi Admin")
    else:
        await m.reply(f"{ids} Adalah bagian dari Admin")


@bot.on_message(filters.command("deladmin"))
@expired()
async def del_admin_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "<b>Silahkan kombinasikan dengan id\ncontoh : /deladmin 883761960</b>"
        )
    ids = int(m.command[1])
    adm = await admin_info(c.me.id, ids)
    if adm:
        await del_admin(int(c.me.id), ids)
        await m.reply(f"{ids} Telah di dihapus dari Admin")
    else:
        await m.reply(f"{ids} Bukan bagian dari Admin")


@bot.on_message(filters.command("cekadmin"))
@expired()
async def cek_admin_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    msg = "**Daftar Admin**\n\n"
    adm = await cek_admin(c.me.id)
    if adm is False:
        return await m.reply("Belum ada daftar Admin")
    ang = 0
    for ex in adm:
        try:
            afa = f"`{ex['admin']}`"
            ang += 1
        except Exception:
            continue
        msg += f"{ang} › {afa}\n"
    await m.reply(msg)


@bot.on_message(filters.command("adsel") & filters.user(ADMINS))
async def add_seller_sub(c, m):
    if c.me.id != BOT_ID:
        return
    if len(m.command) < 2:
        return await m.reply(
            "<b>Silahkan kombinasikan dengan id\ncontoh : /adsel 883761960</b>"
        )
    ids = m.command[1]
    iya = await seller_info(int(ids))
    if not iya:
        await add_seller(int(ids))
        await m.reply(f"{ids} Berhasil di tambahkan ke daftar seller")
    else:
        await m.reply(f"{ids} Sudah menjadi seller")


@bot.on_message(filters.command("delsel") & filters.user(ADMINS))
async def del_seller_sub(c, m):
    if c.me.id != BOT_ID:
        return
    if len(m.command) < 2:
        return await m.reply(
            "<b>Silahkan kombinasikan dengan id\ncontoh : /delsel 883761960</b>"
        )
    ids = m.command[1]
    iya = await seller_info(int(ids))
    if iya:
        await del_seller(int(ids))
        await m.reply(f"{ids} Berhasil di hapus dari seller")
    else:
        await m.reply(f"{ids} Bukan bagian seller")


@bot.on_message(filters.private & filters.command("protect"))
@expired()
async def set_protect(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    adm = await admin_info(c.me.id, m.from_user.id)
    for i in cek:
        owner = i["owner"]
    if not adm and m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "<b>Silahkan kombinasikan dengan True atau False\ncontoh : /protect True</b>"
        )
    jk = m.command[1]
    if jk == "True":
        await add_protect(c.me.id, jk)
        await m.reply(f"Protect berhasil di set {jk}")
    elif jk == "False":
        await add_protect(c.me.id, jk)
        await m.reply(f"Protect berhasil di set {jk}")
    else:
        await m.reply(f"{jk} Salah ❌ Silahkan isi True atau False")


@bot.on_message(filters.command("addsub"))
@expired()
async def add_sub_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "<b>Silahkan kombinasikan dengan id\ncontoh : /addsub -100123456789</b>"
        )
    ids = int(m.command[1])
    adm = await sub_info(c.me.id, ids)
    x = await get_subs(c.me.id)
    s = await max_info(c.me.id)
    if len(x) == s:
        return await m.reply(f"Maaf batas Fsub anda hanya {s}, jika anda ingin mengganti dengan Fsub lain, silahkan hapus salah satu, atau jika anda ingin menambah Fsub lebih dari {s} Silahkan hubungi seller")
    if not adm:
        try:
            await c.export_chat_invite_link(ids)
            await add_sub(int(c.me.id), ids)
            await m.reply(f"{ids} Telah di tambahkan ke Sub")
        except:
            return await m.reply(f"Maaf saya bukan admin di `{ids}`")
    else:
        await m.reply(f"{ids} Adalah bagian dari Sub")


@bot.on_message(filters.command("delsub"))
@expired()
async def del_sub_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "<b>Silahkan kombinasikan dengan id\ncontoh : /delsub -100123456789</b>"
        )
    ids = int(m.command[1])
    adm = await sub_info(c.me.id, ids)
    if adm:
        await del_sub(int(c.me.id), ids)
        await m.reply(f"{ids} Telah di dihapus dari Fsub")
    else:
        await m.reply(f"{ids} Bukan bagian dari Fsub")


@bot.on_message(filters.command("ceksub"))
@expired()
async def cek_sub_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    msg = "<b><u>Daftar Fsub Saat Ini</u></b>\n\n"
    adm = await get_subs(c.me.id)
    if adm is False:
        return await m.reply("<b>Belum ada daftar Fsub</b>")
    ang = 0
    for ex in adm:
        try:
            jj = await c.get_chat(ex["sub"])
            afa = f"`{jj.id}` | {jj.title}"
            ang += 1
        except Exception:
            continue
        msg += f"{ang} › {afa}\n"
    await m.reply(msg)
