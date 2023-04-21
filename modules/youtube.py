# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.
"""
✘ **Bantuan Untuk Youtube**

๏ **Perintah:** Video
◉ **Keterangan:** Unduh Video Dari Youtube.

๏ **Perintah:** Song
◉ **Keterangan:** Unduh Lagu Dari Youtube.
"""
import os
from asyncio import get_event_loop
from functools import partial
import wget
from . import *
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL


def run_sync(func, *args, **kwargs):
    return get_event_loop().run_in_executor(None, partial(func, *args, **kwargs))


@ayra_cmd(pattern="(v|V)ideo( (.*)|$)")
async def yt_video(e):
    infomsg = await e.reply("**🔍 Pencarian...**", quote=False)
    try:
        search = SearchVideos(str(e.text.split(None, 1)[1]), offset=1, mode="dict", max_results=1).result().get("search_result")
        link = f"https://youtu.be/{search[0]['id']}"
    except Exception as error:
        return await infomsg.edit(f"**🔍 Pencarian...\n\n❌ Error: {error}**")
    ydl = YoutubeDL(
        {
            "quiet": True,
            "no_warnings": True,
            "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    )
    await infomsg.edit(f"**📥 Downloader...**")
    try:
        ytdl_data = await run_sync(ydl.extract_info, link, download=True)
        file_path = ydl.prepare_filename(ytdl_data)
        videoid = ytdl_data["id"]
        title = ytdl_data["title"]
        url = f"https://youtu.be/{videoid}"
        duration = ytdl_data["duration"]
        channel = ytdl_data["uploader"]
        views = f"{ytdl_data['view_count']:,}".replace(",", ".")
        thumbs = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg" 
    except Exception as error:
        return await infomsg.edit(f"**📥 Downloader...\n\n❌ Error: {error}**")
    thumbnail = wget.download(thumbs)
    await ayra_bot.send_video(
        message.chat.id,
        video=file_path,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption="**💡 Informasi {}**\n\n**🏷 Nama:** {}\n**🧭 Durasi:** {}\n**👀 Dilihat:** {}\n**📢 Channel:** {}\n**🔗 Tautan:** <a href={}>Youtube</a>\n\n**".format(
            "video",
            title,
            duration,
            views,
            channel,
            url,
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_path):
        if files and os.path.exists(files):
            os.remove(files)


@ayra_cmd(pattern="(s|S)ong( (.*)|$)")
async def yt_audio(e):
    infomsg = await e.reply("**🔍 Pencarian...**", quote=False)
    try:
        search = SearchVideos(str(e.text.split(None, 1)[1]), offset=1, mode="dict", max_results=1).result().get("search_result")
        link = f"https://youtu.be/{search[0]['id']}"
    except Exception as error:
        return await infomsg.edit(f"**🔍 Pencarian...\n\n❌ Error: {error}**")
    ydl = YoutubeDL(
        {
            "quiet": True,
            "no_warnings": True,
            "format": "bestaudio[ext=m4a]",
            "outtmpl": "downloads/%(id)s.%(ext)s",
            "nocheckcertificate": True,
            "geo_bypass": True,
        }
    )
    await infomsg.edit(f"**📥 Downloader...**")
    try:
        ytdl_data = await run_sync(ydl.extract_info, link, download=True)
        file_path = ydl.prepare_filename(ytdl_data)
        videoid = ytdl_data["id"]
        title = ytdl_data["title"]
        url = f"https://youtu.be/{videoid}"
        duration = ytdl_data["duration"]
        channel = ytdl_data["uploader"]
        views = f"{ytdl_data['view_count']:,}".replace(",", ".")
        thumbs = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg" 
    except Exception as error:
        return await infomsg.edit(f"**📥 Downloader...\n\n❌ Error: {error}**")
    thumbnail = wget.download(thumbs)
    await ayra_bot.send_audio(
        message.chat.id,
        audio=file_path,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        caption="**💡 Informasi {}**\n\n**🏷 Nama:** {}\n**🧭 Durasi:** {}\n**👀 Dilihat:** {}\n**📢 Channel:** {}\n**🔗 Tautan:** <a href={}>Youtube</a>\n\n**".format(
            "Audio",
            title,
            duration,
            views,
            channel,
            url,
        ),
        reply_to_message_id=message.id,
    )
    await infomsg.delete()
    for files in (thumbnail, file_path):
        if files and os.path.exists(files):
            os.remove(files)
