from KiaraConfig import Config, db_config, os_config
from TelethonKiara import HEROKU_APP, StartTime
from TelethonKiara.clients.client_list import (client_id, clients_list,
                                              get_user_id)
from TelethonKiara.clients.decs import kiara_cmd, kiara_handler
from TelethonKiara.clients.instaAPI import InstaGram
from TelethonKiara.clients.logger import LOGGER
from TelethonKiara.clients.session import (H2, H3, H4, H5, Kiara, KiaraBot,
                                          validate_session)
from TelethonKiara.DB import gvar_sql
from TelethonKiara.helpers.anime import *
from TelethonKiara.helpers.classes import *
from TelethonKiara.helpers.convert import *
from TelethonKiara.helpers.exceptions import *
from TelethonKiara.helpers.formats import *
from TelethonKiara.helpers.gdriver import *
from TelethonKiara.helpers.google import *
from TelethonKiara.helpers.ig_helper import *
from TelethonKiara.helpers.image import *
from TelethonKiara.helpers.int_str import *
from TelethonKiara.helpers.mediatype import *
from TelethonKiara.helpers.mmf import *
from TelethonKiara.helpers.movies import *
from TelethonKiara.helpers.pasters import *
from TelethonKiara.helpers.pranks import *
from TelethonKiara.helpers.progress import *
from TelethonKiara.helpers.runner import *
from TelethonKiara.helpers.tools import *
from TelethonKiara.helpers.tweets import *
from TelethonKiara.helpers.users import *
from TelethonKiara.helpers.vids import *
from TelethonKiara.helpers.yt_helper import *
from TelethonKiara.strings import *
from TelethonKiara.utils.cmds import *
from TelethonKiara.utils.decorators import *
from TelethonKiara.utils.errors import *
from TelethonKiara.utils.extras import *
from TelethonKiara.utils.funcs import *
from TelethonKiara.utils.globals import *
from TelethonKiara.utils.plug import *
from TelethonKiara.utils.startup import *
from TelethonKiara.version import __kiaraver__, __telever__

cjb = "./KiaraConfig/resources/pics/cjb.jpg"
kiara_logo = "./KiaraConfig/resources/pics/kiarabot_logo.jpg"
restlo = "./KiaraConfig/resources/pics/rest.jpeg"
shhh = "./KiaraConfig/resources/pics/chup_madarchod.jpeg"
shuru = "./KiaraConfig/resources/pics/shuru.jpg"
spotify_logo = "./KiaraConfig/resources/pics/spotify.jpg"


kiara_emoji = Config.EMOJI_IN_HELP
hl = Config.HANDLER
shl = Config.SUDO_HANDLER
kiarabot_version = __kiaraver__
telethon_version = __telever__
abuse_m = "Enabled" if str(Config.ABUSE).lower() in enabled_list else "Disabled"
is_sudo = "True" if gvar_sql.gvarstat("SUDO_USERS") else "False"

my_channel = Config.MY_CHANNEL or "Its_KiaraBot"
my_group = Config.MY_GROUP or "KiaraBot_Chat"
if "@" in my_channel:
    my_channel = my_channel.replace("@", "")
if "@" in my_group:
    my_group = my_group.replace("@", "")

chnl_link = "https://t.me/its_kiarabot"
grp_link = "https://t.me/KiaraBot_Chat"
kiara_channel = f"[†hê Ừʂɛɤẞø†]({chnl_link})"
kiara_grp = f"[Ừʂɛɤẞø† Group]({grp_link})"

WELCOME_FORMAT = """**Use these fomats in your welcome note to make them attractive.**
  {count} : To get group members
  {first} : To use user first name
  {fullname} : To use user full name
  {last} : To use user last name
  {mention} :  To mention the user
  {my_first} : To use my first name
  {my_fullname} : To use my full name
  {my_last} : To use my last name
  {my_mention} : To mention myself
  {my_username} : To use my username
  {title} : To get chat name in message
  {userid} : To use userid
  {username} : To use user username
"""

# TelethonKiara
