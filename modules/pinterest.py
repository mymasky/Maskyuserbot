# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Pinterest**

๏ **Perintah:** `pntrst` <link>
◉ **Keterangan:** Unduh tautan pinterest.
"""


try:
    import cv2
except ImportError:
    cv2 = None

try:
    from htmlwebshot import WebShot
except ImportError:
    WebShot = None

from . import *


@ayra_cmd(
    pattern="(p|P)ntrst( (.*)|$)",
)
async def pinterest(e):
    m = e.pattern_match.group(1).strip()
    if not m:
        return await e.eor("`Berikan tautan pinterest.`", time=3)
    soup = await async_searcher(
        "https://www.expertstool.com/download-pinterest-video/",
        data={"url": m},
        post=True,
    )
    try:
        _soup = bs(soup, "html.parser").find("table").tbody.find_all("tr")
    except BaseException:
        return await e.eor("`Tautan salah atau pin pribadi.`", time=5)
    file = _soup[1] if len(_soup) > 1 else _soup[0]
    file = file.td.a["href"]
    await e.client.send_file(e.chat_id, file, caption=f"Pin:- {m}")
