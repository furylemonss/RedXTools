# RedXTools

A terminal-based automation toolkit for Discord and account management operations.

## Features

### Discord Tools
- Token Generator - Generate Discord tokens
- Token Checker - Validate token authenticity
- Gen & Check - Combined generation and validation
- Server Joiner - Automated server joining
- Server Leaver - Automated server leaving
- Message Spammer - Automated messaging
- Account Nuker - Account destruction tool
- Token Onliner - Set tokens as online
- Token Offliner - Set tokens as offline
- Token Info - Retrieve token details
- Proxy Manager - Proxy configuration
- Account Login - Token-based login

### Account Checkers
- Hotmail Checker - Validate Hotmail accounts
- Zula Checker - Check Zula game accounts
- Valorant Checker - Check Valorant accounts
- Steam Checker - Validate Steam accounts

### Utility Tools
- Duplicate Remover - Remove duplicate lines from files
- Log Searcher - Search within log files
- SMS Bomber - SMS automation tool
- SrcFetch - Website source downloader

## Requirements

- Python 3.11 or higher
- Windows OS

## Installation

### Method 1: Using Start Script
```
start.bat
```

The batch script will:
1. Check for Python installation
2. Install Python silently if missing
3. Upgrade pip
4. Install dependencies
5. Launch the application

### Method 2: Manual Installation
```
pip install -r requirements.txt
python main.py
```

## Dependencies

- requests
- tqdm
- colorama
- httpx
- PyJWT
- websocket-client
- selenium
- undetected-chromedriver
- webdriver-manager
- cryptocode
- jwt
- pyperclip
- websocket
- pycryptodome
- loguru
- pypresence

## Usage

Launch the program and navigate through the menu:

```
[1] Discord Tools         - Token, server and account management
[2] More Tools            - Checkers and utility tools
[3] Settings              - Thread, proxy and other settings
[4] Statistics            - View statistics and reports
[0] Exit                  - Exit program
```

## Configuration

The tool creates a `config.json` file on first run with the following settings:

- RPC settings
- Proxy configuration
- Token generation options
- Rate limiting parameters

## Project Structure

```
RedXTools/
├── main.py                 - Main entry point
├── start.bat              - Windows launcher
├── requirements.txt       - Python dependencies
├── config.json           - Configuration file
├── proxies.txt           - Proxy list
├── modules/
│   └── rpc_manager.py    - Discord RPC integration
├── tools/
│   ├── discord/          - Discord automation tools
│   ├── hotmail/          - Hotmail checker
│   ├── other/            - Utility tools
│   ├── smsbomber/        - SMS automation
│   ├── steam/            - Steam checker
│   ├── valorant/         - Valorant checker
│   └── zula/             - Zula checker
└── results/              - Output directory
```

## Stats Tracking

The application tracks:
- Generated tokens
- Checked tokens
- Valid/Invalid tokens
- Servers joined/left
- Messages sent
- Accounts nuked

## Author

- Developer: furylemons
- Version: 2.0
- Discord: .gg/FXhFrV3rqe

## Disclaimer

This tool is for educational purposes only. Users are responsible for complying with Discord's Terms of Service and applicable laws.
