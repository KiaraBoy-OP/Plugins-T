from TelethonKiara.clients.logger import LOGGER as LOGS
from TelethonKiara.helpers.formats import yaml_format
from TelethonKiara.helpers.progress import humanbytes


async def mediadata(e_media):
    kiara = ""
    if e_media.file.name:
        kiara += f"📍 NAME :  {e_media.file.name}<br>"
    if e_media.file.mime_type:
        kiara += f"📍 MIME TYPE :  {e_media.file.mime_type}<br>"
    if e_media.file.size:
        kiara += f"📍 SIZE :  {humanbytes(e_media.file.size)}<br>"
    if e_media.date:
        kiara += f"📍 DATE :  {yaml_format(e_media.date)}<br>"
    if e_media.file.id:
        kiara += f"📍 ID :  {e_media.file.id}<br>"
    if e_media.file.ext:
        kiara += f"📍 EXTENSION :  '{e_media.file.ext}'<br>"
    if e_media.file.emoji:
        kiara += f"📍 EMOJI :  {e_media.file.emoji}<br>"
    if e_media.file.title:
        kiara += f"📍 TITLE :  {e_media.file.title}<br>"
    if e_media.file.performer:
        kiara += f"📍 PERFORMER :  {e_media.file.performer}<br>"
    if e_media.file.duration:
        kiara += f"📍 DURATION :  {e_media.file.duration} seconds<br>"
    if e_media.file.height:
        kiara += f"📍 HEIGHT :  {e_media.file.height}<br>"
    if e_media.file.width:
        kiara += f"📍 WIDTH :  {e_media.file.width}<br>"
    if e_media.file.sticker_set:
        kiara += f"📍 STICKER SET :\
            \n {yaml_format(e_media.file.sticker_set)}<br>"
    try:
        if e_media.media.document.thumbs:
            kiara += f"📍 Thumb  :\
                \n {yaml_format(e_media.media.document.thumbs[-1])}<br>"
    except Exception as e:
        LOGS.info(str(e))
    return kiara


def media_type(message):
    if message and message.photo:
        return "Photo"
    if message and message.audio:
        return "Audio"
    if message and message.voice:
        return "Voice"
    if message and message.video_note:
        return "Round Video"
    if message and message.gif:
        return "Gif"
    if message and message.sticker:
        return "Sticker"
    if message and message.video:
        return "Video"
    if message and message.document:
        return "Document"
    return None
