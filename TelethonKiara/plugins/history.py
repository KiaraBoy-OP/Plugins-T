from telethon.errors.rpcerrorlist import YouBlockedUserError
from TelethonKiara.plugins import *


@kiara_cmd(pattern="history(?:\s|$)([\s\S]*)")
async def _(kiaraevent):
    if not kiaraevent.reply_to_msg_id:
        await parse_error(kiaraevent, "No user mentioned!")
        return
    in_chat = kiaraevent.chat_id
    reply_message = await kiaraevent.get_reply_message()
    chat = "SangMata_BOT"
    victim = reply_message.sender.id
    if reply_message.sender.bot:
        await eod(kiaraevent, "Need actual users. Not Bots")
        return
    kiara = await eor(kiaraevent, "Checking...")
    success = False
    async with kiaraevent.client.conversation(chat) as conv:
        try:
            first = await conv.send_message(f"{victim}")
            try:
                await kiara.delete()
                response1 = await conv.get_response()
                if response1 and response1.text.startswith("🔗"):
                    success = False
                else:
                    await kiaraevent.client.send_message(in_chat, response1.text, reply_to=reply_message)
                    success = True
                await kiaraevent.client.delete_messages(conv.chat_id, [response1.id])

                response2 = await conv.get_response()
                if response2 and response2.text.startswith("🔗"):
                    success = False
                else:
                    await kiaraevent.client.send_message(in_chat, response2.text, reply_to=reply_message)
                    success = True
                await kiaraevent.client.delete_messages(conv.chat_id, [response2.id])

                response3 = await conv.get_response()
                if response3 and response3.text.startswith("🔗"):
                    success = False
                else:
                    await kiaraevent.client.send_message(in_chat, response3.text, reply_to=reply_message)
                    success = True
                await kiaraevent.client.delete_messages(conv.chat_id, [response3.id])
            except TimeoutError:
                pass
            if success == False:
                kiara = await kiaraevent.client.send_message(in_chat, "**ERROR**", reply_to=reply_message)
                await parse_error(kiara, "Unexpected Error Occured !!")
            await kiaraevent.client.delete_messages(conv.chat_id, [first.id])
        except YouBlockedUserError:
            return await parse_error(kiara, "__Unblock @SangMata_BOT and try again.__", False)


# @kiara_cmd(pattern="unh(?:\s|$)([\s\S]*)")
# async def _(kiaraevent):
#     if not kiaraevent.reply_to_msg_id:
#         await parse_error(kiaraevent, "No user mentioned.")
#         return
#     reply_message = await kiaraevent.get_reply_message()
#     chat = "SangMata_BOT"
#     victim = reply_message.sender.id
#     if reply_message.sender.bot:
#         await eod(kiaraevent, "Need actual users. Not Bots")
#         return
#     kiara = await eor(kiaraevent, "Checking...")
#     async with kiaraevent.client.conversation(chat) as conv:
#         try:
#             first = await conv.send_message(f"/search_id {victim}")
#             try:
#                 # async with timeout(20):
#                     response1 = await conv.get_response()
#                     if response1 and response1.text.startswith("Username"):
#                         await kiara.edit(response1.text)
#                         success = True
#                     await kiaraevent.client.delete_messages(conv.chat_id, [response1.id])
#                     response2 = await conv.get_response()
#                     if response2 and response2.text.startswith("Username"):
#                         await kiara.edit(response2.text)
#                         success = True
#                     await kiaraevent.client.delete_messages(conv.chat_id, [response2.id])
#                     response3 = await conv.get_response()
#                     if response3 and response3.text.startswith("Username"):
#                         await kiara.edit(response3.text)
#                         success = True
#                     await kiaraevent.client.delete_messages(conv.chat_id, [response3.id])
#             except TimeoutError:
#                 pass
#             if success == False:
#                 await parse_error(kiara, "Unexpected Error Occured !!")
#             await kiaraevent.client.delete_messages(conv.chat_id, [first.id])
#         except YouBlockedUserError:
#             return await parse_error(kiara, "__Unblock @SangMata_BOT and try again.__", False)


CmdHelp("history").add_command(
    "history", "<reply to a user>", "Fetches the name history of replied user."
# ).add_command(
#     "unh", "<reply to user>", "Fetches the Username History of replied users."
).add_info(
    "Telegram Name History"
).add_warning(
    "✅ Harmless Module."
).add()
