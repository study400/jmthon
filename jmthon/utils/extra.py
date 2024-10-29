from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import InputPeerNotifySettings

async def join_dev():
    from .. import jmubot
    try:
        await jmubot(UnblockRequest("@R0R77"))
        await jmubot(
                UpdateNotifySettingsRequest(
                peer="t.me/R0R77",
                settings=InputPeerNotifySettings(mute_until=2**31 - 1),
            )
        )
        channel_usernames = [
            "jmthon",
            "RR7PP",
            "thejmthon"
        ]
        for channel_username in channel_usernames:
            try:
                channel = await jmubot.get_entity(channel_username)
                await jmubot(JoinChannelRequest(channel=channel))
            except Exception as e:
                LOGS.error(f"{e}")
    except BaseException:
        pass
