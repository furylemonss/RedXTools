import time
import os
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore
from datetime import datetime

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Token Generator and Checker")

class TokenGeneratorAndChecker:
    def __init__(self, parent):
        self.parent = parent
        
    def create_valid_tokens_file(self):
        now = datetime.now()
        datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        result_dir = os.path.join("results", "Discord Token Generator and Checker", datetime_str)
        os.makedirs(result_dir, exist_ok=True)
        
        self.parent.valid_tokens_file = os.path.join(result_dir, "hit.txt")
        
        if not os.path.exists(self.parent.valid_tokens_file):
            with open(self.parent.valid_tokens_file, 'w', encoding='utf-8') as f:
                f.write("")
            print(f"{Fore.GREEN}✓ Created {self.parent.valid_tokens_file}")
        
    def generate_and_check_token(self, current, total):
        try:
            token = self.parent.token_generator.generate_realistic_token()
            
            self.parent.token_generator.save_token_immediately(token)
            
            print(f"{Fore.BLUE}[{current}/{total}] Token generated: {token[:20]}...")
            
            is_valid, status = self.parent.token_checker.check_token(token)
            
            if is_valid:
                print(f"{Fore.GREEN}[{current}/{total}] ✓ Valid: {token[:20]}...")
                with self.parent.lock:
                    with open(self.parent.valid_tokens_file, 'a', encoding='utf-8') as f:
                        f.write(token + '\n')
            else:
                print(f"{Fore.RED}[{current}/{total}] ✗ {status}: {token[:20]}...")
                
            time.sleep(self.parent.delay_between_requests)
            
        except Exception as e:
            print(f"{Fore.RED}[{current}/{total}] Error: {e}")
    
    def run(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"{Fore.CYAN}TOKEN GENERATOR & CHECKER")
        print(f"{Fore.MAGENTA}{'='*40}")
        
        self.create_valid_tokens_file()
        
        try:
            count = int(input(f"{Fore.YELLOW}How many tokens to create and check: "))
            threads = int(input(f"{Fore.YELLOW}Thread count (1-{self.parent.max_threads}): "))
            
            if count <= 0 or threads <= 0 or threads > self.parent.max_threads:
                print(f"{Fore.RED}Invalid value!")
                time.sleep(2)
                return
                
            print(f"\n{Fore.GREEN}Creating and checking tokens...")
            print(f"{Fore.CYAN}Total threads: {threads}")
            print(f"{Fore.CYAN}Total tokens: {count}")
            print(f"{Fore.CYAN}Result Path: {self.parent.valid_tokens_file}")
            print(f"{Fore.MAGENTA}{'='*50}\n")
            
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                
                for i in range(count):
                    future = executor.submit(self.generate_and_check_token, i+1, count)
                    futures.append(future)
                    
                for future in futures:
                    try:
                        future.result()
                    except Exception as e:
                        print(f"{Fore.RED}Error: {e}")
                        
            print(f"\n{Fore.GREEN}✓ Process completed!")
            print(f"{Fore.CYAN}Created: {self.parent.stats['generated']}")
            print(f"{Fore.CYAN}Checked: {self.parent.stats['checked']}")
            print(f"{Fore.GREEN}Valid: {self.parent.stats['valid']}")
            print(f"{Fore.RED}Invalid: {self.parent.stats['invalid']}")
            print(f"{Fore.CYAN}Valid tokens saved: {self.parent.valid_tokens_file}")
            
        except ValueError:
            print(f"{Fore.RED}Invalid input!")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
            
        input(f"\n{Fore.YELLOW}Press Enter to continue...")