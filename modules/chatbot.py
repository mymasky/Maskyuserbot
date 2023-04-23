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

from telethon.errors import MessageNotModifiedError
from . import ayra_cmd, udB, eor
from .database.ai import OpenAi

@ayra_cmd(pattern="ai( (.*)|$)")
async def openai(event):
    question = event.pattern_match.group(2)
    if not question:
        await event.eor("`Mohon berikan pertanyaan untuk menggunakan AI.`")
        return
    msg = await event.eor("`Processing...`")
    try:
        response = OpenAi().text(question)
        await msg.eor(f"**Q:** {question}\n\n**A:** {response}")
    except Exception as e:
        await msg.eor(f"**Q:** {question}\n\n**A:** `Error: {e}`")


@ayra_cmd(pattern="img( (.*)|$)")
async def imge(event):
    question = event.pattern_match.group(2)
    if not question:
        await event.eor("`Mohon berikan pertanyaan untuk menggunakan AI.`")
        return
    msg = await event.eor("`Processing...`")
    try:
        response = OpenAi().photo(question)
        await event.client.send_photo(event.chat_id, response, reply_to=event.message.id)
        await msg.delete()
    except Exception as error:
        await event.eor(str(error))

