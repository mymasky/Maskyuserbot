# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Update**

๏ **Perintah:** `tr` <kode bahasa>
◉ **Keterangan:** Terjemahkan pesan.

◉ **Contoh:** `tr id` <balas ke pesan>
Ini akan menerjemahkan pesan ke Bahasa Indonesia.
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


@ayra_cmd(pattern="(tr|Tr)", manager=False)
async def _(event):
    input = event.pattern_match.group(1).strip().split(maxsplit=1)
    txt = input[1] if len(input) > 1 else None
    if input:
        input = input[0]
    if txt:
        text = txt
    elif event.is_reply:
        previous_message = await event.get_reply_message()
        text = previous_message.message
    else:
        return await eor(
            event, f"`{HNDLR}tr <kode bahasa> <balasan pesan>`", time=5
        )
    lan = input or "id"
    try:
        tt = translate(text, lang_tgt=lan)
        output_str = f"**TERJEMAHAN** dari {lan}\n{tt}"
        await event.eor(output_str)
    except Exception as exc:
        LOGS.exception(exc)
        await event.eor(str(exc), time=5)
