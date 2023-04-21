# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Webshot**

๏ **Perintah:** `webshot/ss` <link>
◉ **Keterangan:** Dapatkan screenshot dari link tersebut
"""
import glob
import io
import os
from asyncio.exceptions import TimeoutError as AsyncTimeout

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from htmlwebshot import WebShot
except ImportError:
    WebShot = None
from telethon.errors.rpcerrorlist import MessageTooLongError, YouBlockedUserError
from telethon.tl.types import (
    ChannelParticipantAdmin,
    ChannelParticipantsBots,
    DocumentAttributeVideo,
)

from Ayra.fns.tools import metadata, translate

from . import (
    HNDLR,
    LOGS,
    AyConfig,
    async_searcher,
    bash,
    check_filename,
    con,
    eor,
    fast_download,
    get_string,
)
from . import humanbytes as hb
from . import inline_mention, is_url_ok, mediainfo, ayra_cmd


@ayra_cmd(pattern=r"^(w|W)ebshot")
async def webss(event):
    xx = await event.eor(get_string("com_1"))
    xurl = event.pattern_match.group(1).strip()
    if not xurl:
        return await xx.eor(get_string("wbs_1"), time=5)
    if not is_url_ok(xurl):
        return await xx.eor(get_string("wbs_2"), time=5)
    try:
        shot = WebShot(
            quality=88, flags=["--enable-javascript", "--no-stop-slow-scripts"]
        )
        pic = await shot.create_pic_async(url=xurl)
    except FileNotFoundError:
        pic = (
            await fast_download(
                f"https://mini.s-shot.ru/1920x1080/JPEG/1024/Z100/?{xurl}",
                filename=check_filename("shot.png"),
            )
        )[0]
    if pic:
        await xx.reply(
            get_string("wbs_3").format(xurl),
            file=pic,
            link_preview=False,
            force_document=True,
        )
        os.remove(pic)
    await xx.delete()