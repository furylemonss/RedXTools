import os
import sys
from colorama import Fore, Style, init
import tkinter as tk
from tkinter import filedialog
import time

import modules.rpc_manager as rpc_manager
from modules.settings import APP_AUTHOR
rpc_manager.set_details("Duplicate Remover")

init(autoreset=True)

class DuplicateRemover:
    def __init__(self, main_app):
        self.main_app = main_app
        self.version = "1.1"
        self.author = APP_AUTHOR
        self.case_sensitive = True
        self.preserve_order = True
        self.create_backup = True
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        self.clear_screen()
        
        banner = f"""{Fore.MAGENTA}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                     │
│        ██████╗ ██╗   ██╗██████╗ ██╗     ██╗ ██████╗ █████╗ ████████╗███████╗        │
│        ██╔══██╗██║   ██║██╔══██╗██║     ██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝        │
│        ██║  ██║██║   ██║██████╔╝██║     ██║██║     ███████║   ██║   █████╗          │
│        ██║  ██║██║   ██║██╔═══╝ ██║     ██║██║     ██╔══██║   ██║   ██╔══╝          │
│        ██████╔╝╚██████╔╝██║     ███████╗██║╚██████╗██║  ██║   ██║   ███████╗        │
│        ╚═════╝  ╚═════╝ ╚═╝     ╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝        │
│                                                                                     │
│                      ──── DUPLICATE LINE REMOVER ────                               │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}"""
        print(banner)
        
    def print_menu(self):
        print(f"""
{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              DUPLICATE REMOVER                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.LIGHTMAGENTA_EX}1{Fore.WHITE}]{Fore.MAGENTA} Single File Cleanup              {Fore.WHITE}Remove duplicates from one file               {Fore.MAGENTA}│
│  {Fore.WHITE}[{Fore.LIGHTMAGENTA_EX}2{Fore.WHITE}]{Fore.MAGENTA} Multiple Files Cleanup           {Fore.WHITE}Process multiple files at once                {Fore.MAGENTA}│
│  {Fore.WHITE}[{Fore.LIGHTMAGENTA_EX}3{Fore.WHITE}]{Fore.MAGENTA} Directory Processing             {Fore.WHITE}Clean all files in a directory                {Fore.MAGENTA}│
│  {Fore.WHITE}[{Fore.LIGHTMAGENTA_EX}4{Fore.WHITE}]{Fore.MAGENTA} Compare Files                    {Fore.WHITE}Find common and unique lines                  {Fore.MAGENTA}│
│  {Fore.WHITE}[{Fore.LIGHTMAGENTA_EX}5{Fore.WHITE}]{Fore.MAGENTA} Statistics                       {Fore.WHITE}Analyze duplicate statistics                  {Fore.MAGENTA}│
│  {Fore.WHITE}[{Fore.LIGHTMAGENTA_EX}6{Fore.WHITE}]{Fore.MAGENTA} Settings                         {Fore.WHITE}Configure processing options                  {Fore.MAGENTA}│
│  {Fore.WHITE}[{Fore.LIGHTMAGENTA_EX}7{Fore.WHITE}]{Fore.MAGENTA} Help                             {Fore.WHITE}View usage instructions                       {Fore.MAGENTA}│
│                                                                                     │
│  {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}]{Fore.RED} Back                                                                           {Fore.MAGENTA}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
    def remove_duplicates_from_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                print(f"{Fore.RED}[x] File not found: {file_path}{Style.RESET_ALL}")
                return False
                
            print(f"\n{Fore.CYAN}{'─'*85}")
            print(f"{Fore.CYAN}[*] Processing: {os.path.basename(file_path)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─'*85}{Style.RESET_ALL}\n")
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            original_count = len(lines)
            print(f"{Fore.CYAN}[*] Original lines: {original_count}{Style.RESET_ALL}")
            
            seen = set()
            unique_lines = []
            
            for line in lines:
                line = line.rstrip('\n\r')
                check_line = line if self.case_sensitive else line.lower()
                
                if check_line not in seen:
                    seen.add(check_line)
                    unique_lines.append(line)
                        
            if self.create_backup:
                backup_path = file_path + '.backup'
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.writelines([line + '\n' for line in [l.rstrip('\n\r') for l in lines]])
                print(f"{Fore.GREEN}[+] Backup created: {backup_path}{Style.RESET_ALL}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines([line + '\n' for line in unique_lines])
                
            removed_count = original_count - len(unique_lines)
            
            print(f"\n{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────────────────────────────┐")
            print(f"{Fore.MAGENTA}│                                   RESULTS                                           │")
            print(f"{Fore.MAGENTA}├─────────────────────────────────────────────────────────────────────────────────────┤")
            print(f"{Fore.MAGENTA}│                                                                                     │")
            print(f"{Fore.MAGENTA}│  {Fore.WHITE}Original Lines:{Fore.MAGENTA}{original_count:>67} {Fore.MAGENTA}│")
            print(f"{Fore.MAGENTA}│  {Fore.GREEN}Unique Lines:{Fore.MAGENTA}{len(unique_lines):>69} {Fore.MAGENTA}│")
            print(f"{Fore.MAGENTA}│  {Fore.RED}Duplicates Removed:{Fore.MAGENTA}{removed_count:>63} {Fore.MAGENTA}│")
            reduction = (removed_count/original_count*100) if original_count > 0 else 0
            print(f"{Fore.MAGENTA}│  {Fore.CYAN}Reduction:{Fore.MAGENTA}{reduction:>71.2f}% {Fore.MAGENTA}│")
            print(f"{Fore.MAGENTA}│                                                                                     │")
            print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n")
            
            print(f"{Fore.GREEN}[+] File cleaned successfully!{Style.RESET_ALL}")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}[x] Error: {str(e)}{Style.RESET_ALL}")
            return False
            
    def process_multiple_files(self):
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{Fore.CYAN}{'─'*85}")
        print(f"{Fore.CYAN}[*] Multiple File Processing{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*85}{Style.RESET_ALL}\n")
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        print(f"{Fore.MAGENTA}[*] Opening file dialog...{Style.RESET_ALL}")
        files = filedialog.askopenfilenames(
            title="Select Multiple Files to Remove Duplicates",
            filetypes=[
                ("Text files", "*.txt"), 
                ("CSV files", "*.csv"), 
                ("Log files", "*.log"), 
                ("JSON files", "*.json"), 
                ("All files", "*.*")
            ]
        )
        
        root.destroy()
        
        if not files:
            print(f"{Fore.RED}[x] No files selected!{Style.RESET_ALL}")
            return
            
        print(f"{Fore.GREEN}[+] Selected {len(files)} files{Style.RESET_ALL}\n")
        
        success_count = 0
        total_removed = 0
        
        for i, file_path in enumerate(files, 1):
            print(f"{Fore.CYAN}[{i}/{len(files)}] Processing: {os.path.basename(file_path)}{Style.RESET_ALL}")
            if self.remove_duplicates_from_file(file_path):
                success_count += 1
            print()
            
        print(f"{Fore.GREEN}┌─────────────────────────────────────────────────────────────────────────────────────┐")
        print(f"{Fore.GREEN}│                              BATCH RESULTS                                          │")
        print(f"{Fore.GREEN}├─────────────────────────────────────────────────────────────────────────────────────┤")
        print(f"{Fore.GREEN}│                                                                                     │")
        print(f"{Fore.GREEN}│  {Fore.WHITE}Total Files:{Fore.GREEN}{len(files):>70} {Fore.GREEN}│")
        print(f"{Fore.GREEN}│  {Fore.GREEN}Successful:{Fore.GREEN}{success_count:>71} {Fore.GREEN}│")
        print(f"{Fore.GREEN}│  {Fore.RED}Failed:{Fore.GREEN}{len(files) - success_count:>75} {Fore.GREEN}│")
        print(f"{Fore.GREEN}│                                                                                     │")
        print(f"{Fore.GREEN}└─────────────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n")
        
    def process_directory(self):
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{Fore.CYAN}{'─'*85}")
        print(f"{Fore.CYAN}[*] Directory Processing{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*85}{Style.RESET_ALL}\n")
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        print(f"{Fore.MAGENTA}[*] Opening directory dialog...{Style.RESET_ALL}")
        directory = filedialog.askdirectory(title="Select Directory to Process")
        
        root.destroy()
        
        if not directory:
            print(f"{Fore.RED}[x] No directory selected!{Style.RESET_ALL}")
            return
            
        if not os.path.exists(directory):
            print(f"{Fore.RED}[x] Directory not found!{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}[+] Directory selected: {directory}{Style.RESET_ALL}")
        
        file_extensions = input(f"\n{Fore.MAGENTA}Enter file extensions (e.g., .txt,.csv,.log) [empty=all]: {Fore.WHITE}").strip()
        
        if file_extensions:
            extensions = [ext.strip() for ext in file_extensions.split(',')]
            print(f"{Fore.GREEN}[+] Processing files with extensions: {', '.join(extensions)}{Style.RESET_ALL}")
        else:
            extensions = None
            print(f"{Fore.GREEN}[+] Processing all files{Style.RESET_ALL}")
        
        print()
        
        success_count = 0
        total_files = 0
        
        for root_dir, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root_dir, file)
                
                if extensions:
                    if not any(file.endswith(ext) for ext in extensions):
                        continue
                        
                total_files += 1
                print(f"{Fore.CYAN}[{total_files}] Processing: {file}{Style.RESET_ALL}")
                if self.remove_duplicates_from_file(file_path):
                    success_count += 1
                print()
        
        print(f"{Fore.GREEN}┌─────────────────────────────────────────────────────────────────────────────────────┐")
        print(f"{Fore.GREEN}│                           DIRECTORY RESULTS                                         │")
        print(f"{Fore.GREEN}├─────────────────────────────────────────────────────────────────────────────────────┤")
        print(f"{Fore.GREEN}│                                                                                     │")
        print(f"{Fore.GREEN}│  {Fore.WHITE}Total Files:{Fore.GREEN}{total_files:>70} {Fore.GREEN}│")
        print(f"{Fore.GREEN}│  {Fore.GREEN}Successful:{Fore.GREEN}{success_count:>71} {Fore.GREEN}│")
        print(f"{Fore.GREEN}│  {Fore.RED}Failed:{Fore.GREEN}{total_files - success_count:>75} {Fore.GREEN}│")
        print(f"{Fore.GREEN}│                                                                                     │")
        print(f"{Fore.GREEN}└─────────────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n")
        
    def compare_files(self):
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{Fore.CYAN}{'─'*85}")
        print(f"{Fore.CYAN}[*] File Comparison{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*85}{Style.RESET_ALL}\n")
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        print(f"{Fore.MAGENTA}[*] Select first file...{Style.RESET_ALL}")
        file1 = filedialog.askopenfilename(
            title="Select First File",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("Log files", "*.log"), ("All files", "*.*")]
        )
        
        if not file1:
            root.destroy()
            print(f"{Fore.RED}[x] No first file selected!{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}[+] First file: {os.path.basename(file1)}{Style.RESET_ALL}")
        
        print(f"{Fore.MAGENTA}[*] Select second file...{Style.RESET_ALL}")
        file2 = filedialog.askopenfilename(
            title="Select Second File",
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("Log files", "*.log"), ("All files", "*.*")]
        )
        
        root.destroy()
        
        if not file2:
            print(f"{Fore.RED}[x] No second file selected!{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}[+] Second file: {os.path.basename(file2)}{Style.RESET_ALL}\n")
        
        if not os.path.exists(file1) or not os.path.exists(file2):
            print(f"{Fore.RED}[x] One of the files not found!{Style.RESET_ALL}")
            return
            
        try:
            print(f"{Fore.CYAN}[*] Reading files...{Style.RESET_ALL}")
            
            with open(file1, 'r', encoding='utf-8', errors='ignore') as f:
                lines1 = set(line.strip().lower() for line in f.readlines() if line.strip())
                
            with open(file2, 'r', encoding='utf-8', errors='ignore') as f:
                lines2 = set(line.strip().lower() for line in f.readlines() if line.strip())
                
            common = lines1.intersection(lines2)
            only_in_file1 = lines1 - lines2
            only_in_file2 = lines2 - lines1
            
            print(f"\n{Fore.CYAN}┌─────────────────────────────────────────────────────────────────────────────────────┐")
            print(f"{Fore.CYAN}│                            COMPARISON RESULTS                                       │")
            print(f"{Fore.CYAN}├─────────────────────────────────────────────────────────────────────────────────────┤")
            print(f"{Fore.CYAN}│                                                                                     │")
            print(f"{Fore.CYAN}│  {Fore.WHITE}File 1 Lines:{Fore.CYAN}{len(lines1):>71} {Fore.CYAN}│")
            print(f"{Fore.CYAN}│  {Fore.WHITE}File 2 Lines:{Fore.CYAN}{len(lines2):>71} {Fore.CYAN}│")
            print(f"{Fore.CYAN}│  {Fore.GREEN}Common Lines:{Fore.CYAN}{len(common):>71} {Fore.CYAN}│")
            print(f"{Fore.CYAN}│  {Fore.YELLOW}Only in File 1:{Fore.CYAN}{len(only_in_file1):>69} {Fore.CYAN}│")
            print(f"{Fore.CYAN}│  {Fore.MAGENTA}Only in File 2:{Fore.CYAN}{len(only_in_file2):>69} {Fore.CYAN}│")
            print(f"{Fore.CYAN}│                                                                                     │")
            print(f"{Fore.CYAN}└─────────────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n")
            
            if common:
                output_file = "common_lines.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    for line in sorted(common):
                        f.write(line + '\n')
                print(f"{Fore.GREEN}[+] Common lines saved to: {output_file}{Style.RESET_ALL}")
            
            if only_in_file1:
                output_file = "only_in_file1.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    for line in sorted(only_in_file1):
                        f.write(line + '\n')
                print(f"{Fore.YELLOW}[+] Unique to file 1 saved to: {output_file}{Style.RESET_ALL}")
                
            if only_in_file2:
                output_file = "only_in_file2.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    for line in sorted(only_in_file2):
                        f.write(line + '\n')
                print(f"{Fore.MAGENTA}[+] Unique to file 2 saved to: {output_file}{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}[x] Error: {str(e)}{Style.RESET_ALL}")
            
    def show_statistics(self):
        self.clear_screen()
        self.print_banner()
        
        print(f"\n{Fore.CYAN}{'─'*85}")
        print(f"{Fore.CYAN}[*] Directory Statistics{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*85}{Style.RESET_ALL}\n")
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        print(f"{Fore.MAGENTA}[*] Opening directory dialog...{Style.RESET_ALL}")
        directory = filedialog.askdirectory(title="Select Directory to Analyze")
        
        root.destroy()
        
        if not directory:
            print(f"{Fore.RED}[x] No directory selected!{Style.RESET_ALL}")
            return
            
        if not os.path.exists(directory):
            print(f"{Fore.RED}[x] Directory not found!{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}[+] Analyzing directory: {directory}{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}[*] Scanning files...{Style.RESET_ALL}\n")
        
        total_files = 0
        total_lines = 0
        total_duplicates = 0
        file_stats = []
        
        for root_dir, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.txt', '.csv', '.log', '.json')):
                    file_path = os.path.join(root_dir, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            
                        original_count = len(lines)
                        unique_count = len(set(line.strip().lower() for line in lines if line.strip()))
                        duplicates = original_count - unique_count
                        
                        total_files += 1
                        total_lines += original_count
                        total_duplicates += duplicates
                        
                        file_stats.append({
                            'name': file,
                            'path': file_path,
                            'original': original_count,
                            'unique': unique_count,
                            'duplicates': duplicates
                        })
                        
                    except Exception as e:
                        continue
        
        print(f"{Fore.MAGENTA}┌─────────────────────────────────────────────────────────────────────────────────────┐")
        print(f"{Fore.MAGENTA}│                           OVERALL STATISTICS                                        │")
        print(f"{Fore.MAGENTA}├─────────────────────────────────────────────────────────────────────────────────────┤")
        print(f"{Fore.MAGENTA}│                                                                                     │")
        print(f"{Fore.MAGENTA}│  {Fore.WHITE}Total Files:{Fore.MAGENTA}{total_files:>72} {Fore.MAGENTA}│")
        print(f"{Fore.MAGENTA}│  {Fore.CYAN}Total Lines:{Fore.MAGENTA}{total_lines:>72} {Fore.MAGENTA}│")
        print(f"{Fore.MAGENTA}│  {Fore.RED}Total Duplicates:{Fore.MAGENTA}{total_duplicates:>67} {Fore.MAGENTA}│")
        dup_ratio = (total_duplicates/total_lines*100) if total_lines > 0 else 0
        print(f"{Fore.MAGENTA}│  {Fore.YELLOW}Duplicate Ratio:{Fore.MAGENTA}{dup_ratio:>64.2f}% {Fore.MAGENTA}│")
        print(f"{Fore.MAGENTA}│                                                                                     │")
        print(f"{Fore.MAGENTA}└─────────────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n")
        
        if file_stats:
            print(f"{Fore.YELLOW}Top 5 Files with Most Duplicates:{Style.RESET_ALL}\n")
            sorted_files = sorted(file_stats, key=lambda x: x['duplicates'], reverse=True)[:5]
            
            for i, stat in enumerate(sorted_files, 1):
                print(f"{Fore.WHITE}[{i}] {stat['name']}{Style.RESET_ALL}")
                print(f"    {Fore.CYAN}Original: {stat['original']:<10} Unique: {stat['unique']:<10} Duplicates: {stat['duplicates']}{Style.RESET_ALL}")
                print()
    
    def settings_menu(self):
        while True:
            self.clear_screen()
            self.print_banner()
            
            print(f"""{Fore.GREEN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   SETTINGS                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.LIGHTGREEN_EX}1{Fore.WHITE}]{Fore.GREEN} Case Sensitive                     {Fore.WHITE}Current: {str(self.case_sensitive):<35}{Fore.GREEN}│
│  {Fore.WHITE}[{Fore.LIGHTGREEN_EX}2{Fore.WHITE}]{Fore.GREEN} Preserve Order                     {Fore.WHITE}Current: {str(self.preserve_order):<35}{Fore.GREEN}│
│  {Fore.WHITE}[{Fore.LIGHTGREEN_EX}3{Fore.WHITE}]{Fore.GREEN} Create Backup                      {Fore.WHITE}Current: {str(self.create_backup):<35}{Fore.GREEN}│
│                                                                                     │
│  {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}]{Fore.RED} Back                                                                           {Fore.GREEN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
            
            choice = input(f"{Fore.GREEN}┌─[{Fore.WHITE}SELECT{Fore.GREEN}]\n└──> {Fore.WHITE}").strip()
            
            if choice == '1':
                self.case_sensitive = not self.case_sensitive
                print(f"\n{Fore.GREEN}[+] Case sensitive: {self.case_sensitive}{Style.RESET_ALL}")
                time.sleep(1)
            elif choice == '2':
                self.preserve_order = not self.preserve_order
                print(f"\n{Fore.GREEN}[+] Preserve order: {self.preserve_order}{Style.RESET_ALL}")
                time.sleep(1)
            elif choice == '3':
                self.create_backup = not self.create_backup
                print(f"\n{Fore.GREEN}[+] Create backup: {self.create_backup}{Style.RESET_ALL}")
                time.sleep(1)
            elif choice == '0':
                break
            else:
                print(f"\n{Fore.RED}[x] Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)
                
    def show_help(self):
        self.clear_screen()
        self.print_banner()
        
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                     HELP                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}FEATURES:{Fore.CYAN}                                                                          │
│  {Fore.WHITE}• Single file duplicate removal                                                    {Fore.CYAN}│
│  {Fore.WHITE}• Multiple file batch processing                                                   {Fore.CYAN}│
│  {Fore.WHITE}• Directory-based processing                                                       {Fore.CYAN}│
│  {Fore.WHITE}• File comparison and analysis                                                     {Fore.CYAN}│
│  {Fore.WHITE}• Detailed statistics                                                              {Fore.CYAN}│
│  {Fore.WHITE}• Automatic backup creation                                                        {Fore.CYAN}│
│                                                                                     │
│  {Fore.YELLOW}SUPPORTED FILE TYPES:{Fore.CYAN}                                                              │
│  {Fore.WHITE}• .txt (Text files)                                                                {Fore.CYAN}│
│  {Fore.WHITE}• .csv (Comma-separated values)                                                    {Fore.CYAN}│
│  {Fore.WHITE}• .log (Log files)                                                                 {Fore.CYAN}│
│  {Fore.WHITE}• .json (JSON files)                                                               {Fore.CYAN}│
│                                                                                     │
│  {Fore.GREEN}TIPS:{Fore.CYAN}                                                                              │
│  {Fore.WHITE}• Backups are automatically created before processing                              {Fore.CYAN}│
│  {Fore.WHITE}• Empty lines are automatically removed                                            {Fore.CYAN}│
│  {Fore.WHITE}• Use settings to customize behavior                                               {Fore.CYAN}│
│                                                                                     │
│  {Fore.RED}WARNINGS:{Fore.CYAN}                                                                          │
│  {Fore.WHITE}• Always keep backup files                                                         {Fore.CYAN}│
│  {Fore.WHITE}• Test on sample files first                                                       {Fore.CYAN}│
│  {Fore.WHITE}• Original files are modified                                                      {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
    def run(self):
        while True:
            self.print_banner()
            self.print_menu()
            
            choice = input(f"{Fore.MAGENTA}┌─[{Fore.WHITE}SELECT{Fore.MAGENTA}]\n└──> {Fore.WHITE}").strip()
            
            if choice == '1':
                self.clear_screen()
                self.print_banner()
                
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                
                print(f"\n{Fore.MAGENTA}[*] Opening file dialog...{Style.RESET_ALL}")
                file_path = filedialog.askopenfilename(
                    title="Select File to Remove Duplicates",
                    filetypes=[
                        ("Text files", "*.txt"), 
                        ("CSV files", "*.csv"), 
                        ("Log files", "*.log"), 
                        ("JSON files", "*.json"), 
                        ("All files", "*.*")
                    ]
                )
                
                root.destroy()
                
                if file_path:
                    self.remove_duplicates_from_file(file_path)
                else:
                    print(f"{Fore.RED}[x] No file selected!{Style.RESET_ALL}")
                    
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '2':
                self.process_multiple_files()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '3':
                self.process_directory()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '4':
                self.compare_files()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '5':
                self.show_statistics()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '6':
                self.settings_menu()
                
            elif choice == '7':
                self.show_help()
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '0':
                break
                
            else:
                print(f"\n{Fore.RED}[x] Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)


if __name__ == "__main__":
    try:
        app = DuplicateRemover(None)
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[x] Program terminated by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[x] Unexpected error: {e}{Style.RESET_ALL}")
        input("Press Enter to continue...")