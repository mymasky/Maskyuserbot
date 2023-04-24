
import os
import re

from telegraph import upload_file as uf
from telethon.utils import pack_bot_file_id
from telethon import Button
from . import HNDLR, get_string, mediainfo, ayra_cmd

from ._inline import something

def get_msg_button(texts: str):
    btn = []
    for z in re.findall("\\[(.*?)\\|(.*?)\\]", texts):
        text, url = z
        btn.append([text, url])

    txt = texts
    for z in re.findall("\\[.+?\\|.+?\\]", texts):
        txt = txt.replace(z, "")

    return txt.strip(), btn
    
    
def create_tl_btn(button: list):
    btn = []
    for z in button:
        if len(z) > 1:
            kk = [Button.url(*x.strip().split("|")) for x in z]
            btn.append(kk)
        else:
            kk = [Button.url(*z[0][1].strip().split("|"))]
            btn.append(kk)
    return btn



def format_btn(buttons: list):
    txt = ""
    for i in buttons:
        a = 0
        for j, btn in enumerate(i):
            if hasattr(btn.button, "url"):
                a += 1
                if j > 0 and i[j-1].button.url == btn.button.url:
                    txt += f"[{btn.button.text} | {btn.button.url} | same]"
                else:
                    txt += f"[{btn.button.text} | {btn.button.url}]"
        txt += '\n'
    _, btn = get_msg_button(txt)
    return btn



@ayra_cmd(pattern="button")
async def butt(event):
    media, wut, text = None, None, None
    if event.reply_to:
        wt = await event.get_reply_message()
        if wt.text:
            text = wt.text
        if wt.media:
            wut = mediainfo(wt.media)
        if wut and wut.startswith(("pic", "gif")):
            dl = await wt.download_media()
            variable = uf(dl)
            media = f"https://graph.org{variable[0]}"
        elif wut == "video":
            if wt.media.document.size > 8 * 1000 * 1000:
                return await event.eor(get_string("com_4"), time=5)
            dl = await wt.download_media()
            variable = uf(dl)
            os.remove(dl)
            media = f"https://graph.org{variable[0]}"
        else:
            media = pack_bot_file_id(wt.media)
    try:
        text = event.text.split(maxsplit=1)[1]
    except IndexError:
        if not text:
            return await event.eor(
                f"**Please give some text in correct format.**\n\n`{HNDLR}help button`",
            )
    text, buttons = get_msg_button(text)
    if buttons:
        buttons = create_tl_btn(buttons)
    await something(event, text, media, buttons)
    await event.delete()
