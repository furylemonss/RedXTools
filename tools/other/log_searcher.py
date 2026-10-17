import os
import re
import platform
from colorama import Fore, init
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

import modules.rpc_manager as rpc_manager
from modules.settings import APP_AUTHOR
rpc_manager.set_details("Log Searcher")

init(autoreset=True)

class LogSearcher:
    def __init__(self, parent=None):
        self.parent = parent
        self.version = "1.0"
        self.author = APP_AUTHOR
        
    def clear_screen(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')
        
    def print_banner(self):
        banner = f"""
{Fore.BLUE}╔══════════════════════════════════════════════════════════════════════════════════╗
{Fore.BLUE}║                                                                                  ║
{Fore.BLUE}║  {Fore.LIGHTBLACK_EX}██████╗ ███████╗██████╗ ██╗  ██╗   {Fore.RED}████████╗ ██████╗  ██████╗ ██╗     ███████╗{Fore.BLUE}  ║
{Fore.BLUE}║  {Fore.LIGHTBLACK_EX}██╔══██╗██╔════╝██╔══██╗╚██╗██╔╝   {Fore.RED}╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝{Fore.BLUE}  ║
{Fore.BLUE}║  {Fore.LIGHTBLACK_EX}██████╔╝█████╗  ██║  ██║ ╚███╔╝       {Fore.RED}██║   ██║   ██║██║   ██║██║     ███████╗{Fore.BLUE}  ║
{Fore.BLUE}║  {Fore.LIGHTBLACK_EX}██╔══██╗██╔══╝  ██║  ██║ ██╔██╗       {Fore.RED}██║   ██║   ██║██║   ██║██║     ╚════██║{Fore.BLUE}  ║
{Fore.BLUE}║  {Fore.LIGHTBLACK_EX}██║  ██║███████╗██████╔╝██╔╝ ██╗      {Fore.RED}██║   ╚██████╔╝╚██████╔╝███████╗███████║{Fore.BLUE}  ║
{Fore.BLUE}║  {Fore.LIGHTBLACK_EX}╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝      {Fore.RED}╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝{Fore.BLUE}  ║
{Fore.BLUE}║                                                                                  ║
{Fore.BLUE}║  {Fore.BLUE}╔═══════════════════════════════════════════════════════════╗  {Fore.BLUE}                 ║
{Fore.BLUE}║  {Fore.BLUE}║{Fore.GREEN}  RedX Tools v{self.version} {Fore.RESET}- {Fore.GREEN} Developer: {Fore.RED}{self.author}                  {Fore.BLUE}║               {Fore.BLUE}    ║
{Fore.BLUE}║  {Fore.BLUE}╚═══════════════════════════════════════════════════════════╝  {Fore.BLUE}                 ║
{Fore.BLUE}║                                                                                  ║
{Fore.BLUE}╚══════════════════════════════════════════════════════════════════════════════════╝
"""
        print(banner)
        
    def get_desktop_path(self):
        if platform.system() == 'Windows':
            import winreg
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
                    desktop_path = winreg.QueryValueEx(key, "Desktop")[0]
                    return desktop_path
            except:
                return os.path.join(os.path.expanduser("~"), "Desktop")
        else:
            return os.path.join(os.path.expanduser("~"), "Desktop")
    
    def search_logs(self):
        self.clear_screen()
        self.print_banner()
        
        print(f"{Fore.CYAN}{'LOG SEARCH TOOL'}")
        print(f"{Fore.MAGENTA}{'='*50}")
        
        search_term = input(f"{Fore.YELLOW}{'Enter search term:'} ").strip()
        
        if not search_term:
            print(f"{Fore.RED}{'No search term entered!'}")
            input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
            return
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        print(f"{Fore.YELLOW}{'Select logs folder:'}")
        input_folder = filedialog.askdirectory(title="Select Logs Folder")
        
        root.destroy()
        
        if not input_folder:
            print(f"{Fore.RED}{'No folder selected!'}")
            input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
            return
            
        desktop_path = self.get_desktop_path()
        
        if not os.path.exists(input_folder):
            print(f"{Fore.RED}{'Selected folder not found!'}")
            input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
            return
        
        log_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
        
        if not log_files:
            print(f"{Fore.RED}{'No .txt files found in logs folder!'}")
            input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
            return
        
        safe_name = re.sub(r'[^a-z0-9]', '_', search_term.lower())
        output_file = os.path.join(desktop_path, f"results_{safe_name}.txt")
        
        found_count = 0
        
        print(f"\n{Fore.CYAN}{'Searching for'} '{search_term}' {'in all logs...'}\n")
        
        for file in log_files:
            file_path = os.path.join(input_folder, file)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
                for line in lines:
                    if search_term.lower() in line.lower():
                        parts = line.strip().split(':')
                        
                        if len(parts) >= 3:
                            password = parts[-1].strip()
                            email = parts[-2].strip()
                            
                            if (password and email and 
                                len(password) > 2 and len(email) > 2 and
                                '@' in email):
                                
                                with open(output_file, 'a', encoding='utf-8') as out_f:
                                    out_f.write(f"{email}:{password}\n")
                                found_count += 1
                                
            except Exception as e:
                print(f"{Fore.RED}{'Error reading file:'} {file} - {str(e)}")
        
        if found_count == 0:
            print(f"{Fore.YELLOW}{'No results found for'} '{search_term}'")
            print(f"{Fore.YELLOW}{'Try a different search term or check your log files.'}")
        else:
            print(f"\n{Fore.GREEN}{'='*50}")
            print(f"{Fore.GREEN}{'Scan completed!'}")
            print(f"{Fore.CYAN}{'Accounts found:'} {found_count}")
            print(f"{Fore.CYAN}{'Output file:'} {os.path.basename(output_file)}")
            print(f"{Fore.CYAN}{'Location:'} Desktop")
            print(f"{Fore.GREEN}{'='*50}")
        
        input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
    
    def run(self):
        self.search_logs()

if __name__ == "__main__":
    try:
        app = LogSearcher()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}{'Program interrupted by user.'}")
    except Exception as e:
        print(f"{Fore.RED}{'Error:'} {str(e)}")
