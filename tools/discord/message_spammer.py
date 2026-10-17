import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore
from tkinter import Tk, filedialog

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Message Spammer")

class MessageSpammer:
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
        
    def send_message(self, token, channel_id, message, current, total):
        try:
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            data = {'content': message}
            response = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages', 
                                   headers=headers, json=data, timeout=10)
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}[{current}/{total}] ✓ Message sent: {token[:20]}...")
                with self.parent.lock:
                    self.parent.stats['spammed'] += 1
                return True
            elif response.status_code == 401:
                print(f"{Fore.RED}[{current}/{total}] ✗ Invalid token: {token[:20]}...")
            elif "rate limited" in response.text.lower():
                print(f"{Fore.YELLOW}[{current}/{total}] ⚠ Rate limited: {token[:20]}...")
            else:
                print(f"{Fore.RED}[{current}/{total}] ✗ Error ({response.status_code}): {token[:20]}...")
                
        except Exception as e:
            print(f"{Fore.RED}[{current}/{total}] ✗ Error: {token[:20]}... - {str(e)}")
            
        time.sleep(self.parent.delay_between_requests)
        return False
    
    def run(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"{Fore.CYAN}MESSAGE SPAMMER")
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
            
        channel_id = input(f"{Fore.YELLOW}Channel ID: ").strip()
        message = input(f"{Fore.YELLOW}Message: ").strip()
        count = int(input(f"{Fore.YELLOW}Message count: ") or "10")
        threads = min(int(input(f"{Fore.YELLOW}Thread count (1-{self.parent.max_threads}): ") or "5"), self.parent.max_threads)
        
        if not channel_id or not message:
            print(f"{Fore.RED}Invalid input!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
            
        print(f"\n{Fore.GREEN}Message spam starting...")
        print(f"{Fore.CYAN}Channel ID: {channel_id}")
        print(f"{Fore.CYAN}Message: {message}")
        print(f"{Fore.CYAN}Message Count: {count}")
        print(f"{Fore.CYAN}Token Count: {len(valid_tokens)}\n")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for i in range(count):
                for token in valid_tokens:
                    future = executor.submit(self.send_message, token, channel_id, message, i+1, count)
                    futures.append(future)
                    
            sent_count = 0
            for future in futures:
                try:
                    if future.result():
                        sent_count += 1
                except Exception as e:
                    print(f"{Fore.RED}Error: {e}")
                    
        print(f"\n{Fore.GREEN}✓ Total {sent_count} messages sent!")
        input(f"\n{Fore.YELLOW}Press Enter to continue...")