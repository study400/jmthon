from . import *

import contextlib
import os
import sys
import time
from .core.helper import time_formatter#, bash
from .load_plug import load
from telethon.errors import SessionRevokedError
from .utils import (
    group_ub,
    tag_chat,
    inline_on,
    join_dev,
    notify,
    tag_chat, 
    group_ub
)


jmubot.me.phone = None

if not jmubot.me.bot:
    jmdB.set_key("OWNER_ID", jmubot.me.id)
    jmdB.set_key("NAME", jmubot.full_name)

LOGS.info("جار تثبيت سورس جمثون ...")


try:
    LOGS.info("يتم تفعيل وضع الانلاين")
    jmubot.loop.run_until_complete(inline_on())
    LOGS.info("تم تفعيل وضع الانلاين بنجاح ✓")
except Exception as meo:
    LOGS.error(f"- {meo}")
    sys.exit()

jmubot.loop.create_task(join_dev())

async def load_plugins():
    load(path=["plugins/basic", "plugins/assistant","plugins/account","plugins/fun","plugins/group"])

jmubot.run_in_loop(load_plugins())
jmubot.loop.create_task(tag_chat())
jmubot.loop.create_task(group_ub())


LOGS.info(f"⏳ تم استغراق {time_formatter((time.time() - start_time) * 1000)} ميللي ثانية لبدء تشغيل سورس جمثون.")

LOGS.info(
    """
    ╔══════════════════════════════════════════╗
    ║       ✅ تم تنصيب وتشغيل سورس جمثون بنجاح             ║ 
    ║       تابع آخر التحديثات من خلال قناة @Jmthon            ║
    ╚══════════════════════════════════════════╝
    """
)
if not JmdB.get_key("NOTIFY_OFF"):
        jmubot.run_in_loop(notify())
    
try:
    asst.run()
    LOGS.info(f"تم بنجاح تشغيل البوت المساعد من @Jmthon")
except SessionRevokedError:
    LOGS.info(f"جلسة البوت المساعد [@{asst.me.username}] فشلت لكن سيتم تشغيل سورس الحساب فقط")
    jmubot.run()

