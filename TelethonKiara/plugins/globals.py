import random

from telethon import events
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights, MessageEntityMentionName
from TelethonKiara.DB import gmute_sql as gsql
from TelethonKiara.DB.gban_sql import all_gbanned, gbaner, is_gbanned, ungbaner
from TelethonKiara.DB.gvar_sql import gvarstat
from TelethonKiara.plugins import *


async def get_full_user(event):
    args = event.text.split(" ", 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await parse_error(event, "Need a user to do this.")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await parse_error(event, err)
    return user_obj, extra


@kiara_cmd(pattern="gpro(?:\s|$)([\s\S]*)")
async def _(event):
    Kiara_X_Assistant, _, _ = await client_id(event)
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
        manage_call=True,
    )
    yup = 0
    sed = 0
    kiara = await eor(event, "GPromote in action...")
    if event.is_private:
        user = event.chat
        rank = event.text[6:]
    elif event.is_group:
        user, rank = await get_full_user(event)
    else:
        return await parse_error(kiara, "Can be used in Group and PMs only.")
    if Kiara_X_Assistant == user:
        return await parse_error(kiara, "Cant promote self.")
    if not rank:
        rank = "ǟɖʍɨռ"
    if user:
        total_ch = [
            x.entity.id
            for x in await event.client.get_dialogs()
            if (x.is_group or x.is_channel)
        ]
        for x in total_ch:
            try:
                await event.client(EditAdminRequest(x, user, new_rights, rank))
                yup += 1
            except BadRequestError:
                sed += 1
    else:
        await parse_error(kiara, f"No user defined.")

    text_to_send = f"📍 <b>Promoted:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a> \n📍 <b>Success:</b> <code>{yup}</code> \n📍 <b>Failed:</b> <code>{sed}</code>"
    await kiara.edit(f"<b><i>🔥 GPromote Completed !!</b></i> \n\n{text_to_send}", parse_mode="HTML")
    await event.client.send_message(
        Config.LOGGER_ID,
        f"#GPROMOTE \n\n{text_to_send}",
        parse_mode="HTML",
    )


@kiara_cmd(pattern="gdem(?:\s|$)([\s\S]*)")
async def _(event):
    Kiara_X_Assistant, _, _ = await client_id(event)
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
        manage_call=None,
    )
    yup = 0
    sed = 0
    rank = "ǟɖʍɨռ"
    kiara = await eor(event, "GDemote in action...")
    if event.is_private:
        user = event.chat
    elif event.is_group:
        user, _ = await get_full_user(event)
    else:
        return await parse_error(kiara, "can be used in groups or PMs only!")
    if Kiara_X_Assistant == user:
        return await parse_error(kiara, "Can't demote self.")
    if user:
        total_ch = [
            x.entity.id
            for x in await event.client.get_dialogs()
            if (x.is_group or x.is_channel)
        ]
        for x in total_ch:
            try:
                await event.client(EditAdminRequest(x, user, newrights, rank))
                yup += 1
            except BadRequestError:
                sed += 1
    else:
        await parse_error( Kiara_X_Assistant, f"No user defined.")

    text_to_send = f"📍 <b>Demoted:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a> \n📍 <b>Success:</b> <code>{yup}</code> \n📍 <b>Failed:</b> <code>{sed}</code>"
    await kiara.edit(f"<b><i>🔥 GDemote Completed !!</b></i> \n\n{text_to_send}", parse_mode="HTML")
    await event.client.send_message(
        Config.LOGGER_ID,
        f"#GDEMOTE \n\n{text_to_send}",
        parse_mode="HTML",
    )


@kiara_cmd(pattern="gban(?:\s|$)([\s\S]*)")
async def _(event):
    reason = ""
    Kiara_X_Assistant, _, kiara_mention = await client_id(event)
    kiara = await eor(event, f"`Gban in action...`")
    reply = await event.get_reply_message()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", 1)[1]
        except IndexError:
            reason = ""
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", 2)[1]
        userid = await get_user_id(event, usr)
        try:
            reason = event.text.split(" ", 2)[2]
        except IndexError:
            reason = ""
    elif event.is_private:
        userid = (await event.get_chat()).id
        try:
            reason = event.text.split(" ", 1)[1]
        except IndexError:
            reason = ""
    else:
        return await parse_error(kiara, "No user mentioned.")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == Kiara_X_Assistant:
        return await eod(kiara, "🥴 **It's simply not possible.**")
    if str(userid) in DEVLIST:
        return await eod(kiara, "😑 **It's simply not possible.**")
    if is_gbanned(userid):
        return await eod(kiara, "This user is already gbanned and added to my **Gban Watch!!**")
    
    async for gfuck in event.client.iter_dialogs():
        if gfuck.is_group or gfuck.is_channel:
            try:
                await event.client.edit_permissions(
                    gfuck.id, userid, view_messages=False
                )
                chats += 1
            except BaseException:
                pass

    gbaner(userid)
    a = gvarstat("BAN_PIC")
    if a and a == "DISABLE":
        gbpic = None
    elif a:
        b = a.split(" ")
        pic_str = []
        for c in b:
            pic_str.append(c)
        gbpic = random.choice(pic_str)
    else:
        gbpic = cjb
    
    gmsg = f"🥴 [{name}](tg://user?id={userid}) **beta majdur ko khodna 😪 aur** {kiara_mention} **ko chodna... Kabhi sikhana nhi!! 😏**\n\n📍 Added to Gban Watch!!\n**🔰 Total Chats :**  `{chats}`"
    if reason != "":
        gmsg += f"\n**🔰 Reason :**  `{reason}`"
    
    ogmsg = f"**📍 Victim:** [{name}](tg://user?id={userid}) \n**📍 Chats:** `{chats}` \n**📍 Gban By:** {kiara_mention}\n\n**📍 User Added to Gban Watch!!**"
    if reason != "":
        ogmsg += f"\n**📍 Reason:** `{reason}`"
    
    if Config.ABUSE == "ON":
        await event.client.send_message(event.chat_id, gmsg, file=gbpic, reply_to=reply)
    else:
        await event.client.send_message(event.chat_id, f"__**🔥 GBan Completed !!**__ \n\n{ogmsg}", file=gbpic, reply_to=reply)
    await kiara.delete()
    await event.client.send_message(
        Config.LOGGER_ID,
        f"#GBAN \n\n{ogmsg}",
    )


@kiara_cmd(pattern="ungban(?:\s|$)([\s\S]*)")
async def _(event):
    _, _, kiara_mention = await client_id(event)
    kiara = await eor(event, "`Ungban in action...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event, event.pattern_match.group(1))
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await parse_error(kiara, "No user mentioned.")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if not is_gbanned(userid):
        return await eod(kiara, "`User is not gbanned.`")
    
    async for gfuck in event.client.iter_dialogs():
        if gfuck.is_group or gfuck.is_channel:
            try:
                await event.client.edit_permissions(
                    gfuck.id, userid, view_messages=True
                )
                chats += 1
            except BaseException:
                pass

    ungbaner(userid)
    ogmsg = f"**📍 Victim:** [{name}](tg://user?id={userid}) \n**📍 Chats:** `{chats}` \n**📍 UnGban By:** {kiara_mention}\n\n**📍 User removed from Gban Watch!!**"
    await kiara.edit(f"__**🔥 UnGban Completed !!**__ \n\n{ogmsg}")
    await event.client.send_message(
        Config.LOGGER_ID,
        f"#UNGBAN \n\n{ogmsg}",
    )


@kiara_cmd(pattern="listgban$")
async def already(event):
    kiara = await eor(event, "`Fetching Gbanned users...`")
    gbanned_users = all_gbanned()
    GBANNED_LIST = "**Gbanned Users:**\n"
    if len(gbanned_users) > 0:
        for user in gbanned_users:
            usr = user.chat_id
            userid = await get_user_id(event, int(usr))
            try:
                name = (await event.client.get_entity(userid)).first_name
            except ValueError:
                name = "User"
            GBANNED_LIST += f"📍 [{name}](tg://user?id={userid}) (`{userid}`)\n"
    else:
        GBANNED_LIST = "No Gbanned Users!!"
    await kiara.edit(GBANNED_LIST)


@bot.on(events.ChatAction)
async def _(event):
    if event.user_joined or event.added_by:
        user = await event.get_user()
        chat = await event.get_chat()
        gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim:**  [{user.first_name}](tg://user?id={user.id})\n"
        if is_gbanned(str(user.id)):
            if chat.admin_rights:
                try:
                    await bot.edit_permissions(
                        chat.id,
                        user.id,
                        view_messages=False,
                    )
                    gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                except BaseException:
                    pass
            else:
                gban_watcher += f"Reported to @admins"
            await event.reply(gban_watcher)


if H2:
    @H2.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim:**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H2.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
                await event.reply(gban_watcher)


if H3:
    @H3.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim:**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H3.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
                await event.reply(gban_watcher)


if H4:
    @H4.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim:**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H4.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
                await event.reply(gban_watcher)


if H5:
    @H5.on(events.ChatAction)
    async def _(event):
        if event.user_joined or event.added_by:
            user = await event.get_user()
            chat = await event.get_chat()
            gban_watcher = f"⚠️⚠️**Warning**⚠️⚠️\n\n`Gbanned User Joined the chat!!`\n**⚜️ Victim:**  [{user.first_name}](tg://user?id={user.id})\n"
            if is_gbanned(str(user.id)):
                if chat.admin_rights:
                    try:
                        await H5.edit_permissions(
                            chat.id,
                            user.id,
                            view_messages=False,
                        )
                        gban_watcher += f"**🔥 Action 🔥**  \n`Banned this piece of shit....` **AGAIN!**"
                    except BaseException:
                        pass
                else:
                    gban_watcher += f"Reported to @admins"
                await event.reply(gban_watcher)


@kiara_cmd(pattern="gkick(?:\s|$)([\s\S]*)")
async def gkick(event):
    reason = ""
    Kiara_X_Assistant, _, kiara_mention = await client_id(event)
    kiara = await eor(event, "`GKick in action...`")
    reply = await event.get_reply_message()
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
        try:
            reason = event.text.split(" ", 1)[1]
        except IndexError:
            reason = "Not Mentioned!"
    elif event.pattern_match.group(1):
        usr = event.text.split(" ", 2)[1]
        userid = await get_user_id(event, usr)
        try:
            reason = event.text.split(" ", 2)[2]
        except IndexError:
            reason = "Not Mentioned!"
    elif event.is_private:
        userid = (await event.get_chat()).id
        try:
            reason = event.text.split(" ", 1)[1]
        except IndexError:
            reason = "Not Mentioned!"
    else:
        return await parse_error(kiara, "No user mentioned.")
    name = (await event.client.get_entity(userid)).first_name
    chats = 0
    if userid == Kiara_X_Assistant:
        return await eod(kiara, "**🥴 It's simply not possible.**")
    if str(userid) in DEVLIST:
        return await eod(kiara, "**😪 It's simply not possible.**")
    
    async for gkick in event.client.iter_dialogs():
        if gkick.is_group or gkick.is_channel:
            try:
                await event.client.kick_participant(gkick.id, userid)
                chats += 1
            except BaseException:
                pass

    a = gvarstat("BAN_PIC")
    if a and a == "DISABLE":
        gbpic = None
    elif a:
        b = a.split(" ")
        pic_str = []
        for c in b:
            pic_str.append(c)
        gbpic = random.choice(pic_str)
    else:
        gbpic = cjb
    
    gkmsg = f"**📍 Victim:** [{name}](tg://user?id={userid}) \n**📍 Chats:** `{chats}` \n**Reason:** `{reason}`\n**📍 GKick By:** {kiara_mention}"
    await event.client.send_message(event.chat_id, f"__**🔥 GKick Completed !!**__ \n\n{gkmsg}", file=gbpic, reply_to=reply)
    await kiara.delete()
    await event.client.send_message(
        Config.LOGGER_ID,
        f"#GKICK \n\n{gkmsg}",
    )


@kiara_cmd(pattern="gmute(?:\s|$)([\s\S]*)")
async def gm(event):
    Kiara_X_Assistant, _, kiara_mention = await client_id(event)
    kiara = await eor(event, "`GMute in action...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event, event.text.split(" ", 2)[1])
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await parse_error(kiaral, "No user mentioned.")
    name = (await event.client.get_entity(userid)).first_name
    reply = await event.get_reply_message()
    if userid == Kiara_X_Assistant:
        return await eod(kiara, "**🥴 It's simply not possible.**")
    if str(userid) in DEVLIST:
        return await eod(kiara, "**😪 It's simply not possible.**")
    if gsql.is_gmuted(userid, "gmute"):
        return await eod(kiara, "This user is already Gmuted.")
    
    ogmsg = f"**📍 Victim:** [{name}](tg://user?id={userid}) \n**📍 GMute By:** {kiara_mention}"
    try:
        gsql.gmute(userid, "gmute")
        if Config.ABUSE == "ON":
            await event.client.send_message(event.chat_id, f"Chup [Madarchod](tg://user?id={userid})", file=shhh, reply_to=reply)
            await kiara.delete()
        else:
            await kiara.edit(f"__**🔥 GMute Completed !!**__ \n\n{ogmsg}")
        await event.client.send_message(
            Config.LOGGER_ID,
            f"#GMUTE \n\n{ogmsg}",
        )
    except Exception as e:
        await parse_error(kiara, e)


@kiara_cmd(pattern="ungmute(?:\s|$)([\s\S]*)")
async def endgmute(event):
    _, _, kiara_mention = await client_id(event)
    kiara = await eor(event, "`UnGmute in action...`")
    if event.reply_to_msg_id:
        userid = (await event.get_reply_message()).sender_id
    elif event.pattern_match.group(1):
        userid = await get_user_id(event, event.text.split(" ", 2)[1])
    elif event.is_private:
        userid = (await event.get_chat()).id
    else:
        return await parse_error(kiara, "No user mentioned.")
    name = (await event.client.get_entity(userid)).first_name
    if not gsql.is_gmuted(userid, "gmute"):
        return await eod(kiara, "User not found in Gmute DB.")
    try:
        gsql.ungmute(userid, "gmute")
        ogmsg = f"**📍 Victim:** [{name}](tg://user?id={userid}) \n**📍 UnGmute By:** {kiara_mention}"
        await kiara.edit(f"__**🔥 UnGmute Completed !!**__ \n\n{ogmsg}")
        await event.client.send_message(
            Config.LOGGER_ID,
            f"#UNGMUTE \n\n{ogmsg}",
        )
    except Exception as e:
        await parse_error(kiara, e)


@kiara_handler(incoming=True)
async def watcher(event):
    if gsql.is_gmuted(event.sender_id, "gmute"):
        await event.delete()


CmdHelp("globals").add_command(
    "gban", "<reply>/<userid>", "Globally Bans the mentioned user in 'X' chats you are admin with ban permission."
).add_command(
    "ungban", "<reply>/<userid>", "Globally Unbans the user in 'X' chats you are admin!"
).add_command(
    "listgban", None, "Gives the list of all GBanned Users."
).add_command(
    "gkick", "<reply>/<userid>", "Globally Kicks the user in 'X' chats you are admin!"
).add_command(
    "gmute", "<reply> or <userid>", "Globally Mutes the User."
).add_command(
    "ungmute", "<reply> or <userid>", "Globally Unmutes the gmutes user."
).add_command(
    "gpro", "<reply> or <username>", "Globally Promotes the mentioned user in all the chats you are admin with Add Admins permission."
).add_command(
    "gdem", "<reply> or <username>", "Globally Demotes the mentioned user in all the chats you have rights to demoted that user."
).add_info(
    "Global Admin Tool."
).add_warning(
    "✅ Harmlesss Module."
).add()
