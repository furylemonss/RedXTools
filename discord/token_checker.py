import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore
from tkinter import Tk, filedialog
from datetime import datetime

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Token Checker")

class TokenChecker:
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
        
    def create_valid_tokens_file(self):
        now = datetime.now()
        datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        result_dir = os.path.join("results", "Discord Token Checker", datetime_str)
        os.makedirs(result_dir, exist_ok=True)
        
        self.parent.valid_tokens_file = os.path.join(result_dir, "hit.txt")
        
        if not os.path.exists(self.parent.valid_tokens_file):
            with open(self.parent.valid_tokens_file, 'w', encoding='utf-8') as f:
                f.write("")
            print(f"{Fore.GREEN}✓ Created {self.parent.valid_tokens_file}")
        
    def check_token(self, token):
        try:
            headers = self.parent.get_random_headers(token)
            
            proxies = None
            if self.parent.proxy_list:
                proxy = self.parent.get_random_proxy()
                if proxy:
                    proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            
            response = requests.get('https://discord.com/api/v9/users/@me', headers=headers, proxies=proxies, timeout=10)
            
            with self.parent.lock:
                self.parent.stats['checked'] += 1
                
            if response.status_code == 200:
                with self.parent.lock:
                    self.parent.stats['valid'] += 1
                return True, 'Valid'
            elif response.status_code == 401:
                with self.parent.lock:
                    self.parent.stats['invalid'] += 1
                return False, 'Invalid'
            elif response.status_code == 429:
                if self.parent.proxy_list:
                    wait_time = len(self.parent.proxy_list) * 2
                    print(f"{Fore.YELLOW}⚠ Rate limited! Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                return False, "Rate Limited"
            else:
                with self.parent.lock:
                    self.parent.stats['invalid'] += 1
                return False, f"Unknown ({response.status_code})"
                
        except requests.exceptions.Timeout:
            return False, "Timeout"
        except requests.exceptions.RequestException:
            return False, "Connection Error"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def check_single_token(self, token, current, total):
        try:
            is_valid, message = self.check_token(token)
            
            with self.parent.lock:
                if is_valid:
                    print(f"{Fore.GREEN}[{current}/{total}] ✓ Valid {token[:20]}...")
                    with open(self.parent.valid_tokens_file, 'a', encoding='utf-8') as f:
                        f.write(token + '\n')
                else:
                    print(f"{Fore.RED}[{current}/{total}] ✗ {message}: {token[:20]}...")
                    
            time.sleep(self.parent.delay_between_requests)
            
        except Exception as e:
            print(f"{Fore.RED}[{current}/{total}] Error: {e}")
    
    def run(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"{Fore.CYAN}TOKEN CHECKER")
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
        
        self.create_valid_tokens_file()
            
        with open(token_file_path, 'r', encoding='utf-8') as f:
            tokens = [line.strip() for line in f.readlines() if line.strip()]
            
        if not tokens:
            print(f"{Fore.RED}Token file is empty!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
            
        try:
            thread_count = int(input(f"{Fore.YELLOW}Thread count (1-{min(50, len(tokens))}): "))
            if thread_count <= 0 or thread_count > 50:
                thread_count = min(10, len(tokens))
                
            print(f"\n{Fore.GREEN}Token checking starting...")
            print(f"{Fore.CYAN}Tokens to Check: {len(tokens)}")
            print(f"{Fore.CYAN}Thread Count: {thread_count}")
            print(f"{Fore.CYAN}Result Path: {self.parent.valid_tokens_file}")
            print(f"{Fore.MAGENTA}{'='*50}")
            
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = []
                for i, token in enumerate(tokens):
                    future = executor.submit(self.check_single_token, token, i+1, len(tokens))
                    futures.append(future)
                
                for future in futures:
                    try:
                        future.result()
                    except Exception as e:
                        print(f"{Fore.RED}Error: {e}")
            
            print(f"\n{Fore.GREEN}✓ Token checking completed!")
            print(f"{Fore.CYAN}Total checked: {self.parent.stats['checked']} token")
            print(f"{Fore.CYAN}Valid: {self.parent.stats['valid']} token")
            print(f"{Fore.CYAN}Invalid: {self.parent.stats['invalid']} token")
            print(f"{Fore.CYAN}Valid tokens saved: {self.parent.valid_tokens_file}")
            
        except ValueError:
            print(f"{Fore.RED}Invalid number format!")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Token checking cancelled!")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            
        input(f"\n{Fore.YELLOW}Press Enter to continue...")