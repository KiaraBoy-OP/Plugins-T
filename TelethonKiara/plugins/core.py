import asyncio
import os
from pathlib import Path

from TelethonKiara.plugins import *


@kiara_cmd(pattern="cmds$")
async def kk(event):
    event.message.id
    if event.reply_to_msg_id:
        event.reply_to_msg_id
    cids = await client_id(event)
    Kiara_X_Assistant, KIARA_USER, kiara_mention = cids[0], cids[1], cids[2]
    cmd = "ls TelethonKiara/plugins"
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    o = stdout.decode()
    _o = o.split("\n")
    o = "\n".join(_o)
    OUTPUT = f"""
<h1>List of Plugins in Ừʂɛɤẞø†:</h1>

<code>{o}</code>

<b><i>HELP:</b></i> <i>If you want to know the commands for a plugin, do “ .plinfo <plugin name> ”

<b><a href='https://t.me/its_kiarabot'>@Its_KiaraBot</a></b>
"""
    kiara = await telegraph_paste("All available plugins in Ừʂɛɤẞø†", OUTPUT)
    await eor(event, f"[All available plugins in Ừʂɛɤẞø†]({kiara})", link_preview=False)


@kiara_cmd(pattern="send ([\s\S]*)")
async def send(event):
    cids = await client_id(event)
    Kiara_X_Assistant, KIARA_USER, kiara_mention = cids[0], cids[1], cids[2]
    message_id = event.reply_to_msg_id or event.message.id
    thumb = kiara_logo
    input_str = event.pattern_match.group(1)
    omk = f"**• Plugin name ≈** `{input_str}`\n**• Uploaded by ≈** {kiara_mention}\n\n⚡ **[ʟɛɢɛռɖaʀʏ ᴀғ ɥʂɛʀɮօt]({chnl_link})** ⚡"
    the_plugin_file = "./TelethonKiara/plugins/{}.py".format(input_str.lower())
    if os.path.exists(the_plugin_file):
        await event.client.send_file(
            event.chat_id,
            the_plugin_file,
            thumb=thumb,
            caption=omk,
            force_document=True,
            allow_cache=False,
            reply_to=message_id,
        )
        await event.delete()
    else:
        await parse_error(event, f"No plugin named {input_str.lower()}")


@kiara_cmd(pattern="install(?:\s|$)([\s\S]*)")
async def install(event):
    cids = await client_id(event)
    Kiara_X_Assistant, KIARA_USER, kiara_mention = cids[0], cids[1], cids[2]
    b = 1
    owo = event.text[9:]
    kiara = await eor(event, "__Installing.__")
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = (
                await event.client.download_media(  # pylint:disable=E0602
                    await event.get_reply_message(),
                    "./TelethonKiara/plugins/",  # pylint:disable=E0602
                )
            )
            if owo != "-f":
                op = open(downloaded_file_name, "r")
                rd = op.read()
                op.close()
                try:
                    for harm in HARMFUL:
                        if harm in rd:
                            os.remove(downloaded_file_name)
                            return await kiara.edit(
                                f"**⚠️ WARNING !!** \n\n__Replied plugin file contains some harmful codes. Please consider checking the file. If you still want to install then use__ `{hl}install -f`. \n\n**Codes Detected :** \n• {harm}"
                            )
                except BaseException:
                    pass
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                if shortname in CMD_LIST:
                    string = "**Commands found in** `{}`\n".format(
                        (os.path.basename(downloaded_file_name))
                    )
                    for i in CMD_LIST[shortname]:
                        string += "  •  `" + i
                        string += "`\n"
                        if b == 1:
                            a = "__Installing..__"
                            b = 2
                        else:
                            a = "__Installing...__"
                            b = 1
                        await kiara.edit(a)
                    return await kiara.edit(
                        f"✅ **Installed module** :- `{shortname}` \n✨ BY :- {kiara_mention}\n\n{string}\n\n        ⚡ **[ʟɛɢɛռɖaʀʏ ᴀғ ɥʂɛʀɮօt]({chnl_link})** ⚡",
                        link_preview=False,
                    )
                return await kiara.edit(
                    f"Installed module `{os.path.basename(downloaded_file_name)}`"
                )
            else:
                os.remove(downloaded_file_name)
                return await parse_error(kiara, f"Module already installed or unknown format.")
        except Exception as e:
            await parse_error(kiara, e)
            return os.remove(downloaded_file_name)


@kiara_cmd(pattern="uninstall ([\s\S]*)")
async def uninstall(event):
    shortname = event.text[11:]
    if ".py" in shortname:
        shortname = shortname.replace(".py", "")
    kiara = await eor(event, f"__Trying to uninstall plugin__ `{shortname}` ...")
    dir_path = f"./TelethonKiara/plugins/{shortname}.py"
    try:
        remove_plugin(shortname)
        os.remove(dir_path)
        await eod(kiara, f"**Uninstalled plugin** `{shortname}` **successfully.**")
    except OSError as e:
        await parse_error(kiara, f"`{dir_path}` : __{e.strerror}__", False)


@kiara_cmd(pattern="unload ([\s\S]*)")
async def unload(event):
    shortname = event.pattern_match["shortname"]
    try:
        remove_plugin(shortname)
        await eod(event, f"Successfully unloaded `{shortname}`")
    except Exception as e:
        await parse_error(event, e)


@kiara_cmd(pattern="load ([\s\S]*)")
async def load(event):
    shortname = event.pattern_match["shortname"]
    try:
        try:
            remove_plugin(shortname)
        except BaseException:
            pass
        load_module(shortname)
        await eod(event, f"Successfully loaded `{shortname}`")
    except Exception as e:
        await parse_error(event, e)


CmdHelp("core").add_command(
    "install", "<reply to a .py file>", "Installs the replied python file if suitable to Hêllẞø†'s codes.`\n**🚩 Flags :** `-f"
).add_command(
    "uninstall", "<plugin name>", "Uninstalls the given plugin from Hêllẞø†. To get that again do .restart", "uninstall alive"
).add_command(
    "load", "<plugin name>", "Loades the unloaded plugin to your userbot", "load alive"
).add_command(
    "unload", "<plugin name>", "Unloads the plugin from your userbot", "unload alive"
).add_command(
    "send", "<file name>", "Sends the given file from your userbot server, if any.", "send alive"
).add_command(
    "cmds", None, "Gives out the list of modules in KiaraBot."
).add_command(
    "repo", None, "Gives KiaraBot's Github repo link."
).add_command(
    "help", None, "Shows inline help menu."
).add_command(
    "plinfo", "<plugin name>", "Shows the detailed information of given plugin."
).add_command(
    "cmdinfo", "<cmd name>", "Shows the information of given command."
).add_warning(
    "❌ Install External Plugin On Your Own Risk. We won't help if anything goes wrong after installing a plugin."
).add()
