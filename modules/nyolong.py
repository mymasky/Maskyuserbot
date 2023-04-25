# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Nyolong**

๏ **Perintah:** `copy` <link>
◉ **Keterangan:** Colong pesan dari group/channel.
"""

import os

try:
    from PIL import Image
except ImportError:
    Image = None

from Ayra.fns.tools import get_chat_and_msgid

try:
    from telegraph import upload_file as uf
except ImportError:
    uf = None

from telethon.errors.rpcerrorlist import ChatForwardsRestrictedError

from . import ayra_cmd, get_string

# =================================================================#

TMP_DOWNLOAD_DIRECTORY = "resources/downloads/"

_copied_msg = {}


@ayra_cmd(pattern="[cC][o][p][y]( ?(.*)|$)")
async def get_restriced_msg(event):
    match = event.pattern_match.group(1).strip()
    if not match:
        await event.eor("`Berikan tautan!`", time=5)
        return
    xx = await event.eor(get_string("com_1"))
    chat, msg = get_chat_and_msgid(match)
    if not (chat and msg):
        return await event.eor(
            f"{get_string('gms_1')}!\nEg: `https://t.me/c/1313492028/3`"
        )
    try:
        message = await event.client.get_messages(chat, ids=msg)
    except BaseException as er:
        return await event.eor(f"**ERROR**\n`{er}`")
    try:
        await event.client.send_message(event.chat_id, message)
        await xx.try_delete()
        return
    except ChatForwardsRestrictedError:
        pass
    if message.media:
        thumb = None
        if message.document.thumbs:
            thumb = await message.download_media(thumb=-1)
        media, _ = await event.client.fast_downloader(
            message.document,
            show_progress=True,
            event=xx,
            message=f"Downloading {message.file.name}...",
        )
        await xx.edit("`Uploading...`")
        uploaded, _ = await event.client.fast_uploader(
            media.name, event=xx, show_progress=True, to_delete=True
        )
        typ = not bool(message.video)
        await event.reply(
            message.text,
            file=uploaded,
            supports_streaming=typ,
            force_document=typ,
            thumb=thumb,
            attributes=message.document.attributes,
        )
        await xx.delete()
        if thumb:
            os.remove(thumb)
