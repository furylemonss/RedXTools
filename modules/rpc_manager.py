from pypresence import Presence
import time

from modules.settings import (
    APP_NAME,
    APP_VERSION,
    DISCORD_CLIENT_ID,
    RPC_DOWNLOAD_URL,
    RPC_LARGE_IMAGE,
    RPC_YOUTUBE_URL,
)

RPC = None
rpc_start = int(time.time())


def start():
    global RPC
    if not DISCORD_CLIENT_ID:
        return
    RPC = Presence(DISCORD_CLIENT_ID)
    RPC.connect()


def set_details(text):
    if RPC is None:
        return

    buttons = []
    if RPC_DOWNLOAD_URL:
        buttons.append({"label": "Download", "url": RPC_DOWNLOAD_URL})
    if RPC_YOUTUBE_URL:
        buttons.append({"label": "YouTube", "url": RPC_YOUTUBE_URL})

    payload = {
        "details": text,
        "state": APP_NAME,
        "large_image": RPC_LARGE_IMAGE,
        "large_text": f"Version {APP_VERSION}",
        "start": rpc_start,
    }
    if buttons:
        payload["buttons"] = buttons
    RPC.update(**payload)
