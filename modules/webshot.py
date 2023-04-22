# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Webshot**

๏ **Perintah:** `webshot` <link>
◉ **Keterangan:** Dapatkan screenshot dari link tersebut
"""

import asyncio
from . import *

@ayra_cmd(pattern="([Ww][e][b][s][h][o][t]( (.*)|$)")
async def webshot(e):
    await e.eor("`Processing...`")
    try:
        user_link = e.command[1]
        try:
            full_link = f"https://webshot.deam.io/{user_link}/?width=1920&height=1080?delay=2000?type=png"
            await e.client.send_file(
                e.chat_id,
                full_link,
                caption=f"**Tangkapan layar halaman** {user_link}",
            )
        except Exception as dontload:
            await e.eor(f"Error! `{dontload}`\nMencoba lagi membuat tangkapan layar...")
            full_link = f"https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{user_link}"
            await e.client.send_file(
                e.chat_id,
                full_link,
                caption=f"**Tangkapan layar halaman** `{user_link}`",
            )
    except Exception as error:
        await e.eor(
            e.chat_id, f"**Ada yang salah\nLog:`{error}`...**"
        )