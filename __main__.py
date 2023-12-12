import glob
import os
import sys
from pathlib import Path

from KiaraConfig import Config

from TelethonKiara.clients.logger import LOGGER as LOGS
from TelethonKiara.clients.session import H2, H3, H4, H5, Kiara, KiaraBot
from TelethonKiara.utils.plug import load_module, plug_channel
from TelethonKiara.utils.startup import (join_it, logger_check, start_msg,
                                        update_sudo)
from TelethonKiara.version import __kiaraver__

# Global Variables #
KIARA_PIC = "https://te.legra.ph/file/474662f27cd60c1aa5c8d.jpg"


# Client Starter
async def kiaras(session=None, client=None, session_name="Main"):
    num = 0
    if session:
        LOGS.info(f"••• Starting Client [{session_name}] •••")
        try:
            await client.start()
            num = 1
        except:
            LOGS.error(f"Error in {session_name}!! Check & try again!")
    return num


# Load plugins based on config UNLOAD
async def plug_load(path):
    files = glob.glob(path)
    for name in files:
        with open(name) as kiara:
            path1 = Path(kiara.name)
            shortname = path1.stem
            if shortname.replace(".py", "") in Config.UNLOAD:
                os.remove(Path(f"TelethonKiara/plugins/{shortname}.py"))
            else:
                load_module(shortname.replace(".py", ""))


# Final checks after startup
async def kiara_is_on(total):
    await update_sudo()
    await logger_check(Kiara)
    await start_msg(KiaraBot, KIARA_PIC, __kiaraver__, total)
    await join_it(Kiara)
    await join_it(H2)
    await join_it(H3)
    await join_it(H4)
    await join_it(H5)


# Kiarabot starter...
async def start_kiarabot():
    try:
        tbot_id = await KiaraBot.get_me()
        Config.BOT_USERNAME = f"@{tbot_id.username}"
        Kiara.tgbot = KiaraBot
        LOGS.info("••• Starting KiaraBot (TELETHON) •••")
        C1 = await kiaras(Config.KIARABOT_SESSION, Kiara, "KIARABOT_SESSION")
        C2 = await kiaras(Config.SESSION_2, H2, "SESSION_2")
        C3 = await kiaras(Config.SESSION_3, H3, "SESSION_3")
        C4 = await kiaras(Config.SESSION_4, H4, "SESSION_4")
        C5 = await kiaras(Config.SESSION_5, H5, "SESSION_5")
        await KiaraBot.start()
        total = C1 + C2 + C3 + C4 + C5
        LOGS.info("••• KiaraBot Startup Completed •••")
        LOGS.info("••• Starting to load Plugins •••")
        await plug_load("TelethonKiara/plugins/*.py")
        await plug_channel(Kiara, Config.PLUGIN_CHANNEL)
        LOGS.info("⚡ Your KiaraBot Is Now Working ⚡")
        LOGS.info("Head to @Its_KiaraBot for Updates. Also join chat group to get help regarding KiaraBot.")
        LOGS.info(f"» Total Clients = {str(total)} «")
        await kiara_is_on(total)
    except Exception as e:
        LOGS.error(f"{str(e)}")
        sys.exit()


Kiara.loop.run_until_complete(start_kiarabot())

if len(sys.argv) not in (1, 3, 4):
    Kiara.disconnect()
else:
    try:
        Kiara.run_until_disconnected()
    except ConnectionError:
        pass


# kiarabot
