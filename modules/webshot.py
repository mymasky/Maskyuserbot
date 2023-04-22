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

@ayra_cmd(pattern="webshot(?:\s+(.*))?")
async def webshot(e):
    await e.eor("`Processing...`")
    try:
        user_link = e.pattern_match.group(1).strip()
        if not user_link:
            await e.eor("`Masukkan URL situs web yang ingin diambil tangkapan layarnya.`")
            return
        full_link = f"https://webshot.deam.io/{user_link}/?width=1920&height=1080&delay=2000&type=png"
        await e.client.send_file(
            e.chat_id,
            full_link,
            caption=f"**Tangkapan layar halaman** {user_link}",
            force_document=True,
            supports_streaming=False
        )
    except Exception as error:
        await e.eor(f"**Terjadi kesalahan:** `{error}`")
