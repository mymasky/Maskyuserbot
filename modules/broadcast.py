# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Broadcast**

๏ **Perintah:** `gcast`
◉ **Keterangan:** Kirim pesan ke semua obrolan grup.

๏ **Perintah:** `gucast`
◉ **Keterangan:** Kirim pesan ke semua pengguna pribadi.

๏ **Perintah:** `addbl`
◉ **Keterangan:** Tambahkan grup ke dalam anti gcast.

๏ **Perintah:** `delbl`
◉ **Keterangan:** Hapus grup dari daftar anti gcast.

๏ **Perintah:** `blchat`
◉ **Keterangan:** Melihat daftar anti gcast.

◉ **Notes:** Bisa menggunakan media apapun serta menggunakan button.
◉ **Contoh:**
Kirim ke
[Dana|https://link.dana]
[Qris|https://link.qris|same]
"""
import asyncio

from Ayra.dB import DEVS
from Ayra.dB.gcast_blacklist_db import add_gblacklist, list_bl, rem_gblacklist
from Ayra.fns.tools import create_tl_btn, format_btn, get_msg_button
from telethon.errors.rpcerrorlist import FloodWaitError

from . import *
from ._inline import something


@ayra_cmd(pattern="[gG][c][a][s][t]( (.*)|$)", fullsudo=False)
async def gcast(event):
    text, btn, reply = "", None, None
    if xx := event.pattern_match.group(2):
        msg, btn = get_msg_button(event.text.split(maxsplit=1)[1])
    elif event.is_reply:
        reply = await event.get_reply_message()
        msg = reply.text
        if reply.buttons:
            btn = format_btn(reply.buttons)
        else:
            msg, btn = get_msg_button(msg)
    else:
        return await eor(
            event, "`Berikan beberapa teks ke Globally Broadcast atau balas pesan..`"
        )

    kk = await event.eor("`Sebentar Kalo Limit Jangan Salahin Kynan Ya...`")
    er = 0
    done = 0
    err = ""
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            chat_blacklist = udB.get_key("GBLACKLISTS") or []
            chat_blacklist.append(-1001927904459)
            if (
                chat not in chat_blacklist
                and chat not in NOSPAM_CHAT
                and (
                    event.text[2:7] != "admin"
                    or (x.entity.admin_rights or x.entity.creator)
                )
            ):
                try:
                    if btn:
                        bt = create_tl_btn(btn)
                        await something(
                            event,
                            msg,
                            reply.media if reply else None,
                            bt,
                            chat=chat,
                            reply=False,
                        )
                    else:
                        await event.client.send_message(
                            chat, msg, file=reply.media if reply else None
                        )
                    done += 1
                except FloodWaitError as fw:
                    await asyncio.sleep(fw.seconds + 10)
                    try:
                        if btn:
                            bt = create_tl_btn(btn)
                            await something(
                                event,
                                msg,
                                reply.media if reply else None,
                                bt,
                                chat=chat,
                                reply=False,
                            )
                        else:
                            await event.client.send_message(
                                chat, msg, file=reply.media if reply else None
                            )
                        done += 1
                    except Exception as rr:
                        err += f"• {rr}\n"
                        er += 1
                except BaseException as h:
                    err += f"• {str(h)}" + "\n"
                    er += 1
    text += f"Berhasil di {done} obrolan, kesalahan {er} obrolan"
    if err != "":
        open("gcast-error.log", "w+").write(err)
        text += f"\\Anda dapat melakukan `{HNDLR}ayra gcast-error.log` untuk mengetahui laporan kesalahan."
    await kk.edit(text)


@ayra_cmd(pattern="[gG][u][c][a][s][t]( (.*)|$)", fullsudo=False)
async def gucast(event):
    msg, btn, reply = "", None, None
    if xx := event.pattern_match.group(1).strip():
        msg, btn = get_msg_button(event.text.split(maxsplit=1)[1])
    elif event.is_reply:
        reply = await event.get_reply_message()
        msg = reply.text
        if reply.buttons:
            btn = format_btn(reply.buttons)
        else:
            msg, btn = get_msg_button(msg)
    else:
        return await eor(
            event, "`Berikan beberapa teks ke Globally Broadcast atau balas pesan..`"
        )
    kk = await event.eor("`Sebentar Kalo Limit Jangan Salahin Kynan Ya...`")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            if chat not in DEVS:
                try:
                    if btn:
                        bt = create_tl_btn(btn)
                        await something(
                            event,
                            msg,
                            reply.media if reply else None,
                            bt,
                            chat=chat,
                            reply=False,
                        )
                    else:
                        await event.client.send_message(
                            chat, msg, file=reply.media if reply else None
                        )
                    done += 1
                except BaseException:
                    er += 1
    await kk.edit(f"Berhasil di {done} obrolan, kesalahan {er} obrolan")


@ayra_cmd(pattern="addbl")
async def blacklist_(event):
    await gblacker(event, "add")


@ayra_cmd(pattern="delbl")
async def ungblacker(event):
    await gblacker(event, "remove")


@ayra_cmd(pattern="blchat")
async def chatbl(event):
    id = event.chat_id
    if xx := list_bl(id):
        sd = "**❏ Daftar Blacklist Gcast**\n\n"
        return await event.eor(sd + xx)
    await event.eor("**Belum ada daftar**")


async def gblacker(event, type_):
    args = event.text.split()
    if len(args) > 2:
        return await event.eor("**Gunakan Format:**\n `delbl` or `addbl`")
    chat_id = None
    chat_id = int(args[1]) if len(args) == 2 else event.chat_id
    if type_ == "add":
        add_gblacklist(chat_id)
        await event.eor(f"**Ditambahkan ke BL-GCAST**\n`{chat_id}`")
    elif type_ == "remove":
        rem_gblacklist(chat_id)
        await event.eor(f"**Dihapus dari BL-GCAST**\n`{chat_id}`")
