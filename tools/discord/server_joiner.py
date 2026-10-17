import os
import time
import json
import websocket
import jwt
import httpx
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore
import requests
from tkinter import Tk, filedialog

import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Server Joiner")

class ServerJoiner:
    def __init__(self, parent):
        self.parent = parent
        
    def select_token_file(self):
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        file_path = filedialog.askopenfilename(
            title="Select Token File",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        root.destroy()
        return file_path
        
    def extract_invite_code(self, invite_input):
        if "discord.gg/" in invite_input:
            return invite_input.split("discord.gg/")[-1].split("?")[0]
        elif "discord.com/invite/" in invite_input:
            return invite_input.split("discord.com/invite/")[-1].split("?")[0]
        else:
            return invite_input.split("?")[0]
    
    def get_session_id(self, token):
        try:
            print(f"{Fore.YELLOW}⚠ IMPORTANT: Discord desktop application must be CLOSED!")
            print(f"{Fore.CYAN}WebSocket connection establishing...")
            
            ws = websocket.WebSocket()
            ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
            x = json.loads(ws.recv())
            auth = {
                "op": 2,
                "d": {
                    "token": token,
                    "properties": {
                        "$os": "windows",
                    },
                }
            }
            ws.send(json.dumps(auth))
            res = json.loads(ws.recv())
            ws.close()
            return res["d"]["session_id"]
        except Exception as e:
            print(f"{Fore.RED}Session ID could not be retrieved: {str(e)}")
            print(f"{Fore.YELLOW}💡 Solution: Close Discord desktop application and try again!")
            return None
    
    def make_jwt(self, guild_id, channel_id):
        header = {
            "location": "Invite Button Embed",
            "location_guild_id": None,
            "location_channel_id": channel_id,
            "location_channel_type": 1,
        }
        encoded_header = jwt.encode(header, key=None, algorithm='none')
        encoded_header = encoded_header.split(".")[1]
        return encoded_header
    
    def get_fingerprint(self, proxy=None):
        try:
            if proxy:
                session = httpx.Client(proxies=f'http://{proxy}')
            else:
                session = httpx.Client()

            headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Host": "discord.com",
                "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            }

            resp2 = session.get('https://discord.com/', headers=headers)
            coo = resp2.cookies
            cookies = {
                '__dcfduid': coo.get('__dcfduid'),
                '__sdcfduid': coo.get('__sdcfduid'),
                '__cfruid': coo.get('__cfruid'),
                'locale': 'en-US',
            }
            session.close()
            return cookies
        except Exception as e:
            print(f"{Fore.RED}Fingerprint could not be retrieved: {str(e)}")
            return {}
    
    def solve_captcha(self, rqdata, proxy=None, token=None, invite_code=None):
        try:
            print(f"{Fore.YELLOW}⚠ Captcha detected!")
            return self.login_with_requests(token, invite_code, proxy)
                
        except Exception as e:
            print(f"{Fore.RED}Captcha solving error: {str(e)}")
            return None
    
    def login_with_requests(self, token, invite_code, proxy=None):
        try:
            print(f"{Fore.CYAN}Token login with requests...")
            
            session = requests.Session()
            
            if proxy:
                session.proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            print(f"{Fore.YELLOW}Connecting to Discord...")
            response = session.get('https://discord.com/app', headers=headers)
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}✓ Connected to Discord!")
                
                print(f"{Fore.YELLOW}Logging in with token...")
                
                auth_headers = headers.copy()
                auth_headers['Authorization'] = token
                auth_headers['Content-Type'] = 'application/json'
                
                user_response = session.get('https://discord.com/api/v9/users/@me', headers=auth_headers)
                
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    username = user_data.get('username', 'Unknown')
                    discriminator = user_data.get('discriminator', '0000')
                    print(f"{Fore.GREEN}✓ Token valid! Logged in account: {username}#{discriminator}")
                    
                    if invite_code:
                        print(f"{Fore.CYAN}Auto joining server...")
                        
                        invite_response = session.get(f"https://discord.com/api/v9/invites/{invite_code}?inputValue={invite_code}&with_counts=true&with_expiration=true", headers=headers)
                        
                        if invite_response.status_code == 200:
                            invite_data = invite_response.json()
                            guild_name = invite_data.get('guild', {}).get('name', 'Unknown Server')
                            print(f"{Fore.GREEN}✓ Server found: {guild_name}")
                            
                            session_id = self.get_session_id(token)
                            if session_id:
                                print(f"{Fore.CYAN}Session ID received: {session_id[:20]}...")
                                
                                guild_id = invite_data.get('guild', {}).get('id')
                                channel_id = invite_data.get('channel', {}).get('id')
                                jwt_token = self.make_jwt(guild_id, channel_id)
                                
                                cookies = self.get_fingerprint(proxy)
                                
                                join_headers = {
                                    "Authorization": token,
                                    "Content-Type": "application/json",
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                                    "Accept": "*/*",
                                    "Accept-Language": "en-US,en;q=0.9",
                                    "Accept-Encoding": "gzip, deflate, br",
                                    "Origin": "https://discord.com",
                                    "Referer": "https://discord.com/",
                                    "X-Context-Properties": jwt_token,
                                }
                                
                                if cookies:
                                    cookie_string = '; '.join([f"{k}={v}" for k, v in cookies.items() if v is not None])
                                    if cookie_string:
                                        join_headers["Cookie"] = cookie_string
                                
                                join_data = {"session_id": session_id}
                                join_response = session.post(f"https://discord.com/api/v9/invites/{invite_code}", 
                                                           headers=join_headers, json=join_data)
                                
                                if join_response.status_code == 200:
                                    print(f"{Fore.GREEN}✓ Successfully joined server: {guild_name}")
                                    return "success"
                                elif "captcha_rqdata" in join_response.text:
                                    print(f"{Fore.YELLOW}⚠ Captcha required, opening in browser...")
                                    invite_url = f"https://discord.com/invite/{invite_code}"
                                    webbrowser.open(invite_url)
                                    
                                    user_input = input(f"{Fore.CYAN}Did you solve the captcha? (y/n): ").strip().lower()
                                    if user_input == 'y':
                                        print(f"{Fore.GREEN}✓ Server join completed!")
                                        return "success"
                                    else:
                                        return "pending"
                                elif join_response.status_code == 401:
                                    print(f"{Fore.RED}✗ 401 Unauthorized - Token invalid or unauthorized!")
                                    print(f"{Fore.YELLOW}Token may not have permission to join server.")
                                    return None
                                elif join_response.status_code == 403:
                                    print(f"{Fore.RED}✗ 403 Forbidden - Access denied!")
                                    print(f"{Fore.YELLOW}Token may not be able to join this server.")
                                    return None
                                elif join_response.status_code == 429:
                                    print(f"{Fore.YELLOW}⚠ 429 Rate Limited - Too many requests!")
                                    return None
                                else:
                                    print(f"{Fore.RED}✗ Failed to join server: {join_response.status_code}")
                                    try:
                                        error_data = join_response.json()
                                        if 'message' in error_data:
                                            print(f"{Fore.RED}Error message: {error_data['message']}")
                                    except:
                                        pass
                                    return None
                            else:
                                print(f"{Fore.RED}✗ Session ID not received!")
                                return None
                        else:
                            print(f"{Fore.RED}✗ Server invite invalid: {invite_response.status_code}")
                            return None
                    else:
                        print(f"{Fore.RED}✗ Invite code not found!")
                        return None
                else:
                    print(f"{Fore.RED}✗ Token invalid! Error: {user_response.status_code}")
                    return None
            else:
                print(f"{Fore.RED}✗ Could not connect to Discord! Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}✗ Requests login error: {str(e)}")
            return None
    
    def join_server_with_token(self, token, invite_code, current, total):
        try:
            proxy = None
            if self.parent.proxy_list:
                proxy = self.parent.get_random_proxy()
            
            if proxy:
                session = httpx.Client(proxies=f'http://{proxy}')
            else:
                session = httpx.Client()
            
            get = session.get(f"https://discord.com/api/v9/invites/{invite_code}?inputValue={invite_code}&with_counts=true&with_expiration=true")
            
            if get.status_code != 200:
                print(f"{Fore.RED}[{current}/{total}] ✗ Invalid invite code {token[:20]}...")
                session.close()
                return False
            
            try:
                data = get.json()
                guild = data["guild"]["id"]
                channel = data["channel"]["id"]
            except json.JSONDecodeError as e:
                print(f"{Fore.RED}[{current}/{total}] ✗ JSON error {token[:20]}...")
                session.close()
                return False
            
            session_id = self.get_session_id(token)
            if not session_id:
                print(f"{Fore.RED}[{current}/{total}] ✗ Session ID not received: {token[:20]}...")
                session.close()
                return False
            
            jwt_token = self.make_jwt(guild, channel)
            
            cookies = self.get_fingerprint(proxy)
            
            headers = {
                "authority": "discord.com",
                "method": "POST",
                "path": f"/api/v9/invites/{invite_code}",
                "scheme": "https",
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": token,
                "Content-Type": "application/json",
                "Cookie": '; '.join([f"{k}={v}" for k, v in cookies.items() if v is not None]),
                "Origin": "https://discord.com",
                "Priority": "u=1, i",
                "Referer": "https://discord.com/channels/@me/1239540925538107463",
                "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "X-Context-Properties": jwt_token,
                "X-Debug-Options": "bugReporterEnabled",
                "X-Discord-Locale": "en-GB",
                "X-Discord-Timezone": "Africa/Cairo",
                "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyNC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTI0LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2Rpc2NvcmQuY29tL2NoYW5uZWxzL0BtZSIsInJlZmVycmluZ19kb21haW4iOiJkaXNjb3JkLmNvbSIsInJlZmVycmVyX2N1cnJlbnQiOiIiLCJyZWZlcnJpbmdfZG9tYWluX2N1cnJlbnQiOiIiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyOTMzNjIsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGwsImRlc2lnbl9pZCI6MH0="
            }
            
            join_data = {"session_id": session_id}
            join = session.post(f"https://discord.com/api/v9/invites/{invite_code}", headers=headers, json=join_data)
            
            if join.status_code == 200:
                print(f"{Fore.GREEN}[{current}/{total}] ✓ Successfully joined: {token[:20]}...")
                with self.parent.lock:
                    self.parent.stats['joined'] += 1
                session.close()
                return True
            elif "captcha_rqdata" in join.text:
                print(f"{Fore.YELLOW}[{current}/{total}] ⚠ Captcha required: {token[:20]}...")
                try:
                    r = join.json()
                    rqdata = r['captcha_rqdata']
                    rqtoken = r['captcha_rqtoken']
                    
                    result = self.solve_captcha(rqdata, proxy, token, invite_code)
                    if result == "success":
                        print(f"{Fore.GREEN}[{current}/{total}] ✓ Captcha solved, successfully joined: {token[:20]}...")
                        with self.parent.lock:
                            self.parent.stats['joined'] += 1
                        session.close()
                        return True
                    else:
                        print(f"{Fore.RED}[{current}/{total}] ✗ Captcha not solved or join failed: {token[:20]}...")
                except Exception as e:
                    print(f"{Fore.RED}[{current}/{total}] ✗ Captcha process error: {token[:20]}... - {str(e)}")
                session.close()
                return False
            elif join.status_code == 429:
                print(f"{Fore.YELLOW}[{current}/{total}] ⚠ Rate limited: {token[:20]}...")
                session.close()
                return False
            else:
                print(f"{Fore.RED}[{current}/{total}] ✗ Error ({join.status_code}): {token[:20]}...")
                session.close()
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[{current}/{total}] ✗ Error: {token[:20]}... - {str(e)}")
            return False
        finally:
            try:
                session.close()
            except:
                pass
            
        time.sleep(self.parent.delay_between_requests)
        return False
    
    def run(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"{Fore.CYAN}SERVER JOINER")
        print(f"{Fore.MAGENTA}{'='*30}")
        
        print(f"{Fore.YELLOW}IMPORTANT: Discord desktop application must be CLOSED!")
        print(f"{Fore.YELLOW}WebSocket connection conflicts when Discord app is open.")
        print(f"{Fore.CYAN}Press Enter to continue...")
        input()
        
        print(f"{Fore.YELLOW}Select token file...")
        token_file_path = self.select_token_file()
        
        if not token_file_path:
            print(f"{Fore.RED}No file selected!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
            
        if not os.path.exists(token_file_path):
            print(f"{Fore.RED}Token file not found: {token_file_path}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
        
        print(f"{Fore.GREEN}✓ Selected file: {token_file_path}")
        
        valid_tokens = []
        with open(token_file_path, 'r', encoding='utf-8') as f:
            valid_tokens = [line.strip() for line in f.readlines() if line.strip()]
        
        if not valid_tokens:
            print(f"{Fore.RED}Token file is empty!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
            
        print(f"{Fore.GREEN}Example: https://discord.gg/example")
        invite_input = input(f"{Fore.YELLOW}Discord invite link or code: ").strip()
        
        if not invite_input:
            print(f"{Fore.RED}Invalid invite!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
            
        invite_code = self.extract_invite_code(invite_input)
        
        if not invite_code:
            print(f"{Fore.RED}Invalid invite format!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...")
            return
            
        threads = min(int(input(f"{Fore.YELLOW}Thread count (1-{self.parent.max_threads}): ") or "5"), self.parent.max_threads)
            
        print(f"\n{Fore.GREEN}Server joining starting...")
        print(f"{Fore.CYAN}Invite Code: {invite_code}")
        print(f"{Fore.CYAN}Valid Token Count: {len(valid_tokens)}")
        print(f"{Fore.CYAN}Thread Count: {threads}\n")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            
            for i, token in enumerate(valid_tokens):
                future = executor.submit(self.join_server_with_token, token, invite_code, i+1, len(valid_tokens))
                futures.append(future)
                
            joined_count = 0
            for future in futures:
                try:
                    if future.result():
                        joined_count += 1
                except Exception as e:
                    print(f"{Fore.RED}Error: {e}")
                    
        print(f"\n{Fore.GREEN}✓ Total {joined_count} tokens joined the server!")
        input(f"\n{Fore.YELLOW}Press Enter to continue...")