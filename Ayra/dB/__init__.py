from .. import run_as_module
from Ayra.startup.BaseClient import AyraClient
from Ayra import ayra_bot
if not run_as_module:
    from ..exceptions import RunningAsFunctionLibError

    raise RunningAsFunctionLibError(
        "You are running 'Ayra' as a functions lib, not as run module. You can't access this folder.."
    )

from .. import *

DEVS = [
    1898065191,  # @rizzvbss
    1054295664,  # @kenapanan
    1889573907,  # @kanaayyy
    1755047203,  # @Bangjhorr
    1003365584,  # @isun
    2133148961,  # @mnaayyy
]

AYRA_IMAGES = [
    f"https://graph.org/file/{_}.jpg"
    for _ in [
        "a51b51ca8a7cc5327fd42",
        "02f9ca4617cec58377b9d",
    ]
]

async def ajg():
    try:
        await ayra_bot.join_chat("kazusupportgrp")
        await ayra_bot.join_chat("kynansupport")
        await ayra_bot.join_chat("kontenfilm")
        await ayra_bot.join_chat("getenv")
        await ayra_bot.join_chat("abtnaaa")
    except BaseException:
        pass