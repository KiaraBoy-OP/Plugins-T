import inspect
import re
from pathlib import Path

from KiaraConfig import Config
from telethon import events
from TelethonKiara.clients.session import H2, H3, H4, H5, Kiara
from TelethonKiara.utils.globals import CMD_LIST, LOAD_PLUG


def kiara_cmd(
    pattern: str = None,
    allow_sudo: bool = True,
    disable_edited: bool = False,
    forword=False,
    command: str = None,
    **args,
):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")

    if "disable_edited" in args:
        del args["disable_edited"]

    args["blacklist_chats"] = True
    black_list_chats = list(Config.BL_CHAT)
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats

    sudo_user = Config.SUDO_USERS

    if pattern is not None:
        global kiara_reg
        global sudo_reg
        if (
            pattern.startswith(r"\#")
            or not pattern.startswith(r"\#")
            and pattern.startswith(r"^")
        ):
            kiara_reg = sudo_reg = re.compile(pattern)
        else:
            kiara_ = "\\" + Config.HANDLER
            sudo_ = "\\" + Config.SUDO_HANDLER
            kiara_reg = re.compile(kiara_ + pattern)
            sudo_reg = re.compile(sudo_ + pattern)
            if command is not None:
                cmd1 = kiara_ + command
                cmd2 = sudo_ + command
            else:
                cmd1 = (
                    (kiara_ + pattern)
                    .replace("$", "")
                    .replace("\\", "")
                    .replace("^", "")
                )
                cmd2 = (
                    (sudo_ + pattern)
                    .replace("$", "")
                    .replace("\\", "")
                    .replace("^", "")
                )
            try:
                CMD_LIST[file_test].append(cmd1)
            except BaseException:
                CMD_LIST.update({file_test: [cmd1]})

    def decorator(func):
        if not disable_edited:
            Kiara.add_event_handler(
                func, events.MessageEdited(**args, outgoing=True, pattern=kiara_reg)
            )
        Kiara.add_event_handler(
            func, events.NewMessage(**args, outgoing=True, pattern=kiara_reg)
        )
        if allow_sudo:
            if not disable_edited:
                Kiara.add_event_handler(
                    func,
                    events.MessageEdited(
                        **args, from_users=sudo_user, pattern=sudo_reg
                    ),
                )
            Kiara.add_event_handler(
                func, events.NewMessage(**args, from_users=sudo_user, pattern=sudo_reg)
            )
        if H2:
            if not disable_edited:
                H2.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=kiara_reg)
                )
            H2.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=kiara_reg)
            )
        if H3:
            if not disable_edited:
                H3.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=kiara_reg)
                )
            H3.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=kiara_reg)
            )
        if H4:
            if not disable_edited:
                H4.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=kiara_reg)
                )
            H4.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=kiara_reg)
            )
        if H5:
            if not disable_edited:
                H5.add_event_handler(
                    func, events.MessageEdited(**args, outgoing=True, pattern=kiara_reg)
                )
            H5.add_event_handler(
                func, events.NewMessage(**args, outgoing=True, pattern=kiara_reg)
            )
        try:
            LOAD_PLUG[file_test].append(func)
        except Exception:
            LOAD_PLUG.update({file_test: [func]})
        return func

    return decorator


def kiara_handler(**args):
#     args["func"] = lambda e: e.via_bot_id is None
    def decorator(func):
        Kiara.add_event_handler(func, events.NewMessage(**args))
        if H2:
            H2.add_event_handler(func, events.NewMessage(**args))
        if H3:
            H3.add_event_handler(func, events.NewMessage(**args))
        if H4:
            H4.add_event_handler(func, events.NewMessage(**args))
        if H5:
            H5.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator
