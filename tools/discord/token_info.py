import os
import time
from colorama import Fore

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Token Info Viewer")

class TokenInfo:
    def __init__(self, parent):
        self.parent = parent
        
    def run(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"{Fore.CYAN}{'TOKEN INFO VIEWER'}")
        print(f"{Fore.MAGENTA}{'='*30}")
        
        token = input(f"{Fore.YELLOW}{'Enter token:'}: ").strip()
        
        if not token:
            print(f"{Fore.RED}{'Invalid token!'}")
            input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
            return
            
        print(f"\n{Fore.CYAN}{'Getting token information...'}")
        print(f"{Fore.MAGENTA}{'='*50}")
        
        token_info = self.parent.get_token_info(token)
        
        if token_info:
            print(f"\n{Fore.GREEN}✓ {'Token is valid'}")
            print(f"{Fore.CYAN}{'='*50}")
            
            print(f"{Fore.WHITE}👤 {'Username:'}: {Fore.CYAN}{token_info['username']}#{token_info['discriminator']}")
            print(f"{Fore.WHITE}🆔 {'User ID:'}: {Fore.CYAN}{token_info['user_id']}")
            print(f"{Fore.WHITE}📧 {'Email:'}: {Fore.CYAN}{token_info['email']}")
            print(f"{Fore.WHITE}📱 {'Phone:'}: {Fore.CYAN}{token_info['phone']}")
            print(f"{Fore.WHITE}✅ {'Verified:'}: {Fore.GREEN if token_info['verified'] else Fore.RED}{token_info['verified']}")
            print(f"{Fore.WHITE}🔐 {'2FA:'}: {Fore.GREEN if token_info['mfa_enabled'] else Fore.RED}{token_info['mfa_enabled']}")
            print(f"{Fore.WHITE}🌍 {'Locale:'}: {Fore.CYAN}{token_info['locale']}")
            print(f"{Fore.WHITE}💎 {'Nitro:'}: {Fore.GREEN if token_info['has_nitro'] else Fore.RED}{token_info['has_nitro']}")
            print(f"{Fore.WHITE}🏅 {'Badges:'}: {Fore.CYAN}{', '.join(token_info['badges'])}")
            print(f"{Fore.WHITE}📅 {'Creation Date:'}: {Fore.CYAN}{token_info['creation_date']}")
            
            if token_info['avatar_url']:
                print(f"{Fore.WHITE}🖼️  {'Avatar URL:'}: {Fore.CYAN}{token_info['avatar_url']}")
                
        else:
            print(f"\n{Fore.RED}✗ {'Token is invalid'}")
            
        print(f"\n{Fore.MAGENTA}{'='*50}")
        input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
