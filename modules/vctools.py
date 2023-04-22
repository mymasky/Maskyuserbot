# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk VC Tools**

๏ **Perintah:** `startvc`
◉ **Keterangan:** Memulai obrolan suara.

๏ **Perintah:** `stopvc`
◉ **Keterangan:** Mengakhiri obrolan suara.

๏ **Perintah:** `vctitle`
◉ **Keterangan:** Ubah judul obrolan suara.

๏ **Perintah:** `joinvc`
◉ **Keterangan:** Bergabung ke obrolan suara.

๏ **Perintah:** `leavevc`
◉ **Keterangan:** Meninggalkan ke obrolan suara.
"""

import asyncio

from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import EditGroupCallTitleRequest as settitle
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from . import *
from .music import *


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call, limit=1))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@kynan_cmd(pattern="startvc$", group_only=True)
@register(pattern=r"^\.startvcs$", sudo=True)
async def start_voice(c):
    xnxx = await eor(c, get_string("com_1"))
    me = await c.client.get_me()
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await eod(xnxx, get_string("stvc_1").format(me.first_name))
        return
    try:
        Nan = Player(c.chat_id)
        await Nan make_vc_active()
        await xnxx.edit(get_string("stvc_2"))
    except Exception as ex:
        await eod(xnxx, get_string("error_1").format(e))


@kynan_cmd(pattern="stopvc$", group_only=True)
@register(pattern=r"^\.stopvcs$", sudo=True)
async def stop_voice(c):
    jing = await eor(c, get_string("com_1"))
    me = await c.client.get_me()
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await eod(yins, get_string("stvc_1").format(me.first_name))
        return
    try:
        await c.client(stopvc(await get_call(c)))
        await yins.edit(get_string("stvc_3"))
    except Exception as ex:
        await eod(jing, get_string("error_1").format(ex))

@ayra_cmd(pattern="(v|V)ctitle( (.*)|$)")
async def _(event):
    title = event.pattern_match.group(2).strip()
    if not title:
        return await event.eor("Mohon masukkan judul obrolan suara yang valid.")
    try:
        await event.client(settitle(call=await get_call(event), title=title.strip()))
        await event.eor(f"❏ **Judul Voice Chat**\n└ `{title}`.")
    except Exception as ex:
        await event.eor(f"Terjadi kesalahan: {ex}")
        
        
@vc_asst(
    pattern="(j|J)oinvc(?: |$)(.*)")
@register(incoming=True, from_users=DEVS, pattern=r"^(j|J)vcs(?: |$)(.*)")
async def join_(event):
    if len(event.text.split()) > 1:
        chat = event.text.split()[1]
        try:
            chat = await event.client.parse_id(chat)
        except Exception as e:
            return await event.eor(get_string("vcbot_2").format(str(e)))
    else:
        chat = event.chat_id
    Nan = Player(chat)
    if not Nan.group_call.is_connected:
        await Nan.group_call.join(chat)
        await event.eor(f"❏ **Berhasil Bergabung Voice Chat**\n└ **Chat ID:** `{chat}`")
        await asyncio.sleep(1)
        await Nan.group_call.set_is_mute(False)
        await asyncio.sleep(1)
        await Nan.group_call.set_is_mute(True)



@vc_asst("(leavevc|Leavevc|end|End)(?: |$)(.*)")
@register(incoming=True, from_users=DEVS, pattern=r"^(l|L)vcs(?: |$)(.*)")
async def leaver(event):
    if len(event.text.split()) > 1:
        chat = event.text.split()[1]
        try:
            chat = await event.client.parse_id(chat)
        except Exception as e:
            return await event.eor(get_string("vcbot_2").format(str(e)))
    else:
        chat = event.chat_id
    aySongs = Player(chat)
    await aySongs.group_call.leave()
    if CLIENTS.get(chat):
        del CLIENTS[chat]
    if VIDEO_ON.get(chat):
        del VIDEO_ON[chat]
    await event.eor(f"❏ **Berhasil Turun Voice Chat**\n└ **Chat ID:** `{chat}`")
