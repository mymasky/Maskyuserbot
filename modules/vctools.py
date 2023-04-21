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

from . import ayra_cmd, vc_asst, owner_and_sudos, get_string, udB, inline_mention, add_to_queue, mediainfo, file_download, LOGS, is_url_ok, bash, download, Player, VC_QUEUE, list_queue, CLIENTS,VIDEO_ON, vid_download, dl_playlist, DEVS, eor
from Ayra.kynan import register


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call, limit=1))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@ayra_cmd(
    pattern="(s|S)topvc$",
    admins_only=True,
    groups_only=True,
)
async def _(e):
    try:
        await e.client(stopvc(await get_call(e)))
        await e.eor(get_string("vct_4"))
    except Exception as ex:
        await e.eor(f"`{ex}`")


@ayra_cmd(
    pattern="(s|S)tartvc$",
    admins_only=True,
    groups_only=True,
)
async def _(e):
    try:
        await e.client(startvc(e.chat_id))
        await e.eor(get_string("vct_1"))
    except Exception as ex:
        await e.eor(f"`{ex}`")


@ayra_cmd(
    pattern="(v|V)ctitle(?: |$)(.*)",
    admins_only=True,
    groups_only=True,
)
async def _(e):
    title = e.pattern_match.group(1).strip()
    if not title:
        return await e.eor(get_string("vct_6"), time=5)
    try:
        await e.client(settitle(call=await get_call(e), title=title.strip()))
        await e.eor(get_string("vct_2").format(title))
    except Exception as ex:
        await e.eor(f"`{ex}`")
        
        
@ayra_cmd(
    pattern="(j|J)oinvc(?: |$)(.*)")
@register(incoming=True, from_users=DEVS, pattern=r"^Joinvcs$")
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
        await event.reply(f"❏ **Berhasil Bergabung Ke Obrolan Suara**\n└ **Chat ID:** `{chat}`")
        await asyncio.sleep(1)
        await Nan.group_call.set_is_mute(False)
        await asyncio.sleep(1)
        await Nan.group_call.set_is_mute(True)



@vc_asst("(l|L)eavevc")
@register(incoming=True, from_users=DEVS, pattern=r"^Leavevcs$")
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
    await event.eor(get_string("vcbot_1"))
