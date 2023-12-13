import datetime
import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from TelethonKiara.plugins import *


@kiara_cmd(pattern="logo([\s\S]*)")
async def logo(event):
    try:
        kiara = await eor(event, "`Processing.....`")
        _, _, kiara_mention = await client_id(event)
        text = event.text
        lists = text.split(" ", 1)
        if len(lists) == 1:
            return await parse_error(kiara, "Give some text to make Logo")

        if (text[5:]).startswith("-"):
            _type = (lists[0])[6:]
        else:
            _type = random.choice(rand_bg)
        _fnt = random.choice(rand_font)
        query = lists[1]
        start = datetime.datetime.now()
        reply = await event.get_reply_message()
        if reply and reply.media and reply.media.photo:
            await reply.download_media("temp_bg.jpg")
            await kiara.edit("__Downloaded replied photo... starting to make logo__")
        else:
            _unsp = await unsplash(_type, 1)
            _bg = requests.get(_unsp[0])
            with open("temp_bg.jpg", "wb") as file:
                file.write(_bg.content)
            await kiara.edit(f"__Downloaded__ `{_type}` __background... starting to make logo__")
        img = Image.open("temp_bg.jpg")
        img.resize((5000, 5000)).save("logo_bg.jpg")
        os.remove("temp_bg.jpg")
        img = Image.open("logo_bg.jpg")
        wid, hig = img.size
        draw = ImageDraw.Draw(img)
        font_ = requests.get(_fnt)
        _font = "logo_font.ttf"
        with open(_font, "wb") as file:
            file.write(font_.content)
        font_size = await get_font_size(_font, query, img)
        font = ImageFont.truetype(_font, font_size)
        w, h = draw.textsize(query, font=font)
        draw.text(
            ((wid - w) / 2, (hig - h) / 2),
            query,
            font=font,
            fill="white",
            stroke_width=8,
            stroke_fill="black",
        )
        img.save("logo.png", "PNG")
        end = datetime.datetime.now()
        ms = (end - start).seconds
        await event.client.send_file(
            event.chat_id,
            "logo.png",
            caption=f"**Made by:** {kiara_mention} \n**Time taken:** `{ms} seconds`",
            reply_to=reply,
        )
        await kiara.delete()
        os.remove(_font)
        os.remove("logo.png")
        os.remove("logo_bg.jpg")

    except Exception as e:
        print(f"An error occurred: {e}")
        await kiara.edit("An error occurred while processing the request.")

CmdHelp("logos").add_command(
    "logo", "-{type} {logo text}", "Makes a logo with the given text. If replied to a picture makes logo on that else gets random BG.", f"logo Kiarabot \n{hl}logo-car KiaraBot \n{hl}logo-anime KiaraBot \netc..."
).add_info(
    "Logo Maker."
).add_warning(
    "✅ Harmless Module."
).add()
