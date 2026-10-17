import os
import time
from colorama import Fore, Style
from tkinter import Tk, filedialog

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Manage Proxies")

class ProxyManager:
    def __init__(self, parent):
        self.parent = parent
        
    def select_proxy_file(self):
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        file_path = filedialog.askopenfilename(
            title="Select Proxy File",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        root.destroy()
        return file_path
        
    def run(self):
        while True:
            self.parent.clear_screen()
            self.parent.print_banner()
            
            menu = f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                 PROXY MANAGER                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}1{Fore.WHITE}]{Fore.CYAN} Load Proxies               {Fore.WHITE}[{Fore.LIGHTCYAN_EX}2{Fore.WHITE}]{Fore.CYAN} Add Proxy                {Fore.WHITE}[{Fore.LIGHTCYAN_EX}3{Fore.WHITE}]{Fore.CYAN} Remove Proxy       {Fore.CYAN}│
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}4{Fore.WHITE}]{Fore.CYAN} List Proxies               {Fore.WHITE}[{Fore.LIGHTCYAN_EX}5{Fore.WHITE}]{Fore.CYAN} Clear Proxies            {Fore.WHITE}[{Fore.LIGHTCYAN_EX}6{Fore.WHITE}]{Fore.CYAN} Test Proxies       {Fore.CYAN}│
│                                                                                     │
│  {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}]{Fore.RED} Back                                                                           {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}"""
            print(menu)
            
            choice = input(f"{Fore.CYAN}┌─[{Fore.WHITE}SELECT{Fore.CYAN}]\n└──> {Fore.WHITE}").strip()
            
            if choice == '1':
                self.load_proxies()
            elif choice == '2':
                self.add_proxy()
            elif choice == '3':
                self.remove_proxy()
            elif choice == '4':
                self.list_proxies()
            elif choice == '5':
                self.clear_proxies()
            elif choice == '6':
                self.test_proxies()
            elif choice == '0':
                break
            else:
                print(f"\n{Fore.RED}[x] Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)
    
    def load_proxies(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              LOAD PROXIES                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}1{Fore.WHITE}]{Fore.CYAN} Load from default file (proxies.txt)                                           {Fore.CYAN}│
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}2{Fore.WHITE}]{Fore.CYAN} Select custom file                                                             {Fore.CYAN}│
│                                                                                     │
│  {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}]{Fore.RED} Back                                                                           {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
        choice = input(f"{Fore.CYAN}┌─[{Fore.WHITE}SELECT{Fore.CYAN}]\n└──> {Fore.WHITE}").strip()
        
        if choice == '1':
            self.parent.load_proxies()
            print(f"\n{Fore.GREEN}[+] {len(self.parent.proxy_list)} proxies loaded from {self.parent.proxies_file}{Style.RESET_ALL}")
        elif choice == '2':
            print(f"\n{Fore.YELLOW}Select proxy file...{Style.RESET_ALL}")
            proxy_file = self.select_proxy_file()
            
            if proxy_file and os.path.exists(proxy_file):
                with open(proxy_file, 'r', encoding='utf-8') as f:
                    proxies = [line.strip() for line in f.readlines() if line.strip()]
                    self.parent.proxy_list.extend(proxies)
                print(f"\n{Fore.GREEN}[+] {len(proxies)} proxies loaded from {proxy_file}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}[x] No file selected or file not found{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def add_proxy(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                ADD PROXY                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}Format: ip:port:username:password or ip:port                                       {Fore.CYAN}│
│  {Fore.WHITE}Example: 127.0.0.1:8080:user:pass                                                  {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
        proxy = input(f"{Fore.CYAN}Enter proxy: {Fore.WHITE}").strip()
        
        if proxy:
            self.parent.proxy_list.append(proxy)
            with open(self.parent.proxies_file, 'a', encoding='utf-8') as f:
                f.write(proxy + '\n')
            print(f"\n{Fore.GREEN}[+] Proxy added: {proxy}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}[x] Invalid proxy format{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def remove_proxy(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        if not self.parent.proxy_list:
            print(f"\n{Fore.YELLOW}[!] No proxies loaded{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        self.list_proxies_simple()
        
        try:
            index = int(input(f"\n{Fore.CYAN}Enter proxy number to remove: {Fore.WHITE}")) - 1
            if 0 <= index < len(self.parent.proxy_list):
                removed = self.parent.proxy_list.pop(index)
                self.save_proxies()
                print(f"\n{Fore.GREEN}[+] Proxy removed: {removed}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}[x] Invalid proxy number{Style.RESET_ALL}")
        except ValueError:
            print(f"\n{Fore.RED}[x] Invalid input{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def list_proxies(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        self.list_proxies_simple()
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def list_proxies_simple(self):
        if not self.parent.proxy_list:
            print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PROXY LIST                                             │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.YELLOW}No proxies loaded                                                                  {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
            return
        
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         PROXY LIST ({len(self.parent.proxy_list)} proxies)                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │{Style.RESET_ALL}""")
        
        for i, proxy in enumerate(self.parent.proxy_list, 1):
            print(f"{Fore.CYAN}│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}{i:>2}{Fore.WHITE}] {proxy:<76}{Fore.CYAN}│{Style.RESET_ALL}")
        
        print(f"""{Fore.CYAN}│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
    
    def clear_proxies(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CLEAR PROXIES                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.RED}⚠ WARNING: This will delete all loaded proxies!                                    {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
        confirm = input(f"{Fore.YELLOW}Clear all proxies? (y/N): {Fore.WHITE}").strip().lower()
        
        if confirm == 'y':
            self.parent.proxy_list.clear()
            with open(self.parent.proxies_file, 'w', encoding='utf-8') as f:
                f.write("")
            print(f"\n{Fore.GREEN}[+] All proxies cleared{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}[!] Operation cancelled{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def test_proxies(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        if not self.parent.proxy_list:
            print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              TEST PROXIES                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.YELLOW}No proxies to test                                                                {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              TEST PROXIES                                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │{Style.RESET_ALL}""")
        
        import requests
        working_count = 0
        
        for i, proxy in enumerate(self.parent.proxy_list, 1):
            try:
                proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
                response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
                if response.status_code == 200:
                    print(f"{Fore.CYAN}│  {Fore.GREEN}[{i}/{len(self.parent.proxy_list)}] ✓ Working: {proxy:<61}{Fore.CYAN}│{Style.RESET_ALL}")
                    working_count += 1
                else:
                    print(f"{Fore.CYAN}│  {Fore.RED}[{i}/{len(self.parent.proxy_list)}] ✗ Failed: {proxy:<62}{Fore.CYAN}│{Style.RESET_ALL}")
            except Exception as e:
                error_msg = str(e)[:40]
                print(f"{Fore.CYAN}│  {Fore.RED}[{i}/{len(self.parent.proxy_list)}] ✗ Error: {proxy:<63}{Fore.CYAN}│{Style.RESET_ALL}")
        
        print(f"""{Fore.CYAN}│                                                                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  {Fore.GREEN}Working proxies: {working_count}/{len(self.parent.proxy_list):<62}{Fore.CYAN}│
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def save_proxies(self):
        with open(self.parent.proxies_file, 'w', encoding='utf-8') as f:
            for proxy in self.parent.proxy_list:
                f.write(proxy + '\n')