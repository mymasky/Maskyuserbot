# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk DM**

๏ **Perintah:** `dm` <username/id> <reply/type>`
◉ **Keterangan:** Kirim pesan pribadi ke pengguna.
"""

from . import HNDLR, eod, get_string, ayra_cmd


@ayra_cmd(pattern="[dD][mM]( (.*)|$)", fullsudo=True)
async def dm(e):
    if len(e.text.split()) <= 1:
        return await e.eor(get_string("dm_1"), time=5)
    chat = e.text.split()[1]
    try:
        chat_id = await e.client.parse_id(chat)
    except Exception as ex:
        return await e.eor(f"`{ex}`", time=5)
    if len(e.text.split()) > 2:
        msg = e.text.split(maxsplit=2)[2]
    elif e.reply_to:
        msg = await e.get_reply_message()
    else:
        return await e.eor(get_string("dm_2"), time=5)
    try:
        _ = await e.client.send_message(chat_id, msg)
        n_, time = get_string("dm_3"), None
        if not _.is_private:
            n_ = f"[{n_}]({_.message_link})"
        await e.eor(n_, time=time)
    except Exception as m:
        await e.eor(get_string("dm_4").format(m, HNDLR), time=5)