# @riizzvbss
"""
◈ Perintah Tersedia

• `{i}ass`
   Salam Lengkap

• `{i}as`
   Assalamu'alaikum

• `{i}ws`
   Jawab Salam
   
• `{i}ks`
   Kenalan Salam
   
• `{i}jws`
   Istighfar Salam
   
• `{i}3x`
    Bisa Kali

• `{i}kg`
    Keren lu gitu
"""

from time import sleep
from . import (
    eor,
    ayra_cmd,
)

@ayra_cmd(pattern="ass$")
async def _(event):
    await event.eor("**Assalamu'alaikum Warohmatulohi Wabarokatu**")


@ayra_cmd(pattern="as$")
async def _(event):
    await event.eor("**Assalamu'alaikum**")
    
@ayra_cmd(pattern="ws$")
async def _(event):
    await event.eor("**Wa'alaikumussalam**")

    
@ayra_cmd(pattern="ks$")
async def _(event):
    xx = await event.eor(f"**Hy kaa 🥺**")
    sleep(2)
    await xx.edit("**Assalamualaikum...**")


@ayra_cmd(pattern="jws$")
async def _(event):
    xx = await event.eor(event,f"**Astaghfirullah, Jawab salam dong**")
    sleep(2)
    await xx.edit("**Assalamu'alaikum**")


@ayra_cmd(pattern="3x$")
async def _(event):
    xx = await event.eor(f"**Bismillah, 3x**")
    sleep(2)
    await xx.edit("**Assalamu'alaikum Bisa Kali**")
    
@ayra_cmd(pattern="kg$")
async def _(event):
    xx = await event.eor(f"**Lu Ngapah Begitu ?**")
    sleep(2)
    await xx.edit("**Keren Lu Begitu ?**")
