import os
import time
import webbrowser
from colorama import Fore, Style
from tkinter import Tk, filedialog
import threading
import modules.rpc_manager as rpc_manager
rpc_manager.set_details("Discord: Account Login")

class AccountLogin:
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
        
    def run(self):
        self.parent.clear_screen()
        self.parent.print_banner()
        
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              ACCOUNT LOGIN                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}Login to Discord accounts using tokens                                             {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
        print(f"{Fore.YELLOW}Select token file...{Style.RESET_ALL}")
        token_file_path = self.select_token_file()
        
        if not token_file_path:
            print(f"\n{Fore.RED}[x] No file selected!{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
            
        if not os.path.exists(token_file_path):
            print(f"\n{Fore.RED}[x] Token file not found: {token_file_path}{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        print(f"{Fore.GREEN}[+] Selected file: {token_file_path}{Style.RESET_ALL}")
        
        valid_tokens = []
        with open(token_file_path, 'r', encoding='utf-8') as f:
            valid_tokens = [line.strip() for line in f.readlines() if line.strip()]
        
        if not valid_tokens:
            print(f"\n{Fore.RED}[x] Token file is empty!{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        
        print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           AVAILABLE TOKENS ({len(valid_tokens)})                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │{Style.RESET_ALL}""")
        
        for i, token in enumerate(valid_tokens, 1):
            print(f"{Fore.CYAN}│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}{i:>2}{Fore.WHITE}] {token[:50]:<78}{Fore.CYAN}│{Style.RESET_ALL}")
        
        print(f"""{Fore.CYAN}│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        
        try:
            choice = int(input(f"{Fore.CYAN}Select token number: {Fore.WHITE}")) - 1
            if 0 <= choice < len(valid_tokens):
                selected_token = valid_tokens[choice]
                
                print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              LOGIN OPTIONS                                          │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}1{Fore.WHITE}]{Fore.CYAN} Open in browser                       {Fore.WHITE}Login via browser                        {Fore.CYAN}│
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}2{Fore.WHITE}]{Fore.CYAN} Copy token to clipboard               {Fore.WHITE}Copy to clipboard                        {Fore.CYAN}│
│  {Fore.WHITE}[{Fore.LIGHTCYAN_EX}3{Fore.WHITE}]{Fore.CYAN} Show token info                       {Fore.WHITE}Display account details                  {Fore.CYAN}│
│                                                                                     │
│  {Fore.WHITE}[{Fore.RED}0{Fore.WHITE}]{Fore.RED} Back                                                                           {Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
                
                option = input(f"{Fore.CYAN}┌─[{Fore.WHITE}SELECT{Fore.CYAN}]\n└──> {Fore.WHITE}").strip()
                
                if option == '1':
                    self.open_in_browser(selected_token)
                elif option == '2':
                    self.copy_to_clipboard(selected_token)
                elif option == '3':
                    self.show_token_info(selected_token)
                elif option == '0':
                    return
                else:
                    print(f"\n{Fore.RED}[x] Invalid option{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}[x] Invalid token number{Style.RESET_ALL}")
                
        except ValueError:
            print(f"\n{Fore.RED}[x] Invalid input{Style.RESET_ALL}")
            
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def open_in_browser(self, token):
        print(f"\n{Fore.CYAN}[*] Opening Discord in browser...{Style.RESET_ALL}")
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Discord Login</title>
            <script>
                function login() {{
                    setInterval(() => {{
                        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"{token}"`
                    }}, 50);
                    setTimeout(() => {{
                        location.href = "https://discord.com/app";
                    }}, 2500);
                }}
                window.onload = login;
            </script>
        </head>
        <body>
            <h1>Logging into Discord...</h1>
            <p>You will be redirected automatically.</p>
        </body>
        </html>
        """
        
        temp_file = "temp_login.html"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        webbrowser.open(f"file://{os.path.abspath(temp_file)}")
        
        print(f"{Fore.GREEN}[+] Browser opened with token{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] The temp file will be automatically deleted after login{Style.RESET_ALL}")
        
        def cleanup():
            time.sleep(10)
            try:
                os.remove(temp_file)
            except:
                pass
        
        cleanup_thread = threading.Thread(target=cleanup)
        cleanup_thread.daemon = True
        cleanup_thread.start()
    
    def copy_to_clipboard(self, token):
        try:
            import pyperclip
            pyperclip.copy(token)
            print(f"\n{Fore.GREEN}[+] Token copied to clipboard{Style.RESET_ALL}")
        except ImportError:
            print(f"\n{Fore.YELLOW}[!] pyperclip module not found. Install with: pip install pyperclip{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Token: {token}{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.RED}[x] Failed to copy to clipboard: {str(e)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Token: {token}{Style.RESET_ALL}")
    
    def show_token_info(self, token):
        print(f"\n{Fore.CYAN}[*] Getting token information...{Style.RESET_ALL}")
        token_info = self.parent.get_token_info(token)
        
        if token_info:
            print(f"""{Fore.CYAN}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            TOKEN INFORMATION                                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  {Fore.WHITE}Username:        {Fore.LIGHTCYAN_EX}{token_info['username']}#{token_info['discriminator']:<55}{Fore.CYAN}│
│  {Fore.WHITE}User ID:         {Fore.LIGHTCYAN_EX}{token_info['user_id']:<66}{Fore.CYAN}│
│  {Fore.WHITE}Email:           {Fore.LIGHTCYAN_EX}{token_info['email']:<66}{Fore.CYAN}│
│  {Fore.WHITE}Verified:        {(Fore.GREEN + 'Yes' if token_info['verified'] else Fore.RED + 'No'):<72}{Fore.CYAN}│
│  {Fore.WHITE}2FA Enabled:     {(Fore.GREEN + 'Yes' if token_info['mfa_enabled'] else Fore.RED + 'No'):<72}{Fore.CYAN}│
│  {Fore.WHITE}Nitro:           {(Fore.GREEN + 'Yes' if token_info['has_nitro'] else Fore.RED + 'No'):<72}{Fore.CYAN}│
│  {Fore.WHITE}Badges:          {Fore.LIGHTCYAN_EX}{', '.join(token_info['badges']):<66}{Fore.CYAN}│
│  {Fore.WHITE}Created:         {Fore.LIGHTCYAN_EX}{token_info['creation_date']:<66}{Fore.CYAN}│
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
{Style.RESET_ALL}""")
        else:
            print(f"\n{Fore.RED}[x] Invalid token or failed to get information{Style.RESET_ALL}")