# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

"""
◈ Perintah Tersedia

• `{i} rc/carbon` <balas teks>
     `rcarbon` Background Acak.

• `{i} ccarbon` <warna><balas teks>
     Carbon Dengan Kostum Warna.
"""


import random

from telethon.utils import get_display_name

from . import Carbon, eor, get_string, inline_mention, os, ayra_cmd

_colorspath = "resources/colorlist.txt"

if os.path.exists(_colorspath):
    with open(_colorspath, "r") as f:
        all_col = f.read().split()
else:
    all_col = []


@ayra_cmd(
    pattern="(rc|c)arbon",
)
async def crbn(event):
    xxxx = await event.eor(get_string("com_1"))
    te = event.pattern_match.group(1)
    col = random.choice(all_col)
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            b = await event.client.download_media(temp)
            with open(b) as a:
                code = a.read()
            os.remove(b)
        else:
            code = temp.message
    else:
        try:
            code = event.text.split(" ", maxsplit=1)[1]
        except IndexError:
            return await eor(xxxx, get_string("carbon_2"))
    xx = await Carbon(code=code, file_name="ayra_carbon", backgroundColor=col)
    await xxxx.delete()
    await event.reply(
        f"Carbonised by {inline_mention(event.sender)}",
        file=xx,
    )


@ayra_cmd(
    pattern="ccarbon( (.*)|$)",
)
async def crbn(event):
    match = event.pattern_match.group(1).strip()
    if not match:
        return await event.eor(get_string("carbon_3"))
    msg = await event.eor(get_string("com_1"))
    if event.reply_to_msg_id:
        temp = await event.get_reply_message()
        if temp.media:
            b = await event.client.download_media(temp)
            with open(b) as a:
                code = a.read()
            os.remove(b)
        else:
            code = temp.message
    else:
        try:
            match = match.split(" ", maxsplit=1)
            code = match[1]
            match = match[0]
        except IndexError:
            return await eor(msg, get_string("carbon_2"))
    xx = await Carbon(code=code, backgroundColor=match)
    await msg.delete()
    await event.reply(
        f"Carbonised by {inline_mention(event.sender)}",
        file=xx,
    )


