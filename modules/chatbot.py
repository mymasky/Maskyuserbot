import os
import requests
import shutil

from asyncio import gather
from io import *
from . import *
from .database.ai import *


@ayra_cmd(pattern=r"^ai"( (.*)|$)")
async def openai(event):
    OPENAI_API = udB.get_key("OPENAI_API")
    if not OPENAI_API:
        return await event.eor(
            "Ambil OPENAI_API Anda [Disini](https://platform.openai.com/account/api-keys) kemudian ketik {HNDLR}setdb OPENAI_API <api_key>.",
        )
    question = await event.get_reply_message()
    if question:
        text = question.text
    else:
        text = event.pattern_match.group(3)
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
    msg = await event.eor("`Processing..")
    try:
        response = (await requests.post("https://api.openai.com/v1/completions", headers=headers, json=json_data)).json()
        await msg.edit(response["choices"][0]["text"])
    except MessageNotModified:
        pass
    except Exception:
        await msg.eor("`Data tidak ditemukan, pastikan OPENAI_API valid...`")
