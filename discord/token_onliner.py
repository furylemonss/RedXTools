import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Token Onliner")

class TokenOnliner:
    def __init__(self, parent):
        self.parent = parent
        self.active_threads = {}
        self.stop_flags = {}
        
    def keep_token_online_selenium(self, token):
        try:
            print(f"{Fore.CYAN}{'Processing token:'} {token[:20]}...")
            
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.common.exceptions import TimeoutException, WebDriverException
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--disable-dev-tools")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--silent")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            driver = webdriver.Chrome(options=chrome_options)
            
            try:
                driver.get("https://discord.com/app")
                
                WebDriverWait(driver, 10).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                
                login_script = f"""
                function login(token) {{
                    setInterval(() => {{
                        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${{token}}"`
                    }}, 50);
                    setTimeout(() => {{
                        location.reload();
                    }}, 2500);
                }}
                login("{token}");
                """
                
                driver.execute_script(login_script)
                print(f"{Fore.CYAN}{'Injecting token...'}")
                
                time.sleep(3)
                
                token_check = driver.execute_script("return localStorage.getItem('token');")
                if token_check:
                    print(f"{Fore.GREEN}{'Token successfully loaded:'} {token[:20]}...")
                    print(f"{Fore.CYAN}{'Changing status every 10 seconds...'}")
                    
                    statuses = ["online", "idle", "dnd"]
                    status_index = 0
                    
                    while not self.stop_flags.get(token, False):
                        try:
                            if driver.current_url != "https://discord.com/app":
                                driver.get("https://discord.com/app")
                                time.sleep(2)
                                
                            status_script = f"""
                            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.setItem('status', '"{statuses[status_index]}"');
                            """
                            driver.execute_script(status_script)
                            
                            print(f"{Fore.GREEN}[{token[:20]}] Status: {statuses[status_index]}")
                            
                            status_index = (status_index + 1) % len(statuses)
                            time.sleep(30)
                            
                        except Exception as e:
                            print(f"{Fore.RED}[{token[:20]}] Error changing status: {str(e)}")
                            time.sleep(5)
                            
                else:
                    print(f"{Fore.RED}[{token[:20]}] Failed to load token")
                    
            except Exception as e:
                print(f"{Fore.RED}[{token[:20]}] Selenium error: {str(e)}")
            finally:
                try:
                    driver.quit()
                except:
                    pass
                    
        except Exception as e:
            print(f"{Fore.RED}[{token[:20]}] Error: {str(e)}")
    
    def run(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"{Fore.CYAN}{'TOKEN ONLINER'}")
        print(f"{Fore.MAGENTA}{'='*30}")
        
        valid_tokens = []
        if os.path.exists(self.parent.valid_tokens_file):
            with open(self.parent.valid_tokens_file, 'r', encoding='utf-8') as f:
                valid_tokens = [line.strip() for line in f.readlines() if line.strip()]
        
        if not valid_tokens:
            print(f"{Fore.RED}{'Valid token file not found!'}")
            input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
            return
        
        print(f"{Fore.YELLOW}Available tokens: {len(valid_tokens)}")
        print(f"{Fore.YELLOW}1. Start all tokens online")
        print(f"{Fore.YELLOW}2. Start specific tokens")
        print(f"{Fore.YELLOW}3. Stop all tokens")
        print(f"{Fore.YELLOW}4. View active tokens")
        
        choice = input(f"\n{Fore.YELLOW}Choose option: ").strip()
        
        if choice == '1':
            self.start_all_tokens(valid_tokens)
        elif choice == '2':
            self.start_specific_tokens(valid_tokens)
        elif choice == '3':
            self.stop_all_tokens()
        elif choice == '4':
            self.view_active_tokens()
        else:
            print(f"{Fore.RED}Invalid choice")
            
        input(f"\n{Fore.YELLOW}{'Press Enter to continue...'}")
    
    def start_all_tokens(self, valid_tokens):
        print(f"{Fore.GREEN}Starting all tokens online...")
        
        for token in valid_tokens:
            if token not in self.active_threads:
                self.stop_flags[token] = False
                thread = threading.Thread(target=self.keep_token_online_selenium, args=(token,))
                thread.daemon = True
                thread.start()
                self.active_threads[token] = thread
                print(f"{Fore.GREEN}✓ Started: {token[:20]}...")
                
        print(f"{Fore.GREEN}All tokens started!")
    
    def start_specific_tokens(self, valid_tokens):
        print(f"\n{Fore.CYAN}Available tokens:")
        for i, token in enumerate(valid_tokens, 1):
            print(f"{Fore.WHITE}[{Fore.GREEN}{i}{Fore.WHITE}] {token[:20]}...")
            
        try:
            indices = input(f"\n{Fore.YELLOW}Enter token numbers (comma separated): ").strip()
            selected_indices = [int(x.strip()) - 1 for x in indices.split(',')]
            
            for index in selected_indices:
                if 0 <= index < len(valid_tokens):
                    token = valid_tokens[index]
                    if token not in self.active_threads:
                        self.stop_flags[token] = False
                        thread = threading.Thread(target=self.keep_token_online_selenium, args=(token,))
                        thread.daemon = True
                        thread.start()
                        self.active_threads[token] = thread
                        print(f"{Fore.GREEN}✓ Started: {token[:20]}...")
                    else:
                        print(f"{Fore.YELLOW}Already running: {token[:20]}...")
                        
        except ValueError:
            print(f"{Fore.RED}Invalid input")
    
    def stop_all_tokens(self):
        print(f"{Fore.YELLOW}Stopping all tokens...")
        
        for token in list(self.stop_flags.keys()):
            self.stop_flags[token] = True
            
        self.active_threads.clear()
        self.stop_flags.clear()
        
        print(f"{Fore.GREEN}All tokens stopped!")
    
    def view_active_tokens(self):
        if not self.active_threads:
            print(f"{Fore.YELLOW}No active tokens")
        else:
            print(f"\n{Fore.CYAN}Active tokens ({len(self.active_threads)}):")
            for token in self.active_threads.keys():
                print(f"{Fore.GREEN}✓ {token[:20]}...")
