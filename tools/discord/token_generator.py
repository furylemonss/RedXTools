import os
import time
import random
import string
import threading
import base64
import queue
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Token Generator")

class TokenGenerator:
    def __init__(self, parent):
        self.parent = parent
        self.token_prefixes = ['MT', 'ND', 'QT']
        self.prefix_weights = [0.5, 0.3, 0.2]
        
    def generate_realistic_token(self):
        user_id = random.randint(100000000000000000, 999999999999999999)
        user_id_bytes = str(user_id).encode('ascii')
        base64_userid = base64.b64encode(user_id_bytes).decode('ascii').rstrip('=')
        
        prefix = random.choices(self.token_prefixes, weights=self.prefix_weights)[0]
        
        chars = string.ascii_letters + string.digits
        suffix = ''.join(random.choice(chars) for _ in range(27))
        
        token = f"{base64_userid}.{prefix}.{suffix}"
        
        if len(token) != 72:
            needed = 72 - len(token)
            token += ''.join(random.choice(chars) for _ in range(needed))
            
        return token[:72]
        
    def save_token_immediately(self, token):
        with self.parent.lock:
            with open(self.parent.tokens_file, 'a', encoding='utf-8') as f:
                f.write(token + '\n')
            self.parent.stats['generated'] += 1
            
    def generate_token_only(self, current, total):
        try:
            token = self.generate_realistic_token()
            self.save_token_immediately(token)
            
            with self.parent.lock:
                print(f"{Fore.GREEN}[{current}/{total}] {'Token generated'} {token[:20]}...")
                
            time.sleep(self.parent.delay_between_requests)
            
        except Exception as e:
            print(f"{Fore.RED}[{current}/{total}] {'Error:'} {e}")
    
    def run(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"{Fore.CYAN}{'TOKEN GENERATOR'}")
        print(f"{Fore.MAGENTA}{'='*30}")
        
        try:
            count = int(input(f"{Fore.YELLOW}{'How many tokens do you want to generate: '}"))
            if count <= 0:
                print(f"{Fore.RED}{'Invalid number!'}")
                return
                
            print(f"\n{Fore.GREEN}{'Token generation starting...'}")
            print(f"{Fore.CYAN}{'Tokens to Generate:'} {count}")
            print(f"{Fore.CYAN}{'Thread Count:'} {self.parent.max_threads}")
            print(f"{Fore.MAGENTA}{'='*50}")
            
            with ThreadPoolExecutor(max_workers=self.parent.max_threads) as executor:
                futures = []
                for i in range(count):
                    future = executor.submit(self.generate_token_only, i+1, count)
                    futures.append(future)
                
                for future in futures:
                    try:
                        future.result()
                    except Exception as e:
                        print(f"{Fore.RED}{'Error:'} {e}")
            
            print(f"\n{Fore.GREEN}{'✓ Token generation completed!'}")
            print(f"{Fore.CYAN}{'Total generated:'} {self.parent.stats['generated']} token")
            print(f"{Fore.CYAN}{'Saved file:'} {self.parent.tokens_file}")
            
        except ValueError:
            print(f"{Fore.RED}{'Invalid number format!'}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}{'Token generation cancelled!'}")
        except Exception as e:
            print(f"{Fore.RED}{'Error:'} {e}")
            
        input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
