# Ayra - UserBot
# Copyright (C) 2021-2022 senpai80
#
# This file is a part of < https://github.com/senpai80/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/senpai80/Ayra/blob/main/LICENSE/>.

from . import get_help



import os
import sys
import time
from datetime import datetime
from platform import python_version as pyver
from random import choice

from telethon import __version__
from telethon.errors.rpcerrorlist import (
    BotMethodInvalidError,
    ChatSendMediaForbiddenError,
)

from Ayra.version import __version__ as AyraVer
from Ayra.dB import DEVS
from Ayra.kynan import register
from . import *
from .music import *

try:
    from git import Repo
except ImportError:
    LOGS.error("bot: 'gitpython' module not found!")
    Repo = None

from telethon.utils import resolve_bot_file_id

from . import (
    ATRA_COL,
    LOGS,
    OWNER_NAME,
    AYRA_IMAGES,
    Button,
    Carbon,
    Telegraph,
    Var,
    allcmds,
    asst,
    bash,
    call_back,
    callback,
    def_logs,
    eor,
    get_string,
    heroku_logs,
    in_pattern,
    restart,
    shutdown,
    start_time,
    time_formatter,
    udB,
    ayra_cmd,
    ayra_version,
    updater,
)

piic ="https://graph.org/file/02f9ca4617cec58377b9d.jpg"

buttons = [
    [
        Button.url(get_string("bot_4"), "t.me/kynansupport"),
    ]
]

# Will move to strings
alive_txt = """
◈ ᴀʏʀᴀ ꭙ ᴜꜱᴇʀʙᴏᴛ​

  ◈ Version - {}
  ◈ Ayra - {}
  ◈ Telethon - {}
"""

in_alive = "<b>{}</b>\n\n<b>╼┅━━━━━━━━━━━┅╾</b>\n<b>❏ 𝙰𝚈𝚁𝙰-𝚅𝙴𝚁𝚂𝙸𝙾𝙽 :</b> <code>{}</code>\n<b>├ 𝙿𝚈-𝙰𝚈𝚁𝙰 :</b> <code>{}</code>\n<b>├ 𝙿𝚈𝚃𝙷𝙾𝙽 :</b> <code>{}</code>\n<b>├ 𝚄𝙿𝚃𝙸𝙼𝙴 :</b> <code>{}</code>\n<b>├ 𝙱𝚁𝙰𝙽𝙲𝙷</b> {}\n<b>╰ 𝙰𝚈𝚁𝙰-𝚄𝚂𝙴𝚁𝙱𝙾𝚃</b>\n<b>╼┅━━━━━━━━━━━┅╾</b>"

absen = [
    "**𝙃𝙖𝙙𝙞𝙧 𝙙𝙤𝙣𝙜 𝙏𝙤𝙙** 😁",
    "**𝙃𝙖𝙙𝙞𝙧 𝙆𝙖𝙠𝙖 𝙂𝙖𝙣𝙩𝙚𝙣𝙜** 😉",
    "**𝙂𝙪𝙖 𝙃𝙖𝙙𝙞𝙧 𝘾𝙤𝙣𝙩𝙤𝙡** 😁",
    "**𝙂𝙪𝙖 𝙃𝙖𝙙𝙞𝙧 𝙂𝙖𝙣𝙩𝙚𝙣𝙜** 🥵",
    "**𝙃𝙖𝙙𝙞𝙧 𝙉𝙜𝙖𝙗** 😎",
    "**𝙂𝙪𝙖 𝙃𝙖𝙙𝙞𝙧 𝘼𝙗𝙖𝙣𝙜** 🥺",
    "**𝙎𝙞 𝘾𝙖𝙠𝙚𝙥 𝙃𝙖𝙙𝙞𝙧 𝘽𝙖𝙣𝙜** 😎",
    "**Hadir kak maap telat** 🥺",
    "**Hadir Tuan** 🙏🏻",
    "**Hadir Majikan** 🙏🏻",
    "**Hadir Sayang** 😳",
    "**Hadir Bro Kynan** 😁",
    "**Maaf ka habis nemenin ka Kynan** 🥺",
    "**Maaf ka habis disuruh Tuan Kynan** 🥺🙏🏻",
    "**Hadir Kynan Sayang** 😘",
    "**Hadir Kynan Akuuuuhhh** ☺️",
    "**Hadir Kynan brother Aku** 🥰",
]


@callback("alive")
async def alive(event):
    text = alive_txt.format(ayra_version, AyraVer, __version__)
    await event.answer(text, alert=True)
    

@register(incoming=True, from_users=DEVS, pattern=r"^Absen$")
async def kynanabsen(ganteng):
    await ganteng.reply(choice(absen))

@register(incoming=True, from_users=DEVS, pattern=r"^Kynan")
async def naya(naya):
    await naya.reply("**Kynan Punya Nya Naya**🤩")

@ayra_cmd(
    pattern=r"^[aA][lL][iI][vV][eE](?: |$)(.*)")
async def lol(ayra):
    match = ayra.pattern_match.group(1).strip()
    inline = True
    if match not in ["n", "no_inline"]:
        try:
            res = await ayra.client.inline_query(asst.me.username, "alive")
            return await res[0].click(ayra.chat_id)
        except BotMethodInvalidError:
            pass
        except BaseException as er:
            LOGS.exception(er)
        inline = True
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f" `[{y}]({rep})` "
    if inline:
        kk = f"<a href={rep}>{y}</a>"
        parse = "html"
        als = in_alive.format(
            OWNER_NAME,
            f"{ayra_version} [{HOSTED_ON}]",
            AyraVer,
            pyver(),
            uptime,
            kk,
        )

        if _e := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("", _e)
    else:
        parse = "md"
        als = (get_string("alive_1")).format(
            header,
            OWNER_NAME,
            f"{ayra_version} [{HOSTED_ON}]",
            AyraVer,
            uptime,
            pyver(),
            __version__,
            kk,
        )

        if a := udB.get_key("ALIVE_EMOJI"):
            als = als.replace("", a)
    if pic:
        try:
            await ayra.reply(
                als,
                file=pic,
                parse_mode=parse,
                link_preview=False,
                buttons=buttons if inline else None,
            )
            return await ayra.try_delete()
        except ChatSendMediaForbiddenError:
            pass
        except BaseException as er:
            LOGS.exception(er)
            try:
                await ayra.reply(file=pic)
                await ayra.reply(
                    als,
                    parse_mode=parse,
                    buttons=buttons if inline else None,
                    link_preview=False,
                )
                return await ayra.try_delete()
            except BaseException as er:
                LOGS.exception(er)
    await eor(
        ayra,
        als,
        parse_mode=parse,
        link_preview=False,
        buttons=buttons if inline else None,
    )

"""
@ayra_cmd(pattern="ping$", incoming=True, from_users=DEVS, chats=[], type=["official", "assistant"])
async def _(event):
    start = time.time()
    x = await event.eor("Pong !")
    end = round((time.time() - start) * 1000)
    uptime = time_formatter((time.time() - start_time) * 1000)
    await x.edit(get_string("ping").format(end, uptime))
"""

async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "Jam", "Hari"]

    while count < 4:
        count += 1
        remainder, result = divmod(
            seconds, 60) if count < 3 else divmod(
            seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)

    return up_time


@ayra_cmd(pattern="ping", chats=[], type=["official", "assistant"])
@register(incoming=True, from_users=DEVS, pattern=r"^Cping$")
async def _(ping):
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    ping = await eor(ping, "**✧**")
    await ping.edit("**✧✧**")
    await ping.edit("**✧✧✧**")
    await ping.edit("**✧✧✧✧**")
    await ping.edit("**✧✧✧✧✧**")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    user = await ping.client.get_me()
    await ping.edit(
        f"**❏ 𝙰𝚈𝚁𝙰-𝚄𝚂𝙴𝚁𝙱𝙾𝚃**\n"
        f"**├ 𝙿𝙸𝙽𝙶𝙴𝚁 :** `%sms`\n"
        f"**├ 𝚄𝙿𝚃𝙸𝙼𝙴 :** `{uptime}` \n"
        f"**╰ 𝙾𝚆𝙽𝙴𝚁 :** [{user.first_name}](tg://user?id={user.id})" % (duration)
    )

@ayra_cmd(
    pattern="cmds$",
)
async def cmds(event):
    await allcmds(event, Telegraph)


heroku_api = Var.HEROKU_API


@ayra_cmd(
    pattern="(r|R)estart$",
    fullsudo=False,
)
async def restart(e):
    ok = await e.eor(get_string("bot_5"))
    call_back()
    who = "bot" if e.client._bot else "user"
    udB.set_key("_RESTART", f"{who}_{e.chat_id}_{ok.id}")
    if heroku_api:
        return await restart(ok)
    await bash("git pull && pip3 install -r requirements.txt")
    os.execl(sys.executable, sys.executable, "-m", "Ayra")


@ayra_cmd(
    pattern="(s|S)hutdown$",
    fullsudo=False,
)
async def shutdownbot(ayra):
    await shutdown(ayra)


@ayra_cmd(
    pattern="(l|L)ogs( (.*)|$)",
    chats=[],
)
async def _(event):
    opt = event.pattern_match.group(1).strip()
    file = f"ayra{sys.argv[-1]}.log" if len(sys.argv) > 1 else "ayra.log"
    if opt == "heroku":
        await heroku_logs(event)
    elif opt == "carbon" and Carbon:
        event = await event.eor(get_string("com_1"))
        with open(file, "r") as f:
            code = f.read()[-2500:]
        file = await Carbon(
            file_name="ayra-logs",
            code=code,
            backgroundColor=choice(ATRA_COL),
        )
        await event.reply("**Ayra Logs.**", file=file)
    elif opt == "open":
        with open("ayra.log", "r") as f:
            file = f.read()[-4000:]
        return await event.eor(f"`{file}`")
    else:
        await def_logs(event, file)
    await event.try_delete()


@in_pattern("alive", owner=True)
async def inline_alive(ayra):
    pic = udB.get_key("ALIVE_PIC")
    if isinstance(pic, list):
        pic = choice(pic)
    uptime = time_formatter((time.time() - start_time) * 1000)
    header = udB.get_key("ALIVE_TEXT") or get_string("bot_1")
    y = Repo().active_branch
    xx = Repo().remotes[0].config_reader.get("url")
    rep = xx.replace(".git", f"/tree/{y}")
    kk = f"<a href={rep}>{y}</a>"
    als = in_alive.format(
        OWNER_NAME, f"{ayra_version} [{HOSTED_ON}]", AyraVer, pyver(), uptime, kk
    )

    if _e := udB.get_key("ALIVE_EMOJI"):
        als = als.replace("", _e)
    builder = ayra.builder
    if pic:
        try:
            if ".jpg" in pic:
                results = [
                    await builder.photo(
                        pic, text=als, parse_mode="html", buttons=buttons
                    )
                ]
            else:
                if _pic := resolve_bot_file_id(pic):
                    pic = _pic
                    buttons.insert(
                        0, [Button.inline(get_string("bot_2"), data="alive")]
                    )
                results = [
                    await builder.document(
                        pic,
                        title="Inline Alive",
                        description="↻ꝛɪᴢ",
                        parse_mode="html",
                        buttons=buttons,
                    )
                ]
            return await ayra.answer(results)
        except BaseException as er:
            LOGS.info(er)
    result = [
        await builder.article(
            "Alive", text=als, parse_mode="html", link_preview=False, buttons=buttons
        )
    ]
    await ayra.answer(result)


@ayra_cmd(pattern=r"^[uU][pP][dD][aA][tT][eE](?: |$)(.*)")
async def _(e):
    xx = await e.eor(get_string("upd_1"))
    if e.pattern_match.group(1).strip() and (
        "fast" in e.pattern_match.group(1).strip()
        or "soft" in e.pattern_match.group(1).strip()
    ):
        await bash("git pull -f && pip3 install -r requirements.txt")
        call_back()
        await xx.edit(get_string("upd_7"))
        os.execl(sys.executable, "python3", "-m", "Ayra")
        # return
    m = await updater()
    branch = (Repo.init()).active_branch
    if m:
        x = await asst.send_file(
            udB.get_key("LOG_CHANNEL"),
            piic,
            caption="• **Pembaruan tersedia** •",
            force_document=False,
            buttons=Button.inline("Changelog", data="changes"),
        )
        Link = x.message_link
        await xx.edit(
            f'<strong><a href="{Link}">[ChangeLogs]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )
    else:
        await xx.edit(
            f'<code>Your BOT is </code><strong>up-to-date</strong><code> with </code><strong><a href="https://github.com/naya1503/Ayra/tree/{branch}">[{branch}]</a></strong>',
            parse_mode="html",
            link_preview=False,
        )


@callback("updtavail", owner=True)
async def updava(event):
    await event.delete()
    await asst.send_file(
        udB.get_key("LOG_CHANNEL"),
        caption="• **Pembaruan tersedia** •",
        force_document=False,
        buttons=Button.inline("Changelog", data="changes"),
    )
