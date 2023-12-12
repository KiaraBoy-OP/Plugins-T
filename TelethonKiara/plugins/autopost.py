from TelethonKiara.DB.autopost_sql import (add_post, get_all_post, is_post,
                                          remove_post)
from TelethonKiara.DB.gvar_sql import addgvar, delgvar, gvarstat
from TelethonKiara.plugins import *


@kiara_cmd(pattern="autopost(?:\s|$)([\s\S]*)")
async def _(event):
    if event.is_private:
        return await parse_error(event, "AutoPost Can Only Be Used For Channels & Groups.")
    kiara = await eor(event, "Trying to start autoposting from here...")
    cid = await client_id(event)
    Kiara_X_Assistant = cid[0]
    hel_ = event.text[10:]
    cli_ = Kiara_X_Assistant
    checker = gvarstat(f"AUTOPOST_{str(cli_)}")
    if hel_ == "":
        return await eod(
            kiara,
            f"Give correct command for working of autopost. \n`{hl}autopost channel_id`",
        )
    if str(hel_).startswith("-100"):
        kk = str(hel_).replace("-100", "")
    else:
        kk = hel_
    if not kk.isdigit():
        return await parse_error(kiara, "Only channel ID is supported.")
    if is_post(kk, event.chat_id):
        if checker and checker == "True":
            return await eod(kiara, "This channel is already in this client's autopost database.")
        else:
            addgvar(f"AUTOPOST_{str(cli_)}", "True")
            return await kiara.edit(
                f"**📍 Started AutoPosting from** `{hel_}` for `{cli_}`"
            )
    add_post(kk, event.chat_id)
    addgvar(f"AUTOPOST_{str(cli_)}", "True")
    await kiara.edit(f"**📍 Started AutoPosting from** `{hel_}` for `{cli_}`")


@kiara_cmd(pattern="rmautopost(?:\s|$)([\s\S]*)")
async def _(event):
    if event.is_private:
        return await parse_error(event, "AutoPost Can Only Be Used For Channels.")
    kiara = await eor(event, "Removing autopost...")
    cid = await client_id(event)
    Kiara_X_Assistant = cid[0]
    hel_ = event.text[12:]
    cli_ = Kiara_X_Assistant
    checker = gvarstat(f"AUTOPOST_{str(cli_)}")
    if hel_ == "":
        return await eod(
            kiara,
            f"Give correct command for removing autopost. \n`{hl}autopost channel_id`",
        )
    if str(hel_).startswith("-100"):
        kk = str(hel_).replace("-100", "")
    else:
        kk = hel_
    if not kk.isdigit():
        return await parse_error(event, "Only channel ID is supported.")
    if not is_post(kk, event.chat_id):
        return await eod(event, "I don't think this channel is in AutoPost Database.")
    if is_post(kk, event.chat_id):
        if checker and checker == "True":
            remove_post(kk, event.chat_id)
            delgvar(f"AUTOPOST_{str(cli_)}")
            return await eod(kiara, f"Removed `{hel_}` from `{cli_}` autopost database.")
        else:
            return await eod(
                kiara, f"This channel is not in `{cli_}` autopost database."
            )


@kiara_handler(incoming=True)
async def _(event):
    chat_id = str(event.chat_id).replace("-100", "")
    channels_set = get_all_post(chat_id)
    if channels_set == []:
        return
    cid = await client_id(event)
    Kiara_X_Assistant = cid[0]
    cli_ = Kiara_X_Assistant
    checker = gvarstat(f"AUTOPOST_{str(cli_)}")
    if checker and checker == "True":
        for chat in channels_set:
            if event.media:
                await event.client.send_file(int(chat), event.media, caption=event.text)
            elif not event.media:
                await event.client.send_message(int(chat), event.message)


CmdHelp("autopost").add_command(
    "autopost", "<channel id>", "Auto Posts every new post from targeted channel to your channel.", "autopost <channelid> [in your channel]"
).add_command(
    "rmautopost", "<channel id>", "Stops AutoPost from targeted autoposting channel."
).add_info(
    "AutoPost From One Channel To Another."
).add_warning(
    "✅ Harmless Module."
).add()
