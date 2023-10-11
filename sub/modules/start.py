#
# Copyright (C) 2023 by stereoproject
# All rights reserved.

import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta
from distutils.util import strtobool
from time import time

from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from pyrogram.types import *

from sub import Bot, bot
from sub.config import *
from sub.modules.btn import *
from sub.modules.data import *
from sub.modules.func import *


logs = logging.getLogger(__name__)


def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "sub"])


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60**2 * 24),
    ("hour", 60**2),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else "s"}')
    return ", ".join(parts)


start_msg = """
<b>Hallo {}, saya adalah {} 
yang mempermudah kalian untuk membuat file sharing bot 
tanpa harus memiliki vps/heroku sendiri
Silahkan klik tombol dibawah ini untuk memulainya\n\nNote : Jika kamu tidak bisa mendeploy sendiri, kamu bisa menghubungi salah satu admin yang tertera di bot ini</b>
"""

but_tutor = [
    [
        InlineKeyboardButton("🛡 ᴀʙᴏᴜᴛ 🛡", callback_data="about"),
    ],
    [
        InlineKeyboardButton("🎥 ᴛᴜᴛᴏʀɪᴀʟ", callback_data="tutor"),
        InlineKeyboardButton("ᴅᴇᴘʟᴏʏ 🤖", callback_data="deploy_fsub"),
    ],
    [
        InlineKeyboardButton("💬 ʟɪᴠᴇ ᴄʜᴀᴛ 💬", callback_data="support"),
    ],
]


@bot.on_message(filters.command("start") & filters.private & subcribe)
@expired()
async def start_bot(c, m):
    if c.me.id == BOT_ID:
        await add_user(c.me.id, m.from_user.id)
        await m.reply(
            start_msg.format(m.from_user.mention, c.me.mention),
            reply_markup=InlineKeyboardMarkup(but_tutor),
        )
        return
    '''
    av = await timer_info(c.me.id)
    time = datetime.now().strftime("%d-%m-%Y")
    if av == time:
        print(f"@{c.me.username} Telah habis Mohon Tunggu, Bot sedang direstart")
        await remove_bot(str(c.me.id))
        await del_timer(c.me.id)
        os.popen(f"rm {c.me.id}*")
        await restart()
    '''
    kk = await protect_info(c.me.id)
    kon = strtobool(kk)
    await add_user(c.me.id, m.from_user.id)
    for ix in await cek_owner(c.me.id):
        chg = ix["channel"]
    text = m.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except Exception:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(chg))
                end = int(int(argument[2]) / abs(chg))
            except BaseException:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
            temp_msg = await m.reply("<code>Silahkan Tunggu Sebentar...</code>")
            try:
                mes = await get_messages(c, ids)
            except BaseException:
                await m.reply("<b>Telah Terjadi Error </b>😥")
                return
            await temp_msg.delete()
            for msg in mes:
                caption = msg.caption.html if msg.caption else ""
                try:
                    await msg.copy(
                        m.chat.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        protect_content=kon,
                        reply_markup=None,
                    )
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(
                        m.chat.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        protect_content=kon,
                        reply_markup=None,
                    )
                except BaseException:
                    pass
        elif len(argument) == 2:
            try:
                ids = int(int(argument[1]) / abs(chg))
            except BaseException:
                return
            temp_msg = await m.reply("<code> Silahkan Tunggu Sebentar...</code>")
            try:
                mes = await c.get_messages(chg, ids)
            except BaseException:
                await m.reply("<b> Telah Terjadi Error </b>😥")
                return
            caption = mes.caption.html if mes.caption else ""
            await temp_msg.delete()
            await mes.copy(
                m.chat.id,
                caption=caption,
                parse_mode=ParseMode.HTML,
                protect_content=kon,
                reply_markup=None,
            )

    else:
        msgs = await get_start(c.me.id)
        if msgs:
            text = msgs
        else:
            text = "<b>Hello {user}\n\nAnda Harus Bergabung Di Channel / Grup Saya Terlebih Dahulu\n\nSilahkan Bergabung Channel Dan Jangan Keluar Lagi Dari Channel\n\nSetelah Bergabung Langsung Klik Coba Lagi Untuk Mendapatkan Media Dari Bot Ini .. .. ..</b>"
        try:
            buttons = await start_button(c)
            await m.reply(
                text.format(user=m.from_user.metion),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except:
            await m.reply(
                text.format(user=m.from_user.mention),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                    text="ᴛᴇɴᴛᴀɴɢ sᴀʏᴀ",
                    callback_data="tentang",
                )]])
            )

@bot.on_message(filters.command("start") & filters.private)
@expired()
async def start_bots(c, m):
    if c.me.id == BOT_ID:
        await add_user(c.me.id, m.from_user.id)
        await m.reply(
            start_msg.format(m.from_user.mention, c.me.mention),
            reply_markup=InlineKeyboardMarkup(but_tutor),
        )
        return
    '''
    av = await timer_info(c.me.id)
    time = datetime.now().strftime("%d-%m-%Y")
    if av == time:
        print(f"@{c.me.username} Telah habis Mohon Tunggu Sedang Restart Bot")
        await remove_bot(str(c.me.id))
        await del_timer(c.me.id)
        os.popen(f"rm {c.me.id}*")
        await restart()
    '''
    await add_user(c.me.id, m.from_user.id)
    buttons = await fsub_button(c, m)
    msgs = await get_start(c.me.id)
    if msgs:
        text = msgs
    else:
        text = "<b>Hello {user}\n\nAnda Harus Bergabung Di Channel / Grup Saya Terlebih Dahulu\n\nSilahkan Bergabung Channel Dan Jangan Keluar Lagi Dari Channel\n\nSetelah Bergabung Langsung Klik Coba Lagi Untuk Mendapatkan Media Dari Bot Ini .. .. ..</b>"
    try:
        await m.reply(
            text.format(user=m.from_user.mention),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception as e:
        print(e)


@bot.on_message(filters.command("id") & filters.private)
async def cek_id(c, m):
    if c.me.id != BOT_ID:
        return
    if len(m.command) < 2:
        return await m.reply_photo(
            "https://telegra.ph/file/86fff250dda1c1d9b14cb.jpg",
            caption="Silahkan kombinasikan dengan link tautan\ncontoh : /id https://t.me/stereoproject\natau\n/id https://t.me/c/728292989/77",
        )
    link = m.command[1]
    if not "t.me" in link:
        return await m.reply("Maaf link salah")
    if "t.me/c" in link:
        try:
            chat = int("-100" + str(link.split("/")[-2]))
            await m.reply(f"**ID**: `{chat}`")
        except Exception as e:
            return await m.reply(f"**Error**: {e}")
    else:
        xx = str(link.split("/")[-1])
        try:
            chat = await c.get_chat(xx)
            await m.reply(f"**ID**: `{chat.id}`")
        except Exception as e:
            return await m.reply(f"**Error**: {e}")


@bot.on_callback_query(filters.regex("about"))
async def about(_, callback_query):
    await callback_query.message.edit(
        text=f"<b><u>💎 PREMIUM FSUB BOT 💎</u></b>\n\nini adalah bot yang berfungsi untuk menciptakan bot file sharing atau bot fsub dengan mudah dan simple.\nDengan membuat file sharing melalui bot ini, anda mempunyai hak penuh atas bot anda sendiri (bisa broadcast, ganti² fsub, tambah admin dll) dan bisa melakukan perubahan setting langsung di bot..\n\n➲ support by - @RACUN_SHOPEE101\n➲ bot by - @{_.me.username}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("❮ Kembali", callback_data="back_start"),
                ]
            ]
        ),
    )


@bot.on_callback_query(filters.regex("tutor"))
async def tutor(_, callback_query):
    await callback_query.message.edit(
        text="<b>Silahkan ikuti tutorial dibawah ini</b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🛑 ᴀᴘᴘ_ɪᴅ & ᴀᴘᴘ_ʜᴀsʜ", url="https://my.telegram.org/auth"
                    ),
                    InlineKeyboardButton(
                        "sᴜᴘᴘᴏʀᴛ ʙʏ ✨", url="https://t.me/RACUN_SHOPEE101"
                    ),
                ],
                [
                    InlineKeyboardButton("❮ Kembali", callback_data="back_start"),
                ],
            ]
        ),
    )


@bot.on_callback_query(filters.regex("back_start"))
async def back_start_bc(c, callback_query):
    await callback_query.message.edit(
        start_msg.format(callback_query.from_user.mention, c.me.mention),
        reply_markup=InlineKeyboardMarkup(but_tutor),
    )


@bot.on_callback_query(filters.regex("deploy_fsub"))
async def deploy_fsub_bot(c, callback_query):
    if c.me.id != BOT_ID:
        return
    user_id = callback_query.from_user.id
    jancok = await cek_seller()
    if user_id not in MEMBER and user_id not in jancok:
        for X in jancok:
            await c.resolve_peer(X)
        buttons = InlineKeyboard(row_width=3)
        keyboard: List[InlineKeyboardButton] = []
        but = []
        for i in range(len(jancok)):
            list_admin = f"⛑️ ᴀᴅᴍɪɴ {i+1}"
            id_admin = jancok[i]
            keyboard.append(
                InlineKeyboardButton(
                    list_admin,
                    user_id=id_admin,
                )
            )
        but.append(InlineKeyboardButton("❮ Kembali", callback_data="back_start"))
        buttons.add(*keyboard + but)
        await callback_query.message.edit(
            "<b>Anda bukan bagian dari pengguna yang di ijinkan untuk menggunakan perintah ini\nSilahkan hubungi admin dibawah ini jika anda ingin membuat bot File sharing melalui BOT ini.</b>",
            reply_markup=buttons,
        )
        return
    await callback_query.message.delete()
    api_id = await c.ask(
        user_id,
        "<b>Masukan API_ID Dapatkan APP ID di web my.telegram.org</b>",
        filters=filters.text,
    )
    if await cancel(callback_query, api_id.text):
        return
    try:
        api_ids = int(api_id.text)
    except ValueError:
        await api_id.reply(
            "<b>Bukan API_ID yang valid Silakan ulang kembali dan masukan angka 6 digit</b>",
            quote=True,
        )
        return
    api_hash = await c.ask(
        user_id,
        "<b>Masukan API_HASH Dapatkan API HASH di web my.telegram.org</b>",
        filters=filters.text,
    )
    if await cancel(callback_query, api_hash.text):
        return
    bot_token = await c.ask(
        user_id,
        "<b>Masukan Bot token, Dapatkan dari t.me/BotFather</b>",
        filters=filters.text,
    )
    if await cancel(callback_query, bot_token.text):
        return
    name_id = bot_token.text.split(":")[0]
    cot = Bot(
        name=str(name_id),
        api_id=api_ids,
        api_hash=api_hash.text,
        bot_token=bot_token.text,
    )
    try:
        cot.in_memory = False
        await cot.start()
        await c.send_message(
            user_id,
            f"<b>Bot Terdeteksi</b> @{cot.me.username}",
        )
    except Exception as e:
        return await c.send_message(user_id, f"Error:\n{e}")
    channel_id = await c.ask(
        user_id,
        "<b>Masukan ID Channel Untuk Channel Database anda, yang berawalan -100 dan bot wajib admin</b>",
        filters=filters.text,
    )
    if await cancel(callback_query, channel_id.text):
        return
    try:
        await cot.export_chat_invite_link(int(channel_id.text))
        await channel_id.reply(f"Channel Database Terdeteksi `{channel_id.text}`", quote=True)
    except Exception:
        channel_id = await c.ask(user_id,
            f"Pastikan @{cot.me.username} adalah admin di Channel DataBase anda, Channel Database saat Ini: `{channel_id.text}`\nMasukan ID channel database anda kembali",
            filters=filters.text,
        )
        
    sub_id = await c.ask(
        user_id,
        "<b>Masukan ID dari Channel Atau Group Untuk Wajib Subscribenya yang berawalan -100 dan bot wajib admin</b>",
    )
    if await cancel(callback_query, sub_id.text):
        return
    try:
        if int(sub_id.text) != 0:
            await cot.export_chat_invite_link(int(sub_id.text))
            await sub_id.reply(f"Fsub Terdeteksi `{sub_id.text}`", quote=True)
    except Exception:
        sub_id = await c.ask(user_id,
            f"Pastikan @{cot.me.username} adalah admin di Channel atau Group anda, Channel atau Group Saat Ini: `{sub_id.text}`\nSilahkan kirim kembali",
            filters=filters.text,
        )
    admin_id = await c.ask(
        user_id,
        "<b>Masukan User ID untuk mendapatkan hak Admin di BOT dan masukan 1 user admin bot terlebih dahulu</b>",
        filters=filters.text,
    )
    if await cancel(callback_query, channel_id.text):
        return
    try:
        admin_ids = int(admin_id.text)
    except ValueError:
        admin_id = await c.ask(user_id,
            "<b>Bukan User ID account yang valid, Silakan masukan user ID account kembali</b>",
            filters=filters.text,
        )
    await c.send_message(user_id, "<code>✅ Bot Telah Berhasil Di Deploy dan Silahkan tunggu...</code>")
    await add_bot(str(cot.me.id), api_ids, api_hash.text, bot_token.text)
    await add_owner(
        cot.me.id,
        int(user_id),
        int(channel_id.text),
    )
    await add_sub(
        cot.me.id,
        int(sub_id.text),
    )
    time = (datetime.now() + timedelta(30)).strftime("%d-%m-%Y")
    await add_timer(cot.me.id, time)
    await add_admin(cot.me.id, admin_ids)
    anu = await c.send_message(
        LOG_GRP,
        "<b><u>🔥 BOT berhasil diaktifkan 🔥</u></b>\n"
        f"• <b>Nama Bot:</b> {cot.me.first_name}\n"
        f"• <b>Username:</b> @{cot.me.username}\n"
        f"• <b>ID Bot:</b> <code> {cot.me.id}</code>\n"
        f"• <b>Tanggal Exp:</b> <code>{time}</code>\n\n"
        f"• <b>Pembuat:</b> {callback_query.from_user.mention}\n"
        f"• <b>ID Pembuat:</b> <code>{callback_query.from_user.id}</code>",
    )
    await c.pin_chat_message(LOG_GRP, anu.id)
    sinting = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Bot Telah Aktif", callback_data=f"telah_aktif {callback_query.from_user.id} {cot.me.username}"
                )
            ]
        ]
    )
    await c.send_message(LOG_GRP, f"Pesan untuk deployer @{cot.me.username}", reply_markup=sinting
    )
    os.popen(f"rm {name_id}*")
    await restart()


@bot.on_message(
    filters.private
    & ~filters.command(
        [
            "start",
            "clone",
            "users",
            "broadcast",
            "eval",
            "addbase",
            "ultra",
            "addultra",
            "ultraaktif",
            "addadmin",
            "deladmin",
            "cekadmin",
            "help",
            "del",
            "info",
            "batch",
            "adsel",
            "delsel",
            "genlink",
            "protect",
            "id",
            "addsub",
            "delsub",
            "ceksub",
            "ping",
            "uptime",
            "maxsub",
            "setting",
            "cancel",
            "cekbot",
        ]
    )
)
@expired()
async def buat_konten(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    adm = await admin_info(c.me.id, m.from_user.id)
    for i in cek:
        owner = i["owner"]
        dbc = i["channel"]
    av = await timer_info(c.me.id)
    time = datetime.now().strftime("%d-%m-%Y")
    if av == time:
        print(f"@{c.me.username} Telah Habis Mohon Tunggu.. Bot sedang direstart 💞")
        await remove_bot(str(c.me.id))
        os.popen(f"rm {c.me.id}*")
        await restart()
    if not adm and m.from_user.id != owner:
        return
    ppk = await m.reply("<code>Silahkan Tunggu sebentar...</code>")
    iya = await m.copy(dbc)
    sagne = iya.id * abs(dbc)
    string = f"get-{sagne}"
    base64_string = await encode(string)
    link = f"https://t.me/{c.me.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔁 Share Link", url=f"https://telegram.me/share/url?url={link}"
                )
            ]
        ]
    )

    await ppk.edit(
        f"<b>Link Sharing File Berhasil Di Buat:</b>\n\n{link}",
        reply_markup=reply_markup,
    )
    try:
        await iya.edit_reply_markup(reply_markup)
    except Exception:
        pass


@bot.on_message(filters.command("help"))
async def helper_text(c, m):
    if c.me.id == BOT_ID:
        jancok = await cek_seller()
        if m.from_user.id in jancok:
            return await m.reply(
                    "<b>Daftar Perintah:</b>\n\n/ultra - Untuk akses deploy user\n/addultra - Untuk set masa aktif bot\n/ultraaktif - Untuk cek masa aktif bot\n/maxsub - untuk menentukan batas sub"
                )
    cek = await cek_owner(c.me.id)
    adm = await admin_info(c.me.id, m.from_user.id)
    jancok = await cek_seller()
    for i in cek:
        owner = i["owner"]
    if m.from_user.id in jancok:
        await m.reply(
            "<b>Daftar Perintah:</b>\n\n/ultra - Untuk akses deploy user\n/addultra - Untuk set masa aktif bot\n/ultraaktif - Untuk cek masa aktif bot"
        )

    elif m.from_user.id == owner:
        help_owner = '''
<b>⟱ Cara Menggunakan Bot Ini ⟱

❏ Perintah Untuk Pengguna BOT
├ /start - Untuk memulai bot
├ /ping - Untuk mengecek bot hidup
└ /uptime - Untuk melihat status bot 

❏ Perintah Untuk Admin BOT
├ /addadmin - Untuk menambah admin di bot
├ /addsub - Untuk menambah Fsub
├ /addbase - Untuk set channel base
├ /batch - Untuk membuat link lebih dari 1file
├ /broadcast - Untuk mengirim pesan siaran
├ /cekadmin - Untuk menampilkan admin
├ /ceksub - Untuk cek daftar Fsub
├ /deladmin - Untuk menghapus admin bot
├ /delsub - Untuk menghapus Fsub
├ /genlink - Untuk membuat tautan satu posting
├ /help - Untuk bantuan perintah bot ini
├ /info - Untuk mengecek masa aktif bot anda
├ /protect - Untuk menyalahkan True dan Untuk matikan False
├ /setting - Untuk menambahkan lain-lain
└ /users - Untuk melihat statistik pengguna bot.

➲ ᴅɪᴋᴇʟᴏʟᴀ ᴏʟᴇʜ - </b><a href='https://t.me/RACUN_SHOPEE101'>𝗥𝗔𝗖𝗨𝗡 𝗦𝗛𝗢𝗣𝗘𝗘</a>
 '''
        await m.reply(help_owner)

    elif adm:
        await m.reply(
            "📋 <b>Daftar Perintah</b>\n\n/users - Untuk cek pengunjung bot\n/broadcast - Untuk kirim pesan broadcast ke pengunjung bot\n/batch - Untuk membuat link lebih dari satu file\n/genlink - buat tautan untuk satu posting\n/protect - True untuk protect False untuk off"
        )
    else:
        await m.reply("Maaf ini bukan untuk anda.")


@bot.on_message(
    filters.incoming
    & ~filters.command(
        [
            "del",
            "eval",
            "addbase",
            "ultra",
            "addultra",
            "addadmin",
            "deladmin",
            "cekadmin",
            "help",
            "ultraaktif",
            "batch",
            "adsel",
            "delsel",
            "genlink",
            "protect",
            "id",
            "info",
            "addsub",
            "delsub",
            "ceksub",
            "ping",
            "uptime",
            "maxsub",
            "setting",
            "cancel",
            "cekbot",
        ]
    )
)
@expired()
async def post_channel(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        dbc = i["channel"]
    if m.chat.id != dbc:
        return
    converted_id = m.id * abs(dbc)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{c.me.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔁 Share Link", url=f"https://telegram.me/share/url?url={link}"
                )
            ]
        ]
    )
    try:
        await m.edit_reply_markup(reply_markup)
    except Exception:
        pass


@bot.on_message(filters.command("del") & filters.user(ADMINS))
async def del_users(c, m):
    if c.me.id != BOT_ID:
        return
    if len(m.command) < 2:
        return await m.reply("Silahkan kombinasikan dengan ID")
    ids = m.command[1]
    await remove_bot(str(ids))
    await del_owner(int(ids))
    await del_timer(int(ids))
    await m.reply(f"Hapus data untuk id {ids}")
    os.popen(f"rm {ids}*")
    await restart()


@bot.on_message(filters.command("addbase") & filters.private)
@expired()
async def ya_setting_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "Silahkan kombinasikan dengan ID channel database\ncontoh : /addbase -100123456789"
        )
    ids = int(m.command[1])
    try:
        await c.export_chat_invite_link(ids)
        await add_owner(
            int(c.me.id),
            int(m.from_user.id),
            int(ids),
        )
        await m.reply(f"Channel ID Database berhasil di set `{ids}`")
    except:
        return await m.reply(f"Maaf saya bukan admin di `{ids}`")


@bot.on_message(filters.command("ultra"))
async def member_prem(c, m):
    if c.me.id != BOT_ID:
        return
    if len(m.command) < 2:
        return await m.reply(
            "<b>Masukan user ID pembuat, untuk mendeploy di @JayXRobot\ncontoh : /ultra 1944309678</b>"
        )
    iya = await seller_info(m.from_user.id)
    if not iya and m.from_user.id not in ADMINS:
        return
    ids = m.command[1]
    if int(ids) not in MEMBER:
        MEMBER.append(int(ids))
        await m.reply(f"{ids} Berhasil di tambahkan ke member premium")
    else:
        await m.reply(f"Maaf {ids} Sudah menjadi member premium")


@bot.on_message(filters.command("addultra"))
async def add_aktif_bot(c, m):
    if len(m.command) < 3:
        return await m.reply(
            "<b>Masukan ID bot yang ingin ditambah masa aktifnya, 1 sama dengan 1 hari\nContoh : /addultra 1944309678 30</b>"
        )
    iya = await seller_info(m.from_user.id)
    if not iya and m.from_user.id not in ADMINS:
        return
    ids = m.command[1]
    h = int(m.command[2])
    time = (datetime.now() + timedelta(h)).strftime("%d-%m-%Y")
    await add_timer(int(ids), time)
    await m.reply(f"User ID : {ids}\nTime : {time}")


@bot.on_message(filters.command("ultraaktif"))
async def cek_member_prem(c, m):
    iya = await seller_info(m.from_user.id)
    if not iya and m.from_user.id not in ADMINS:
        return
    anu = await cek_prem()
    msg = "<b><u>💎 List Fsub Premium Bot</u></b>\n\n"
    ang = 0
    for ex in anu:
        try:
            afa = f"`{ex['nama']}` » {ex['aktif']}"
            ang += 1
        except Exception:
            continue
        msg += f"{ang} › {afa}\n"
    await m.reply(msg)


async def cancel(callback_query, text):
    if text.startswith("/"):
        await bot.send_message(
            callback_query.from_user.id,
            "⁉️ <b>Proses di batalkan, silahkan coba lagi</b>",
        )
        return True
    else:
        return False


@bot.on_message(filters.command("info") & filters.private)
@expired()
async def status_mem(c, m):
    if c.me.id == BOT_ID:
        return
    adm = await admin_info(c.me.id, m.from_user.id)
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if adm or m.from_user.id == int(owner):
        act = await timer_info(c.me.id)
        await c.send_message(
            int(owner),
            f"🤖 <b>Bot Name:</b> {c.me.first_name}\n"
            f"🆔 <b>Bot ID:</b> <code> {c.me.id}</code>\n"
            f"⏱️ <b>Bot Expired:</b> <code> {act}</code>"
        )
    else:
        return


@bot.on_callback_query(filters.regex("support"))
async def _(c, callback_query):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    try:
        buttons = [
            [InlineKeyboardButton("❌ Batalkan", callback_data=f"batal {user_id}")]
        ]
        pesan = await c.ask(
            user_id,
            "<b>Silahkan Kirimkan Pesan Apapun Untuk Menghubungi Seller</b>",
            reply_markup=InlineKeyboardMarkup(buttons),
            timeout=60,
        )
        await c.send_message(
            user_id, "💬 Pesan Anda Telah Dikirim Ke Seller ✅\nSilahkan Tunggu Balasan"
        )
        await callback_query.message.delete()
    except asyncio.TimeoutError:
        return await c.send_message(user_id, "<b>Pembatalkan otomatis</b>")
    button = [
        [
            InlineKeyboardButton(full_name, user_id=user_id),
            InlineKeyboardButton("Jawab 💬", callback_data=f"jawab_pesan {user_id}"),
        ],
    ]
    await pesan.copy(
        LOG_GRP,
        reply_markup=InlineKeyboardMarkup(button),
    )


@bot.on_callback_query(filters.regex("jawab_pesan"))
async def _(c, callback_query):
    user_id = int(callback_query.from_user.id)
    user_ids = int(callback_query.data.split()[1])
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    if user_ids == LOG_GRP:
        try:
            button = [
                [InlineKeyboardButton("❌ Batalkan", callback_data=f"batal {user_id}")]
            ]
            pesan = await c.ask(
                user_id,
                f"<b>Silahkan Kirimkan Balasan Anda.</b>",
                reply_markup=InlineKeyboardMarkup(button),
                timeout=60,
            )
            await c.send_message(
                user_id,
                "✅ <code>Pesan Anda Telah Dikirim Ke Seller\nSilahkan Tunggu Balasan</code>",
            )
            await callback_query.message.delete()
        except asyncio.TimeoutError:
            return await c.send_message(user_id, "<b>Pembatalkan otomatis</b>")
        buttons = [
            [
                InlineKeyboardButton(full_name, user_id=user_id),
                InlineKeyboardButton("Jawab 💬", callback_data=f"jawab_pesan {user_id}"),
            ],
        ]
        await pesan.copy(
            user_ids,
            reply_markup=InlineKeyboardMarkup(buttons),
        )

    else:
        try:
            button = [
                [InlineKeyboardButton("❌ Batalkan", callback_data=f"batal {LOG_GRP}")]
            ]
            pesan = await c.ask(
                LOG_GRP,
                f"<b>Silahkan Kirimkan Balasan Anda.</b>",
                reply_markup=InlineKeyboardMarkup(button),
                timeout=60,
            )
            await c.send_message(
                LOG_GRP,
                "✅ <b>Pesan Anda Telah Dikirim Ke User, Silahkan Tunggu Balasan</b>",
            )
            await callback_query.message.delete()
        except asyncio.TimeoutError:
            return await c.send_message(LOG_GRP, "<b>Pembatalkan otomatis</b>")
        buttons = [
            [
                InlineKeyboardButton("Jawab 💬", callback_data=f"jawab_pesan {LOG_GRP}"),
            ],
        ]
        await pesan.copy(
            user_ids,
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@bot.on_callback_query(filters.regex("batal"))
async def _(client, callback_query):
    user_ids = int(callback_query.data.split()[1])
    if user_ids == LOG_GRP:
        client.cancel_listener(LOG_GRP)
        await client.send_message(LOG_GRP, "❌ <b>Pesan di batalkan</b>")
        await callback_query.message.delete()
        return True
    elif user_ids != LOG_GRP:
        client.cancel_listener(user_ids)
        await client.send_message(user_ids, "❌ <b>Pesan di batalkan</b>")
        await callback_query.message.delete()
        return True
    else:
        return False


@bot.on_message(filters.command("ping"))
async def ping_pong(c, m):
    start = time()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    m_reply = await m.reply("Pinging...")
    delta_ping = time() - start
    await m_reply.edit(
        "<b>PONG!!</b>🏓 \n"
        f"<b>• Pinger -</b> <code>{delta_ping * 1000:.3f}ms</code>\n"
        f"<b>• Uptime -</b> <code>{uptime}</code>\n"
    )


@bot.on_message(filters.command("uptime"))
async def get_uptime(client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "🤖 <b>Bot Status:</b>\n"
        f"• <b>Uptime:</b> <code>{uptime}</code>\n"
        f"• <b>Start Time:</b> <code>{START_TIME_ISO}</code>"
    )

@bot.on_callback_query(filters.regex("tentang"))
async def cb_tentang(c, query: CallbackQuery):
    try:
        await query.message.edit(
            text=f"Tentang Bot ini:\n\n@{c.me.username} Adalah Bot Telegram Untuk Menyimpan Postingan Atau File Yang Dapat Diakses Melalui Link Khusus.\n\n➲ ᴄʀᴇᴀᴛᴏʀ : [ᴋʟɪᴋ ᴅɪsɪɴɪ](https://s.id/Tentang-Saya)\n➲ sᴜᴘᴘᴏʀᴛ ʙʏ : [𝗥𝗔𝗖𝗨𝗡 𝗦𝗛𝗢𝗣𝗘𝗘](https://t.me/RACUN_SHOPEE101)", 
            reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("❮ Kembali", callback_data="kembali_aja"),
                        ]
                    ]
            ),
            disable_web_page_preview=True,
            )
    except BaseException as e:
        logs.info(e)

@bot.on_callback_query(filters.regex("kembali_aja"))
async def cb_kembali_aja(c, query):
    buttons = await start_button(c)
    await query.message.edit(
            f"<b>Hello {query.from_user.mention}\n\nSaya dapat menyimpan file pribadi di Channel Tertentu dan pengguna lain dapat mengaksesnya dari link khusus.</b>",
            reply_markup=InlineKeyboardMarkup(buttons),
    )

@bot.on_message(filters.command("maxsub"))
async def add_max_bot(c, m):
    if len(m.command) < 3:
        return await m.reply(
            "<b>Masukan ID bot yang ingin ditambah Fsub nya, dan jumlah Fsub nya\nContoh : /maxsub 1944309678 4</b>"
        )
    iya = await seller_info(m.from_user.id)
    if not iya and m.from_user.id not in ADMINS:
        return
    ids = m.command[1]
    h = int(m.command[2])
    await add_max(int(ids), h)
    await m.reply(f"<b>Bot ID:</b> {ids}\n<b>Max Sub:</b> {h}")


@bot.on_message(filters.command('set_start'))
async def set_start_msg(c: Client, m: Message):
    if c.me.id == BOT_ID:
        return
    r = m.reply_to_message
    if r:
        if '{user}' not in r.text:
            return await m.reply("Format yg anda berikan salah.\n\nSilahkan gunakan contoh seperti ini.\nHello {user} silahkan klik grup/channel terlebih dahulu.")
        else:
            await set_start(user_id=c.me.id, caption=r.text)
            await m.reply(f'''
Pesan start bot anda berhasil di atur.

<code>{r.text}</code>
'''
            )
            return
    else:
        await m.reply("Silahkan balas ke pesan.")
        return


@bot.on_message(filters.command('exp'))
async def update_expired(c: Client, m: Message):
    if c.me.id != BOT_ID:
        return
    target = m.command[1]
    arg = m.text.split(None, 2)[2]
    date = 30 * int(arg)
    time = (datetime.now() + timedelta(int(date))).strftime("%d-%m-%Y")
    check = await timer_info(int(target))
    if "Belum" not in check:
        xx = await m.reply(f"<b>Pengguna {int(target)} ditemukan dengan tanggal kedaluwarsa {check}.</b>\n<b>Memperbarui Tanggal Kedaluwarsa.</b>")
        await add_timer(int(target), time)
        await asyncio.sleep(2)
        await xx.edit(f"<b>Berhasil Memperbarui Kedaluwarsa.</b>\n\n<b>User ID:</b> {int(target)}\n<b>Date:</b> {time}")
        return
    else:
        pass


@bot.on_callback_query(filters.regex("telah_aktif"))
async def _(client, callback_query):
    user_ids = int(callback_query.data.split()[1])
    bot_user = callback_query.data.split()[2]
    await client.send_message(user_ids, f"🔥 Bot berhasil diaktifkan, silahkan start bot anda @{bot_user}")
    await callback_query.message.edit("<b>Pesan telah di kirim</b>")


@bot.on_callback_query(filters.regex("tutup"))
async def cb_tutup(c, query: CallbackQuery):
    try:
        await query.answer()
        await query.message.delete()
    except BaseException as e:
        logs.info(e)
