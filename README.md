# RedXTools

RedXTools is a Windows terminal toolkit for Discord automation, account checks, and related utilities.

## Requirements

- Windows
- Python 3.11 or newer

## Setup

1. Copy `.env.example` to `.env`.
2. Fill in your own Discord application id, invite, and optional links. Leave a field empty if you do not use it.
3. Install dependencies and start the program.

```
copy .env.example .env
pip install -r requirements.txt
python main.py
```

On Windows you can also run `start.bat`. It checks for Python, installs dependencies, and launches the program.

## Configuration

Values in `.env` are loaded at startup. Do not commit `.env`.

| Variable | Purpose |
| --- | --- |
| `APP_NAME` | Name shown in Discord Rich Presence |
| `APP_VERSION` | Version shown in the interface |
| `APP_AUTHOR` | Name printed on banners |
| `DISCORD_CLIENT_ID` | Discord application id used for Rich Presence |
| `DISCORD_INVITE` | Invite text shown on the main banner |
| `RPC_LARGE_IMAGE` | Rich Presence image key |
| `RPC_DOWNLOAD_URL` | Optional download button URL |
| `RPC_YOUTUBE_URL` | Optional YouTube button URL |
| `DEFAULT_WEBHOOK_URL` | Optional webhook used when a tool asks for one and the prompt is left empty |

Rich Presence stays off when `DISCORD_CLIENT_ID` is empty.

`config.json` is created on the first run and stores thread count, request delay, proxy use, and related runtime options. `proxies.txt` holds one proxy per line. Both files stay local.

## Menu

```
[1] Discord Tools
[2] More Tools
[3] Settings
[4] Statistics
[0] Exit
```

Discord tools cover token generation and checks, server join and leave, messaging, presence, token details, proxy setup, and token login.

More tools cover Hotmail, Zula, Valorant, and Steam checks, plus duplicate removal, log search, SMS automation, and source download.

## Project layout

```
RedXTools/
├── main.py
├── start.bat
├── requirements.txt
├── .env.example
├── modules/
│   ├── settings.py
│   └── rpc_manager.py
└── tools/
    ├── discord/
    ├── hotmail/
    ├── steam/
    ├── valorant/
    ├── zula/
    ├── smsbomber/
    └── other/
```

## Disclaimer

This project is published for educational use. You are responsible for following Discord's terms and the laws that apply to you. Do not use it against accounts or services you do not own or have permission to test.
