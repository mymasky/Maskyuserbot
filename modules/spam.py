# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
◈ Perintah Tersedia

• `{i}spam <angka> <tulis/balas pesan>`
    obrolan spam, batas saat ini adalah dari 1 hingga 99.

• `{i}bigspam <angka> <tulis/balas pesan>`
    Obrolan spam, batas saat ini di atas 100.

• `{i}delayspam <delay time> <count> <msg>`
    Obrolan spam dengan penundaan..

• `{i}tspam <text>`
    Obrolan Spam dengan Satu-Satu Karakter..
"""

import asyncio

from . import *


@ayra_cmd(pattern="tspam")
async def tmeme(e):
    tspam = str(e.text[7:])
    message = tspam.replace(" ", "")
    for letter in message:
        await e.respond(letter)
    await e.delete()


@ayra_cmd(pattern="spam")
async def spammer(e):
    message = e.text
    if e.reply_to:
        if not len(message.split()) >= 2:
            return await eod(e, "`Gunakan dalam Format yang Tepat`")
        spam_message = await e.get_reply_message()
    else:
        if not len(message.split()) >= 3:
            return await eod(e, "`Membalas Pesan atau Memberikan beberapa Teks ..`")
        spam_message = message.split(maxsplit=2)[2]
    counter = message.split()[1]
    try:
        counter = int(counter)
        if counter >= 100:
            return await eod(e, "`Gunakan bigspam`")
    except BaseException:
        return await eod(e, "`Gunakan dalam Format yang Tepat`")
    await asyncio.wait([e.respond(spam_message) for i in range(counter)])
    await e.delete()


@ayra_cmd(pattern="bigspam", fullsudo=True)
async def bigspam(e):
    message = e.text
    if e.reply_to:
        if not len(message.split()) >= 2:
            return await eod(e, "`Gunakan dalam Format yang Tepat`")
        spam_message = await e.get_reply_message()
    else:
        if not len(message.split()) >= 3:
            return await eod(e, "`Membalas Pesan atau Memberikan beberapa Teks ..`")
        spam_message = message.split(maxsplit=2)[2]
    counter = message.split()[1]
    try:
        counter = int(counter)
    except BaseException:
        return await eod(e, "`Gunakan dalam Format yang Tepat`")
    await asyncio.wait([e.respond(spam_message) for i in range(counter)])
    await e.delete()


@ayra_cmd(pattern="delayspam ?(.*)")
async def delayspammer(e):
    try:
        args = e.text.split(" ", 3)
        delay = float(args[1])
        count = int(args[2])
        msg = str(args[3])
    except BaseException:
        return await e.edit(f"**Penggunaan :** {HNDLR}delayspam <delay time> <count> <msg>")
    await e.delete()
    try:
        for i in range(count):
            await e.respond(msg)
            await asyncio.sleep(delay)
    except Exception as u:
        await e.respond(f"**Error :** `{u}`")
