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
"""
import asyncio
import os

from telethon.errors.rpcerrorlist import ChatAdminRequiredError, FloodWaitError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.types import ChatAdminRights, User

from Ayra.dB import DEVS
from Ayra.dB.gban_mute_db import (
    gban,
    gmute,
    is_gbanned,
    is_gmuted,
    list_gbanned,
    ungban,
    ungmute,
)
from Ayra.dB.gcast_blacklist_db import (
    add_gblacklist,
    is_gblacklisted,
    rem_gblacklist,
    get_stuff,
)
from Ayra.fns.tools import create_tl_btn, format_btn, get_msg_button

from . import (
    HNDLR,
    LOGS,
    NOSPAM_CHAT,
    OWNER_NAME,
    eod,
    eor,
    get_string,
    inline_mention,
    ayra_bot,
    ayra_cmd,
    udB,
)
from ._inline import something


def black_aja():
    return udB.get_key("GBLACKLISTS") or {}

def list_bl(id):
    ok = black_aja()
    if id in ok:
        return "".join(f"**๏ {z}**\n" for z in ok[]

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

    kk = await event.eor("`Sebentar Kalo Limit Jangan Salahin Gua...`")
    er = 0
    done = 0
    err = ""
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            chat_blacklist = udB.get_key("GBLACKLISTS")
            if (
                chat not in chat_blacklist and
                chat not in NOSPAM_CHAT and
                (
                  event.text[2:7] != "admin" or
                  (x.entity.admin_rights or x.entity.creator)
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
    text += f"Berhasil di {done} obrolan, kesalahan {er} obrolan(s)"
    if err != "":
        open("gcast-error.log", "w+").write(err)
        text += f"\Anda dapat melakukan `{HNDLR}ayra gcast-error.log` untuk mengetahui laporan kesalahan."
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
    kk = await event.eor("`Sebentar Kalo Limit Jangan Salahin Gua...`")
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
    await kk.edit(f"Berhasil di {done} obrolan, kesalahan {er} obrolan(s)")


@ayra_cmd(pattern="addbl")
async def blacklist_(event):
    await gblacker(event, "add")


@ayra_cmd(pattern="delbl")
async def ungblacker(event):
    await gblacker(event, "remove")


@ayra_cmd(pattern="blchat")
async def chatbl(event):
    id = event.chat_id
    x = list_bl(id)
    if x:
        sd = "**❏ Daftar Blacklist Gcast**\n\n"
        return await event.eor(sd + x)
    await event.eor("**Belum ada daftar**")


"""
@ayra_cmd(pattern="blchat")
async def chatbl(event):
    chat = event.chat_id
    if x := list_bl(chat):
        sd = "**❏ Daftar Blacklist Gcast**\n\n"
        return await e.eor(sd + x)
    await e.eor("**Belum ada daftar**")
"""


async def gblacker(event, type_):
    try:
        chat_id = int(event.text.split(maxsplit=1)[1])
        try:
            chat_id = (await event.client.get_entity(chat_id)).id
        except Exception as e:
            return await event.eor(f"**ERROR**\n`{str(e)}`")
    except IndexError:
        chat_id = event.chat_id
    if type_ == "add":
        add_gblacklist(chat_id)
        await event.eor(f"Ditambahkan ke BLGCAST\n{chat_id}")
    elif type_ == "remove":
        rem_gblacklist(chat_id)
        await event.eor(f"Dihapus dari BLGCAST\n{chat_id}")