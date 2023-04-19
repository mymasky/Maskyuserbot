# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

"""
◈ Perintah Tersedia

• `{i} makevoice` <balasan ke video>
        Membuat catatan suara dari video

• `{i} extractaudio` <balas ke video>
        Untuk mengekstrak audio dari video

• `{i} convert` <gif/img/stiker/webm> <balas ke file>

•`{i}glitch <balas ke gambar>`
      Memberikan gif glitchy.
      
•`{i}invertgif`
  Membuat Gif Terbalik(negative).

•`{i}bwgif`
  Jadikan Gif hitam putih

•`{i}rvgif`
  Balikkan gif

•`{i}vtog`
  Balas Ke Video, Ini akan Membuat Gif
  Video ke Gif

•`{i}gif <query>`
   Kirim video tentang kueri.
  
•`{i}size <reply to media>`
   Untuk mendapatkan ukurannya.

•`{i}resize <number> <number>`
   Untuk mengubah ukuran gambar pada sumbu x, y.
   eg. `{i}resize 690 960`
"""

import os
import time
import random

from . import LOGS

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from PIL import Image
except ImportError:
    LOGS.info(f"{__file__}: PIL  not Installed.")
    Image = None

from telegraph import upload_file as uf
from datetime import datetime as dt

from Ayra.fns.tools import set_attributes

from . import (
    LOGS,
    AyConfig,
    ayra_cmd,
    bash,
    downloader,
    eod,
    eor,
    genss,
    get_string,
    udB,
    uploader,
    humanbytes,
    get_paste,
    mediainfo,
    stdr,
    time_formatter,
    uploader,
)
opn = []

conv_keys = {
    "img": "png",
    "sticker": "webp",
    "webp": "webp",
    "image": "png",
    "webm": "webm",
    "gif": "gif",
    "json": "json",
    "tgs": "tgs",
}
@ayra_cmd(
    pattern="convert( (.*)|$)",
)
async def uconverter(event):
    xx = await event.eor(get_string("com_1"))
    a = await event.get_reply_message()
    if a is None:
        return await event.eor("`Balas ke Media...`")
    input_ = event.pattern_match.group(1).strip()
    b = await a.download_media("resources/downloads/")
    if not b and (a.document and a.document.thumbs):
        b = await a.download_media(thumb=-1)
    if not b:
        return await xx.edit(get_string("cvt_3"))
    try:
        convert = conv_keys[input_]
    except KeyError:
        return await xx.edit(get_string("sts_3").format("gif/img/sticker/webm/webp"))
    file = await con.convert(b, outname="ayra", convert_to=convert)
    if file:
        await event.client.send_file(
            event.chat_id, file, reply_to=event.reply_to_msg_id or event.id
        )
        os.remove(file)
    await xx.delete()

@ayra_cmd(pattern="makevoice$")
async def vnc(e):
    if not e.reply_to:
        return await eod(e, get_string("audiotools_1"))
    r = await e.get_reply_message()
    if not mediainfo(r.media).startswith(("audio", "video")):
        return await eod(e, get_string("spcltool_1"))
    xxx = await e.eor(get_string("com_1"))
    file, _ = await e.client.fast_downloader(
        r.document,
    )
    await xxx.edit(get_string("audiotools_2"))
    await bash(
        f"ffmpeg -i '{file.name}' -map 0:a -codec:a libopus -b:a 100k -vbr on out.opus"
    )
    try:
        await e.client.send_message(
            e.chat_id, file="out.opus", force_document=False, reply_to=r
        )
    except Exception as er:
        LOGS.exception(er)
        return await xxx.edit("`Gagal Mengonversi Audio...`")
    await xxx.delete()
    os.remove(file.name)
    os.remove("out.opus")


@ayra_cmd(pattern="toaudio$")
async def ex_aud(e):
    reply = await e.get_reply_message()
    if not (reply and reply.media and mediainfo(reply.media).startswith("video")):
        return await e.eor(get_string("audiotools_8"))
    name = reply.file.name or "video.mp4"
    vfile = reply.media.document
    msg = await e.eor(get_string("com_1"))
    c_time = time.time()
    file = await downloader(
        f"resources/downloads/{name}",
        vfile,
        msg,
        c_time,
        f"Mengunduh {name}...",
    )

    out_file = f"{file.name}.aac"
    cmd = f"ffmpeg -i {file.name} -vn -acodec copy {out_file}"
    o, err = await bash(cmd)
    os.remove(file.name)
    attributes = await set_attributes(out_file)

    f_time = time.time()
    try:
        fo = await uploader(out_file, out_file, f_time, msg, f"Mengunggah {out_file}...")

    except FileNotFoundError:
        return await eor(msg, get_string("audiotools_9"))
    await e.client.send_file(
        e.chat_id,
        fo,
        caption=get_string("audiotools_10"),
        thumb=AyConfig.thumb,
        attributes=attributes,
        reply_to=e.reply_to_msg_id,
    )
    await msg.delete()


@ayra_cmd(pattern="glitch$")
async def _(e):
    try:
        import glitch_me  # ignore :pylint
    except ModuleNotFoundError:
        await bash(
            "pip install -e git+https://github.com/1Danish-00/glitch_me.git#egg=glitch_me"
        )
    reply = await e.get_reply_message()
    if not reply or not reply.media:
        return await e.eor(get_string("cvt_3"))
    xx = await e.eor(get_string("glitch_1"))
    wut = mediainfo(reply.media)
    if wut.startswith(("pic", "sticker")):
        ok = await reply.download_media()
    elif reply.document and reply.document.thumbs:
        ok = await reply.download_media(thumb=-1)
    else:
        return await xx.eor(get_string("com_4"))
    cmd = f"glitch_me gif --line_count 200 -f 10 -d 50 '{ok}' ayra.gif"
    stdout, stderr = await bash(cmd)
    await e.reply(file="ayra.gif", force_document=False)
    await xx.delete()
    os.remove(ok)
    os.remove("ayra.gif")
    
    
@ayra_cmd(pattern="(bw|invert)gif$")
async def igif(e):
    match = e.pattern_match.group(1).strip()
    a = await e.get_reply_message()
    if not (a and a.media):
        return await e.eor("`Reply To gif only`", time=5)
    wut = mediainfo(a.media)
    if "gif" not in wut:
        return await e.eor("`Reply To Gif Only`", time=5)
    xx = await e.eor(get_string("com_1"))
    z = await a.download_media()
    if match == "bw":
        cmd = f'ffmpeg -i "{z}" -vf format=gray ayra.gif -y'
    else:
        cmd = f'ffmpeg -i "{z}" -vf lutyuv="y=negval:u=negval:v=negval" ayra.gif -y'
    try:
        await bash(cmd)
        await e.client.send_file(e.chat_id, "ayra.gif", supports_streaming=True)
        os.remove(z)
        os.remove("ayra.gif")
        await xx.delete()
    except Exception as er:
        LOGS.info(er)


@ayra_cmd(pattern="rvgif$")
async def reverse_gif(event):
    a = await event.get_reply_message()
    if not (a and a.media) and "video" not in mediainfo(a.media):
        return await e.eor("`Balas ke Video saja`", time=5)
    msg = await event.eor(get_string("com_1"))
    file = await a.download_media()
    await bash(f'ffmpeg -i "{file}" -vf reverse -af areverse reversed.mp4 -y')
    await event.respond("- **Video/GIF Terbalik**", file="reversed.mp4")
    await msg.delete()
    os.remove(file)
    os.remove("reversed.mp4")


@ayra_cmd(pattern="gif( (.*)|$)")
async def gifs(ayra):
    get = ayra.pattern_match.group(1).strip()
    xx = random.randint(0, 5)
    n = 0
    if ";" in get:
        try:
            n = int(get.split(";")[-1])
        except IndexError:
            pass
    if not get:
        return await ayra.eor(f"`{HNDLR}gif <query>`")
    m = await ayra.eor(get_string("com_2"))
    gifs = await ayra.client.inline_query("gif", get)
    if not n:
        await gifs[xx].click(
            ayra.chat_id, reply_to=ayra.reply_to_msg_id, silent=True, hide_via=True
        )
    else:
        for x in range(n):
            await gifs[x].click(
                ayra.chat_id, reply_to=ayra.reply_to_msg_id, silent=True, hide_via=True
            )
    await m.delete()


@ayra_cmd(pattern="vtog$")
async def vtogif(e):
    a = await e.get_reply_message()
    if not (a and a.media):
        return await e.eor("`Reply To video only`", time=5)
    wut = mediainfo(a.media)
    if "video" not in wut:
        return await e.eor("`Reply To Video Only`", time=5)
    xx = await e.eor(get_string("com_1"))
    dur = a.media.document.attributes[0].duration
    tt = time.time()
    if int(dur) < 120:
        z = await a.download_media()
        await bash(
            f'ffmpeg -i {z} -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 ayra.gif -y'
        )
    else:
        filename = a.file.name
        if not filename:
            filename = "video_" + dt.now().isoformat("_", "seconds") + ".mp4"
        vid = await downloader(filename, a.media.document, xx, tt, get_string("com_5"))
        z = vid.name
        await bash(
            f'ffmpeg -ss 3 -t 100 -i {z} -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 ayra.gif'
        )

    await e.client.send_file(e.chat_id, "ayra.gif", support_stream=True)
    os.remove(z)
    os.remove("ayra.gif")
    await xx.delete()
    
@ayra_cmd(pattern="size$")
async def size(e):
    r = await e.get_reply_message()
    if not (r and r.media):
        return await e.eor(get_string("ascii_1"))
    k = await e.eor(get_string("com_1"))
    if hasattr(r.media, "document"):
        img = await e.client.download_media(r, thumb=-1)
    else:
        img = await r.download_media()
    im = Image.open(img)
    x, y = im.size
    await k.edit(f"Dimensi Gambar Ini Adalah\n`{x} x {y}`")
    os.remove(img)


@ayra_cmd(pattern="resize( (.*)|$)")
async def size(e):
    r = await e.get_reply_message()
    if not (r and r.media):
        return await e.eor(get_string("ascii_1"))
    sz = e.pattern_match.group(1).strip()
    if not sz:
        return await eor(
            f"Berikan Beberapa Ukuran Untuk Diubah Ukurannya, Seperti `{HNDLR}resize 720 1080` ", time=5
        )
    k = await e.eor(get_string("com_1"))
    if hasattr(r.media, "document"):
        img = await e.client.download_media(r, thumb=-1)
    else:
        img = await r.download_media()
    sz = sz.split()
    if len(sz) != 2:
        return await eor(
            k, f"Berikan Beberapa Ukuran Untuk Diubah Ukurannya, Seperti `{HNDLR}resize 720 1080` ", time=5
        )
    x, y = int(sz[0]), int(sz[1])
    im = Image.open(img)
    ok = im.resize((x, y))
    ok.save(img, format="PNG", optimize=True)
    await e.reply(file=img)
    os.remove(img)
    await k.delete()