import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
from tkinter import Tk, filedialog

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Token Offliner")

class TokenOffliner:
    def __init__(self, parent):
        self.parent = parent
        
    def select_token_file(self):
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        file_path = filedialog.askopenfilename(
            title="Select Token File",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        root.destroy()
        return file_path
        
    def set_offline_status(self, token, current, total):
        try:
            headers = self.parent.get_random_headers(token)
            
            data = {
                "status": "invisible",
                "activities": []
            }
            
            response = requests.patch('https://discord.com/api/v9/users/@me/settings', 
                                    headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}[{current}/{total}] ✓ Set offline: {token[:20]}...{Style.RESET_ALL}")
                return True
            elif response.status_code == 401:
                print(f"{Fore.RED}[{current}/{total}] ✗ Invalid token: {token[:20]}...{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[{current}/{total}] ✗ Failed ({response.status_code}): {token[:20]}...{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}[{current}/{total}] ✗ Error: {token[:20]}... - {str(e)}{Style.RESET_ALL}")
            
        time.sleep(self.parent.delay_between_requests)
        return False
    
    def run(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              TOKEN OFFLINER                                         │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}Set Discord tokens to offline/invisible status                                      {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
        print(f"{Fore.YELLOW}Select token file...{Style.RESET_ALL}")
        token_file_path = self.select_token_file()
        
        if not token_file_path:
            print(f"\n{Fore.RED}[x] No file selected!{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        if not os.path.exists(token_file_path):
            print(f"\n{Fore.RED}[x] Token file not found: {token_file_path}{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}[+] Selected file: {token_file_path}{Style.RESET_ALL}")
        
        valid_tokens = []
        with open(token_file_path, 'r', encoding='utf-8') as f:
            valid_tokens = [line.strip() for line in f.readlines() if line.strip()]
        
        if not valid_tokens:
            print(f"\n{Fore.RED}[x] Token file is empty!{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CONFIRMATION                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}Available tokens: {Fore.LIGHTCYAN_EX}{len(valid_tokens):<65}{Fore.CYAN}│
│  {Fore.YELLOW}⚠ This will set all tokens to offline/invisible status                             {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
        confirm = input(f"{Fore.YELLOW}Continue? (y/N): {Fore.WHITE}").strip().lower()
        if confirm != 'y':
            print(f"\n{Fore.YELLOW}[!] Operation cancelled{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        threads = min(int(input(f"{Fore.CYAN}Thread count (1-{self.parent.max_threads}): {Fore.WHITE}") or "5"), self.parent.max_threads)
        
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           SETTING TOKENS OFFLINE                                    │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}Tokens to process: {Fore.LIGHTCYAN_EX}{len(valid_tokens):<65}{Fore.CYAN}│
│  {Fore.WHITE}Thread count: {Fore.LIGHTCYAN_EX}{threads:<70}{Fore.CYAN}│
│                                                                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
{Style.RESET_ALL}""")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for i, token in enumerate(valid_tokens):
                future = executor.submit(self.set_offline_status, token, i+1, len(valid_tokens))
                futures.append(future)
            
            success_count = 0
            for future in futures:
                try:
                    if future.result():
                        success_count += 1
                except Exception as e:
                    print(f"{Fore.RED}[x] Error: {e}{Style.RESET_ALL}")
        
        print(f"""{Fore.CYAN}
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                  RESULTS                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.GREEN}✓ Successfully set offline: {success_count}/{len(valid_tokens):<52}{Fore.CYAN}│
│  {Fore.RED}✗ Failed: {len(valid_tokens) - success_count}/{len(valid_tokens):<70}{Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")