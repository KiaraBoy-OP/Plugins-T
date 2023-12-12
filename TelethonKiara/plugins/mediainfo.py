import asyncio
import os
import time

from TelethonKiara.plugins import *


@kiara_cmd(pattern="mediainfo$")
async def mediainfo(event):
    KIARA_MEDIA = None
    reply = await event.get_reply_message()
    logo = "https://te.legra.ph/file/25ceab16205256486aec5.jpg"
    if not reply:
        return await parse_error(event, "No replied media file found.")
    if not reply.media:
        return await parse_error(event, "No replied media file found.")
    kiara = await eor(event, "`Fetching media info...`")
    KIARA_MEDIA = reply.file.mime_type
    if not KIARA_MEDIA:
        return await parse_error(kiara, "Need media files to fetch mediainfo.")
    elif KIARA_MEDIA.startswith(("text")):
        return await parse_error(kiara, "Need media files to fetch mediainfo.")
    hel_ = await mediadata(reply)
    c_time = time.time()
    file_path = await event.client.download_media(
        reply,
        Config.TMP_DOWNLOAD_DIRECTORY,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(
                d,
                t,
                kiara,
                c_time,
                "Downloading ...",
            )
        ),
    )
    out, _, _, _ = await runcmd(f"mediainfo '{file_path}'")
    if not out:
        out = "Unknown Format !!"
    paster = f"""
<h2>📃 MEDIA INFO 📃</h2>
<code>
{hel_}
</code>
<h2>🧐 MORE DETAILS 🧐</h2>
<code>
{out} 
</code>
<img src='{logo}'/>"""
    paste = await telegraph_paste(f"{KIARA_MEDIA}", paster)
    await kiara.edit(
        f"📌 Fetched  Media Info Successfully !! \n\n**Check Here:** [{KIARA_MEDIA}]({paste})"
    )
    os.remove(file_path)


CmdHelp("mediainfo").add_command(
    "mediainfo", "<reply to a media>", "Fetches the detailed information of replied media."
).add_info(
    "Everything About That Media."
).add_warning(
    "✅ Harmless Module."
).add()
