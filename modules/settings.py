import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_env(path=None):
    env_path = Path(path) if path else ROOT / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def env(name, default=""):
    return os.environ.get(name, default).strip()


load_env()

APP_NAME = env("APP_NAME", "RedXTools")
APP_VERSION = env("APP_VERSION", "2.0")
APP_AUTHOR = env("APP_AUTHOR", "RedXTools")
DISCORD_INVITE = env("DISCORD_INVITE")
DISCORD_CLIENT_ID = env("DISCORD_CLIENT_ID")
RPC_LARGE_IMAGE = env("RPC_LARGE_IMAGE", "logo")
RPC_DOWNLOAD_URL = env("RPC_DOWNLOAD_URL")
RPC_YOUTUBE_URL = env("RPC_YOUTUBE_URL")
DEFAULT_WEBHOOK_URL = env("DEFAULT_WEBHOOK_URL")
