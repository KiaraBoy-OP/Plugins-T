import asyncio
import os

import cv2
from PIL import Image
from TelethonKiara.plugins import *


@kiara_cmd(pattern="mms(?:\s|$)([\s\S]*)")
async def _(event):
    _reply = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (_reply and (_reply.media)):
        await eod(event, "`Can't memify this 🥴`")
        return
    hel_ = await eor(event, "__Memifying ...__")
    kiara = await _reply.download_media()
    if kiara and kiaral.endswith((".tgs")):
        await hel_.edit("OwO animated sticker...")
        cmd = ["lottie_convert.py", kiara, "pic.png"]
        file = "pic.png"
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif kiara and kiara.endswith((".webp", ".png")):
        pics = Image.open(kiara)
        pics.save("pic.png", format="PNG", optimize=True)
        file = "pic.png"
    elif kiara:
        img = cv2.VideoCapture(kiara)
        tal, semx = img.read()
        cv2.imwrite("pic.png", semx)
        file = "pic.png"
    else:
        return await eod(hel_, "Unable to memify this!")
    output = await draw_meme_text(file, msg)
    await event.client.send_file(
        event.chat_id, output, force_document=False, reply_to=event.reply_to_msg_id
    )
    await hel_.delete()
    try:
        os.remove(kiara)
        os.remove(file)
        os.remove(output)
    except BaseException:
        pass


@kiara_cmd(pattern="mmf(?:\s|$)([\s\S]*)")
async def _(event):
    _reply = await event.get_reply_message()
    msg = event.pattern_match.group(1)
    if not (_reply and (_reply.media)):
        await eod(event, "`Can't memify this 🥴`")
        return
    hel_ = await eor(event, "__Memifying ...__")
    kiara = await _reply.download_media()
    if kiara and kiara.endswith((".tgs")):
        await hel_.edit("OwO animated sticker...")
        cmd = ["lottie_convert.py", kiara, "pic.png"]
        file = "pic.png"
        process = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
    elif kiara and kiara.endswith((".webp", ".png")):
        pic = Image.open(kiara)
        pic.save("pic.png", format="PNG", optimize=True)
        file = "pic.png"
    elif kiara:
        img = cv2.VideoCapture(kiara)
        tal, semx = img.read()
        cv2.imwrite("pic.png", semx)
        file = "pic.png"
    else:
        return await eod(hel_, "Unable to memify this!")
    output = await draw_meme(file, msg)
    await event.client.send_file(
        event.chat_id, output, force_document=False, reply_to=event.reply_to_msg_id
    )
    await hel_.delete()
    try:
        os.remove(kiara)
        os.remove(file)
    except BaseException:
        pass
    os.remove(pic)


CmdHelp("memify").add_command(
    "mms", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in sticker format.", "mms <reply to a img/stcr/gif> hii ; hello"
).add_command(
    "mmf", "<reply to a img/stcr/gif> <upper text> ; <lower text>", "Memifies the replied image/gif/sticker with your text and sends output in image format.", "mmf <reply to a img/stcr/gif> hii ; hello"
).add_info(
    "Memify images and stickers."
).add_warning(
    "✅ Harmless Module."
).add()
