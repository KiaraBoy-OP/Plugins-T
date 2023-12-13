import datetime
import random
import time
from unicodedata import name

from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot
from TelethonKiara.DB.gvar_sql import gvarstat, addgvar
from TelethonKiara.plugins import *

# -------------------------------------------------------------------------------

ALIVE_TEMP = """
<b><i>🔥🔥ɥʂɛʀɮօt ɨs օռʟɨռɛ🔥🔥</i></b>
<b><i>↼ Øwñêr ⇀</i></b> : 『 {kiara_mention} 』
╭──────────────
┣─ <b>» Telethon:</b> <i>{telethon_version}</i>
┣─ <b>» Ừʂɛɤẞø†:</b> <i>{kiarabot_version}</i>
┣─ <b>» Sudo:</b> <i>{is_sudo}</i>
┣─ <b>» Uptime:</b> <i>{uptime}</i>
┣─ <b>» Ping:</b> <i>{ping}</i>
╰──────────────
<b><i>»»» <a href='https://t.me/Shadow_Boy_2005'>[𝚂𝙷𝙰𝙳𝙾𝚆 𝙱𝙾𝚈]</a> «««</i></b>
"""

msg = """{}\n
<b><i>🏅 𝙱𝚘𝚝 𝚂𝚝𝚊𝚝𝚞𝚜 🏅</b></i>
<b>Telethon ≈</b>  <i>{}</i>
<b>Ừʂɛɤẞø† ≈</b>  <i>{}</i>
<b>Uptime ≈</b>  <i>{}</i>
<b>Abuse ≈</b>  <i>{}</i>
<b>Sudo ≈</b>  <i>{}</i>
"""
# -------------------------------------------------------------------------------


@kiara_cmd(pattern="alivetemp$")
async def set_alive_temp(event):
    kiara = await eor(event, "`Fetching template ...`")
    reply = await event.get_reply_message()
    if not reply:
        alive_temp = gvarstat("ALIVE_TEMPLATE") or ALIVE_TEMP
        to_reply = await kiara.edit("Below is your current alive template 👇")
        await event.client.send_message(event.chat_id, alive_temp, parse_mode=None, link_preview=False, reply_to=to_reply)
        return
    addgvar("ALIVE_TEMPLATE", reply.text)
    await kiara.edit(f"`ALIVE_TEMPLATE` __changed to:__ \n\n`{reply.text}`")


@kiara_cmd(pattern="alive$")
async def _(event):
    start = datetime.datetime.now()
    userid, kiara_user, kiara_mention = await client_id(event, is_html=True)
    kiara = await eor(event, "`Building Alive....`")
    reply = await event.get_reply_message()
    uptime = await get_time((time.time() - StartTime))
    name = gvarstat("ALIVE_NAME") or kiara_user
    alive_temp = gvarstat("ALIVE_TEMPLATE") or ALIVE_TEMP
    a = gvarstat("ALIVE_PIC")
    pic_list = []
    if a:
        b = a.split(" ")
        if len(b) >= 1:
            for c in b:
                pic_list.append(c)
        PIC = random.choice(pic_list)
    else:
        PIC = "https://te.legra.ph/file/8e99869e89c6aba9b3968.mp4"
    end = datetime.datetime.now()
    ping = (end - start).microseconds / 1000
    alive = alive_temp.format(
        kiara_mention=kiara_mention,
        telethon_version=telethon_version,
        kiarabot_version=kiarabot_version,
        is_sudo=is_sudo,
        uptime=uptime,
        ping=ping,
    )
    await event.client.send_file(
        event.chat_id,
        file=PIC,
        caption=alive,
        reply_to=reply,
        parse_mode="HTML",
    )
    await kiara.delete()


@kiara_cmd(pattern="kiara$")
async def kiara_a(event):
    userid, _, _ = await client_id(event)
    uptime = await get_time((time.time() - StartTime))
    am = gvarstat("ALIVE_MSG") or "<b>»» ɥʂɛʀɮօt ιѕ σиℓιиє ««</b>"
    try:
        kiara = await event.client.inline_query(Config.BOT_USERNAME, "alive")
        await kiara[0].click(event.chat_id)
        if event.sender_id == userid:
            await event.delete()
    except (noin, dedbot, BotInlineDisabledError):  # Handle BotInlineDisabledError
        await eor(
            event,
            msg.format(am, telethon_version, kiarabot_version, uptime, abuse_m, is_sudo),
            parse_mode="HTML",
        )


CmdHelp("alive").add_command(
    "alive", None, "Shows the default Alive message."
).add_command(
    "kiara", None, "Shows inline Alive message."
).add_warning(
    "✅ Harmless Module"
).add()
