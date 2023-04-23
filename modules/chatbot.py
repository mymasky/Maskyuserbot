# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Chatbot**

๏ **Perintah:** `ai` <balas pesan/berikan pertanyaan>
◉ **Keterangan:** Sangat berguna untuk kebutuhan.
"""
import os
import requests
import openai
import shutil
from telethon.errors import MessageNotModifiedError
from asyncio import gather
from io import *
from . import *
from .database.ai import *


@ayra_cmd(pattern="ai( (.*)|$)")
async def openai(event):
"""
    OPENAI_API = udB.get_key("OPENAI_API")
    if not OPENAI_API:
        return await event.eor(
            "Ambil OPENAI_API Anda [Disini](https://platform.openai.com/account/api-keys) kemudian ketik {HNDLR}setdb OPENAI_API <api_key>.",
        )
"""
    OPENAI_API = "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"
    question = await event.get_reply_message()
    if question:
        text = question.text
    else:
        text = event.pattern_match.group(2)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API}",
    }

    json_data = {
        "model": "text-davinci-003",
        "prompt": question,
        "max_tokens": 500,
        "temperature": 0,
    }
    msg = await event.eor("`Processing...`")
    try:
        response = (await requests.post("https://api.openai.com/v1/completions", headers=headers, json=json_data)).json()
        await msg.edit(response["choices"][0]["text"])
    except MessageNotModifiedError:
        pass
    except Exception:
        await msg.eor("`Data tidak ditemukan, pastikan OPENAI_API valid...`")
