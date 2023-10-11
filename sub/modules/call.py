#
# Copyright (C) 2023 by stereoproject
# All rights reserved.

from pyrogram import filters
from pyrogram.types import *
import os
from sub import bot
from sub.config import BOT_ID, ADMINS
from sub.modules.data import *

ppk = [
    [
        InlineKeyboardButton("ᴄʜᴀɴɴᴇʟ ᴅᴀᴛᴀʙᴀꜱᴇ", callback_data="ch_base"),
    ],
    [
        InlineKeyboardButton("ᴀᴅᴍɪɴ", callback_data="admin_jan"),
    ],
    [
        InlineKeyboardButton("ꜰᴏʀᴄᴇ ꜱᴜʙ", callback_data="sub_jan"),
    ],
]

admin = [
    [
        InlineKeyboardButton("ᴀᴅᴍɪɴ ➕", callback_data="admin_plus"),
        InlineKeyboardButton("ᴀᴅᴍɪɴ ➖", callback_data="admin_min"),
    ],
    [
        InlineKeyboardButton("❮ ᴋᴇᴍʙᴀʟɪ", callback_data="setting_cok"),
    ],
]

sub = [
    [
        InlineKeyboardButton("ꜰᴏʀᴄᴇ ꜱᴜʙ ➕", callback_data="sub_plus"),
        InlineKeyboardButton("ꜰᴏʀᴄᴇ ꜱᴜʙ ➖", callback_data="sub_min"),
    ],
    [
        InlineKeyboardButton("❮ ᴋᴇᴍʙᴀʟɪ", callback_data="setting_cok"),
    ],
]


@bot.on_callback_query(filters.regex("setting_cok"))
async def setting_jancok(c, query):
    await query.message.edit(
        "Anda sedang berada di setting, Silahkan pilih menu di bawah ini",
        reply_markup=InlineKeyboardMarkup(ppk),
    )


@bot.on_callback_query(filters.regex("admin_jan"))
async def admin_jancok(c, query):
    msg = "<b><u>👤Daftar Admin Anda</u></b>\n\n"
    adm = await cek_admin(c.me.id)
    if adm is False:
        return await query.message.edit(
            "<b>Belum ada daftar Admin</b>", reply_markup=InlineKeyboardMarkup(admin)
        )
    ang = 0
    for ex in adm:
        try:
            afa = f"`{ex['admin']}`"
            ang += 1
        except Exception:
            continue
        msg += f"{ang} › {afa}\n"
    await query.message.edit(msg, reply_markup=InlineKeyboardMarkup(admin))


@bot.on_callback_query(filters.regex("admin_plus"))
async def admin_pluscok(c, query):
    await query.message.delete()
    admin = await c.ask(
        query.from_user.id,
        "<b>Kirimkan user ID yang akan di jadikan admin bot, klik /cancel untuk membatalkan</b>",
        filters.text,
    )
    if await jembut(c, query, admin.text):
        return
    try:
        admin_text = int(admin.text)
    except ValueError:
        return await c.send_message(
            query.from_user.id,
            "<b>Terjadi kesalahan, Silahkan pilih tombol di bawah</b>",
            reply_markup=InlineKeyboardMarkup(admin),
        )
    adm = await admin_info(c.me.id, admin_text)
    if not adm:
        await add_admin(int(c.me.id), admin_text)
        await c.send_message(
            query.from_user.id,
            f"{admin_text} Telah di tambahkan jadi Admin",
            reply_markup=InlineKeyboardMarkup(admin),
        )
    else:
        await c.send_message(
            query.from_user.id,
            f"{admin_text} Adalah bagian dari Admin",
            reply_markup=InlineKeyboardMarkup(admin),
        )


@bot.on_callback_query(filters.regex("admin_min"))
async def admin_mincok(c, query):
    await query.message.delete()
    admin = await c.ask(
        query.from_user.id,
        "<b>Kirimkan user ID yang akan di hapus dari admin bot, klik /cancel untuk membatalkan</b>",
        filters.text,
    )
    if await jembut(c, query, admin.text):
        return
    try:
        admin_text = int(admin.text)
    except ValueError:
        return await c.send_message(
            query.from_user.id,
            "<b>Terjadi kesalahan, Silahkan pilih tombol di bawah</b>",
            reply_markup=InlineKeyboardMarkup(admin),
        )
    adm = await admin_info(c.me.id, admin_text)
    if adm:
        await del_admin(int(c.me.id), admin_text)
        await c.send_message(
            query.from_user.id,
            f"{admin_text} Telah di dihapus dari Admin",
            reply_markup=InlineKeyboardMarkup(admin),
        )
    else:
        await c.send_message(
            query.from_user.id,
            f"{admin_text} Bukan bagian dari Admin",
            reply_markup=InlineKeyboardMarkup(admin),
        )


@bot.on_callback_query(filters.regex("sub_jan"))
async def jan_sub_bot(c, query):
    msg = "<b><u>💎Daftar Fsub Anda</u></b>\n\n"
    adm = await get_subs(c.me.id)
    if adm is False:
        return await query.message.edit(
            "<b>Belum ada daftar Fsub</b>", reply_markup=InlineKeyboardMarkup(sub)
        )
    ang = 0
    for ex in adm:
        try:
            jj = await c.get_chat(ex["sub"])
            afa = f"`{jj.id}` | {jj.title}"
            ang += 1
        except Exception:
            continue
        msg += f"{ang} › {afa}\n"
    await query.message.edit(msg, reply_markup=InlineKeyboardMarkup(sub))


@bot.on_callback_query(filters.regex("sub_plus"))
async def sub_pluscok(c, query):
    x = await get_subs(c.me.id)
    s = await max_info(c.me.id)
    if len(x) == s:
        return await query.message.edit(f"⚠️ <b>Maaf batas fsub anda hanya {s}, jika ingin mengganti dengan fsub lain silahkan hapus salah satu, atau jika anda ingin menambah fsub lebih dari {s} silahkan hubungi seller</b>", reply_markup=InlineKeyboardMarkup(sub),)
    await query.message.delete()
    subs = await c.ask(
        query.from_user.id,
        "<b>Kirimkan ID yang akan di jadikan Forcesub grup atau channel, klik /cancel untuk membatalkan</b>",
        filters.text,
    )
    if await jembut(c, query, subs.text):
        return
    sub_text = int(subs.text)
    adm = await sub_info(c.me.id, sub_text)
    if not adm:
        try:
            await c.export_chat_invite_link(sub_text)
            await add_sub(int(c.me.id), sub_text)
            await c.send_message(
                query.from_user.id,
                f"{sub_text} Telah di tambahkan ke Sub",
                reply_markup=InlineKeyboardMarkup(sub),
            )
        except:
            return await c.send_message(
                query.from_user.id,
                f"Maaf saya bukan admin di `{sub_text}`",
                reply_markup=InlineKeyboardMarkup(sub),
            )
    else:
        await c.send_message(
            query.from_user.id,
            f"{sub_text} Adalah bagian dari Fsub",
            reply_markup=InlineKeyboardMarkup(sub),
        )


@bot.on_callback_query(filters.regex("sub_min"))
async def sub_mincok(c, query):
    await query.message.delete()
    subs = await c.ask(
        query.from_user.id,
        "<b>Kirimkan ID yang akan di hapus dari forcesub, klik /cancel untuk membatalkan</b>",
        filters.text,
    )
    if await jembut(c, query, subs.text):
        return
    sub_text = int(subs.text)
    adm = await sub_info(c.me.id, sub_text)
    if adm:
        await del_sub(int(c.me.id), sub_text)
        await c.send_message(
            query.from_user.id,
            f"{sub_text} Telah di dihapus dari Fsub",
            reply_markup=InlineKeyboardMarkup(sub),
        )
    else:
        await c.send_message(
            query.from_user.id,
            f"{sub_text} Bukan bagian dari Fsub",
            reply_markup=InlineKeyboardMarkup(sub),
        )


@bot.on_callback_query(filters.regex("ch_base"))
async def ch_base_asu(c, query):
    await query.message.delete()
    base = await c.ask(
        query.from_user.id,
        "<b>Kirimkan ID yang akan di jadikan channel database, klik /cancel untuk membatalkan</b>",
        filters.text,
    )
    if await jembut(c, query, base.text):
        return
    ids = int(base.text)
    try:
        await c.export_chat_invite_link(ids)
        await add_owner(
            int(c.me.id),
            int(query.from_user.id),
            int(ids),
        )
        await c.send_message(
            query.from_user.id,
            f"Channel database berhasil di set `{ids}`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("❮ ᴋᴇᴍʙᴀʟɪ", callback_data="setting_cok"),
                    ]
                ]
            ),
        )
    except:
        return await c.send_message(
            query.from_user.id,
            f"Maaf saya bukan admin di `{ids}`",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("❮ ᴋᴇᴍʙᴀʟɪ", callback_data="setting_cok"),
                    ]
                ]
            ),
        )


@bot.on_message(filters.command("setting") & filters.private)
async def setting_text(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    await m.reply(
        "<b>Anda sedang berada di setting, Silahkan pilih menu di bawah ini</b>",
        reply_markup=InlineKeyboardMarkup(ppk),
    )


async def jembut(c, query, text):
    if text.startswith("/"):
        await c.send_message(
            query.from_user.id,
            "<b>Proses di batalkan, silahkan coba lagi</b>",
            reply_markup=InlineKeyboardMarkup(ppk),
        )
        return True
    else:
        return False

@bot.on_message(filters.command("cekbot"))
async def cekbot_text(c, m):
    if c.me.id != BOT_ID:
        return
    iya = await seller_info(m.from_user.id)
    if not iya and m.from_user.id not in ADMINS:
        return
    msg = "<u><b>Iki Infone Jancok</b></u>\n\n"
    num = 0
    for b in bot._bot:
        if b.me.id != bot.me.id:
            xx = await cek_owner(b.me.id)
            ex = await timer_info(b.me.id)
            mx = await max_info(b.me.id)
            for x in xx:
                ow = x["owner"]
        try:
            if b.me.id == bot.me.id:
                ppk = f"┣ <b>Nama Bot:</b> {b.me.first_name}\n┣ <b>UserName Bot:</b> @{b.me.username}\n┗ <b>ID Bot:</b> {b.me.id}\n\n"
            else:
                ppk = f"┣ <b>Nama Bot:</b> {b.me.first_name}\n┣ <b>UserName Bot:</b> @{b.me.username}\n┣ <b>ID Bot:</b> {b.me.id}\n┣ <b>Expired:</b> {ex}\n┣ <b>Max Sub:</b> {mx}\n┗ <b>ID Pembuat:</b> {ow}\n\n"
            num += 1
        except:
            continue
        msg += f"<b>{num}. Bot Yang Aktif</b>\n{ppk}"
    if len(msg) > 4000:
        names = "fsub.txt"
        with open(names, "w+", encoding="utf8") as out_file:
            out_file.write(msg)
        await m.reply_document(names)
        os.remove(names)
    else:
        await m.reply(msg)
