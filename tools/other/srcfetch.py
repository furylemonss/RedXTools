from bs4 import BeautifulSoup
from colorama import Fore, init
from os import system as sy, makedirs, path
from urllib.parse import urlparse, urljoin
import socket
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random

init(autoreset=True)

class SrcFetch:
    def __init__(self, main_app):
        self.main_app = main_app
        self.red = Fore.RED
        self.blue = Fore.BLUE
        self.magenta = Fore.MAGENTA
        self.cyan = Fore.CYAN
        self.green = Fore.GREEN
        self.reset = Fore.RESET
        
        self.USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]

    def print_banner(self):
        print("")

    def check_domain(self, url):
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            if domain.startswith("www."):
                domain = domain[4:]
            socket.gethostbyname(domain)
            return True
        except (socket.gaierror, Exception):
            return False

    def domain_handler(self, url):
        if not url.startswith("http"):
            url = "https://" + url
        return self.check_domain(url), url

    def get_valid_domain(self):
        site = input(self.blue + "Enter site URL: ")
        valid, full_url = self.domain_handler(site)
        if not valid:
            print(self.red + f"[-] Invalid domain! Please make sure it's in this format: {self.cyan}https://example.com")
            return None
        return full_url

    def safe_domain(self, url):
        parsed = urlparse(url)
        domain = parsed.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        return domain

    def build_headers(self, referer=None, user_agent=None):
        if user_agent is None:
            user_agent = random.choice(self.USER_AGENTS)
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        }
        if referer:
            headers["Referer"] = referer
        return headers

    def create_session(self, cookie_string=None, retries=3, backoff=0.3):
        session = requests.Session()
        retry = Retry(total=retries, backoff_factor=backoff, status_forcelist=(429,500,502,503,504), allowed_methods=frozenset(['GET','POST']))
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        if cookie_string:
            cookies = {}
            for pair in cookie_string.split(";"):
                if "=" in pair:
                    k,v = pair.split("=",1)
                    cookies[k.strip()] = v.strip()
            session.cookies.update(cookies)
        return session

    def session_get(self, session, url, referer=None, timeout=15):
        headers = self.build_headers(referer=referer)
        try:
            r = session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            print(self.red + f"[-] Request failed: {url} -> {e}")
            return None

    def fetchHTML(self, url, session):
        r = self.session_get(session, url, referer=None)
        if not r:
            return False
        soup = BeautifulSoup(r.text, "html.parser")
        domain_folder = self.safe_domain(url)
        makedirs(domain_folder, exist_ok=True)
        with open(f"{domain_folder}/index.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        return True

    def fetchCSS(self, url, session):
        r = self.session_get(session, url, referer=None)
        if not r:
            return False
        soup = BeautifulSoup(r.text, "html.parser")
        success = False
        for link_tag in soup.find_all("link", rel="stylesheet"):
            href = link_tag.get("href")
            if not href:
                continue
            if href.startswith("//"):
                full_url = "https:" + href
            elif href.startswith("/"):
                parsed = urlparse(url)
                full_url = f"{parsed.scheme}://{parsed.netloc}{href}"
            else:
                full_url = urljoin(url, href)
            css_resp = self.session_get(session, full_url, referer=url)
            if not css_resp:
                print(self.red + f"[-] CSS request failed: {full_url}")
                continue
            parsed_href = urlparse(full_url)
            local_path = path.join(parsed_href.netloc, parsed_href.path.lstrip("/"))
            local_dir = path.dirname(local_path)
            makedirs(local_dir, exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(css_resp.content)
            print(self.green + f"[+] Downloaded: {local_path}")
            success = True
        return success

    def run(self):
        try:
            self.main_app.clear_screen()
            self.print_banner()
            
            print(f"\n{self.magenta}{'='*60}")
            print(f"{Fore.WHITE}    WEBSITE SOURCE CODE DOWNLOADER")
            print(f"{self.magenta}{'='*60}")
            
            site = self.get_valid_domain()
            if site:
                print(self.green + f"[+] Domain verified: {site}")
                session = self.create_session(cookie_string=None)
                
                print(f"\n{self.cyan}[INFO] Downloading HTML file...")
                if self.fetchHTML(site, session):
                    print(self.green + f"[+] HTML downloaded: {site}")
                else:
                    print(self.red + f"[-] HTML download failed: {site}")
                
                print(f"\n{self.cyan}[INFO] Downloading CSS files...")
                if self.fetchCSS(site, session):
                    print(self.green + f"[+] CSS files downloaded: {site}")
                else:
                    print(self.red + f"[-] CSS files download failed: {site}")
                    
                print(f"\n{self.green}[+] Operation completed! Files saved to folder.")
            else:
                print(self.red + f"[-] Invalid domain!")
                
        except Exception as e:
            print(f"{self.red}[ERROR] {e}")
            
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Fore.RESET}")
