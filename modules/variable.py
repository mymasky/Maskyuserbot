# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Variable**

๏ **Perintah:** `get keys`
◉ **Keterangan:** Mengambil semua variable didatabase.

๏ **Perintah:** `get db` <nama variable>
◉ **Keterangan:** Mengambil value dari variable tersebut.

๏ **Perintah:** `setdb` <variable> <value>
◉ **Keterangan:** Atur variable dengan value.

๏ **Perintah:** `deldb` <variable
◉ **Keterangan:** Menghapus variable beserta value didatabase.

◉ **Contoh :** `setdb HNDLR !` => Ini akan mengatur
HNDLR anda menjadi `!`, default nya adalah `.`

**Harap melakukan Restart setelah mengatur db**.
"""

import os
import re

from . import *

@ayra_cmd(pattern="[sS][e][t][d][b]( (.*)|$)", fullsudo=False)
async def _(event):
    match = event.pattern_match.group(1).strip()
    if not match:
        return await event.eor("Berikan kunci dan nilai untuk ditetapkan!")
    try:
        delim = " " if re.search("[|]", match) is None else " | "
        data = match.split(delim, maxsplit=1)
        if data[0] in ["--extend", "-e"]:
            data = data[1].split(maxsplit=1)
            data[1] = f"{str(udB.get_key(data[0]))} {data[1]}"
        udB.set_key(data[0], data[1])
        await event.eor(
            f"**Pasangan Nilai Kunci DB Diperbarui\nKunci :** `{data[0]}`\n**Value :** `{data[1]}`"
        )

    except BaseException:
        await event.eor(get_string("com_7"))


@ayra_cmd(pattern="[dD][e][l][d][b]( (.*)|$)", fullsudo=False)
async def _(event):
    key = event.pattern_match.group(1).strip()
    if not key:
        return await event.eor("Beri saya nama kunci untuk dihapus!", time=5)
    _ = key.split(maxsplit=1)
    try:
        if _[0] == "-m":
            for key in _[1].split():
                k = udB.del_key(key)
            key = _[1]
        else:
            k = udB.del_key(key)
        if k == 0:
            return await event.eor("`Tidak Ada Kunci Seperti Itu.`")
        await event.eor(f"`Kunci berhasil dihapus {key}`")
    except BaseException:
        await event.eor(get_string("com_7"))

@ayra_cmd(pattern="[gG][e][t]($| (.*))", fullsudo=False)
async def get_var(event):
    try:
        opt = event.text.split(maxsplit=2)[1]
    except IndexError:
        return await event.eor(f"Apaan ?\bBaca `{HNDLR}help variables`")
    x = await event.eor(get_string("com_1"))
    if opt != "keys":
        try:
            varname = event.text.split(maxsplit=2)[2]
        except IndexError:
            return await eor(x, "Var seperti itu tidak ada!", time=5)
    if opt == "var":
        c = 0
        # try redis
        val = udB.get_key(varname)
        if val is not None:
            c += 1
            await x.edit(
                f"**Variabel** - `{varname}`\n**Value**: `{val}`\n**Type**: Kunci Redis."
            )
        # try env vars
        val = os.getenv(varname)
        if val is not None:
            c += 1
            await x.edit(
                f"**Variable** - `{varname}`\n**Value**: `{val}`\n**Type**: Env Var."
            )

        if c == 0:
            await eor(x, "Such a var doesn't exist!", time=5)

    elif opt == "type":
        c = 0
        # try redis
        val = udB.get_key(varname)
        if val is not None:
            c += 1
            await x.edit(f"**Variable** - `{varname}`\n**Type**: Redis Key.")
        # try env vars
        val = os.getenv(varname)
        if val is not None:
            c += 1
            await x.edit(f"**Variable** - `{varname}`\n**Type**: Env Var.")

        if c == 0:
            await eor(x, "Such a var doesn't exist!", time=5)

    elif opt == "db":
        val = udB.get(varname)
        if val is not None:
            await x.edit(f"**Key** - `{varname}`\n**Value**: `{val}`")
        else:
            await eor(x, "No such key!", time=5)

    elif opt == "keys":
        keys = sorted(udB.keys())
        msg = "".join(
            f"• `{i}`" + "\n"
            for i in keys
            if not i.isdigit()
            and not i.startswith("-")
            and not i.startswith("_")
            and not i.startswith("GBAN_REASON_")
        )

        await x.edit(f"**Daftar Kunci DB :**\n{msg}")
