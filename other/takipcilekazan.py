import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from colorama import init, Fore, Style
import time
import os
import sys
from modules.settings import APP_AUTHOR

init(autoreset=True)

class TakipciLekazan:
    def __init__(self, main_app):
        self.main_app = main_app
        self.language = 'en'
        self.username = ""
        self.password = ""
        self.point = 0
        self.videoCount = 0
        self.driver = None
        
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        self.PROXY = None
        self.HEADLESS = True

    def get_text(self, key):
        texts = {
            'takipcilekazan_title': 'TAKIPCIKAZAN AUTOMATION',
            'username': 'Username',
            'password': 'Password',
            'username_required': 'Username is required!',
            'password_required': 'Password is required!',
            'press_ctrl_c_to_stop': 'Press Ctrl+C to stop',
            'video_watched': 'Video watched',
            'watched': 'watched',
            'total_points_earned': 'Total Points Earned',
            'points_from_this_video': 'Points from this video',
            'operations_terminated': 'Operations terminated',
            'error': 'Error',
            'login_elements_not_found': 'Login elements not found'
        }
        return texts.get(key, key)

    def print_banner(self):
        version = "1.1"
        author = APP_AUTHOR
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
{Fore.BLUE}║  {Fore.BLUE}║{Fore.GREEN}  RedX Tools v{version} {Fore.RESET}- {Fore.GREEN} Developer: {Fore.RED+author}                  {Fore.BLUE}║               {Fore.BLUE}    ║
{Fore.BLUE}║  {Fore.BLUE}╚═══════════════════════════════════════════════════════════╝  {Fore.BLUE}                 ║
{Fore.BLUE}║                                                                                  ║
{Fore.BLUE}╚══════════════════════════════════════════════════════════════════════════════════╝
"""
        print(banner)

    def setup_driver(self):
        options = uc.ChromeOptions()
        if self.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-first-run")
        options.add_argument("--no-service-autorun")
        options.add_argument("--password-store=basic")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        options.add_argument(f"--user-agent={self.USER_AGENT}")
        if self.PROXY:
            options.add_argument(f"--proxy-server={self.PROXY}")
        
        self.driver = uc.Chrome(options=options, headless=self.HEADLESS)
        return self.driver

    def login(self):
        self.driver.get("https://www.takipcilekazan.com/")
        self.driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[4]/a').click()
        time.sleep(2)

        xpath_user = '//*[@id="login_box"]/div/div/div/div[3]/form/div[1]/div/input'
        xpath_pass = '//*[@id="login_box"]/div/div/div/div[3]/form/div[2]/div/input'
        xpath_checkbox = '//*[@id="login_box"]/div/div/div/div[3]/form/div[3]/input'
        xpath_submit = '//*[@id="login_box"]/div/div/div/div[3]/form/button'

        attempts = 0
        max_attempts = 60

        while attempts < max_attempts:
            attempts += 1
            try:
                el_user = self.driver.find_element(By.XPATH, xpath_user)
                el_pass = self.driver.find_element(By.XPATH, xpath_pass)
                el_user.clear()
                el_user.send_keys(self.username)
                el_pass.clear()
                el_pass.send_keys(self.password)
                try:
                    chk = self.driver.find_element(By.XPATH, xpath_checkbox)
                    if not chk.is_selected():
                        chk.click()
                except Exception:
                    pass
                self.driver.find_element(By.XPATH, xpath_submit).click()
                break
            except Exception:
                time.sleep(1)
        else:
            raise RuntimeError(self.get_text('login_elements_not_found'))

    def get_credentials(self):
        print(f"{Fore.CYAN}{self.get_text('takipcilekazan_title')}")
        print(f"{Fore.MAGENTA}{'='*30}")
        print()
        
        if self.username == "":
            self.username = input(f"{Fore.YELLOW}[INPUT] {self.get_text('username')}: {Fore.WHITE}").strip()
            if not self.username:
                print(f"{Fore.RED}[-] {self.get_text('username_required')}")
                return False
        if self.password == "":            
            self.password = input(f"{Fore.YELLOW}[INPUT] {self.get_text('password')}: {Fore.WHITE}").strip()
            if not self.password:
                print(f"{Fore.RED}[-] {self.get_text('password_required')}")
                return False
            
        return True

    def show_main_menu(self):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}    MAIN MENU")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.WHITE}1. {Fore.GREEN}Youtube Watch As Long As You Watch")
        print(f"{Fore.WHITE}2. {Fore.GREEN}Youtube Automatic Video")
        print(f"{Fore.WHITE}3. {Fore.GREEN}Youtube Video 60 Seconds")
        print(f"{Fore.WHITE}4. {Fore.GREEN}Youtube Video 120 Seconds")
        print(f"{Fore.CYAN}{'='*60}")
        
        while True:
            try:
                choice = input(f"\n{Fore.YELLOW}[CHOICE] Which option do you want to use? (1-4): {Fore.WHITE}").strip()
                if choice in ['1', '2', '3', '4']:
                    return int(choice)
                else:
                    print(f"{Fore.RED}[-] Please select 1, 2, 3 or 4!")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}[-] Operation cancelled!")
                return None

    def run_youtube_video_60sn(self):
        try:
            while True:
                try:
                    print(f"{Fore.YELLOW}{'-'*50}")
                    print(f"{Fore.MAGENTA}{self.get_text('press_ctrl_c_to_stop')}")
                    print(f"{Fore.YELLOW}{'-'*50}")

                    self.driver.execute_script('window.location.href = "https://www.takipcilekazan.com/?page=module&md=youtube"')
                    time.sleep(1)
                    self.driver.find_element(By.CLASS_NAME, 'visit_button').click()
                    time.sleep(2)
                    self.driver.execute_script("""
                    if(window.player === undefined){
                        window.player = new YT.Player('ytPlayer', {
                            events: {
                                'onReady': function(event) { event.target.playVideo(); }
                            }
                        });
                    } else {
                        window.player.playVideo();
                    }
                    """)
                    onVideoPoint = ((self.driver.find_element(By.ID, "n_coins").text).split()[0])
                    self.videoCount+=1
                    if self.videoCount != 1:
                        self.point += int(onVideoPoint)
                    while True:
                        time.sleep(1)
                        try:
                            element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Başka bir video izlemek için burayı tıklayın')]")
                            if element.is_displayed():
                                element.click()
                                print(f"{Fore.CYAN}{self.get_text('video_watched')} #{self.videoCount} {Fore.GREEN}{self.get_text('watched')}{Fore.RESET}")
                                print(f"{Fore.YELLOW}{'-'*50}")
                                break
                        except NoSuchElementException:
                            pass
                        try:
                            played = int(self.driver.execute_script("return played;"))
                            os.system("cls")
                            print(f"{Fore.MAGENTA}{self.get_text('press_ctrl_c_to_stop')}")
                            print(f"{Fore.YELLOW}{'-'*50}")
                            print(f"{Fore.BLUE}{self.get_text('total_points_earned')}: {Fore.WHITE}{self.point}")
                            print(f"{Fore.CYAN}{self.videoCount}.video {Fore.MAGENTA}{played}{Fore.RESET}/{Fore.MAGENTA}60")
                            print(f"{Fore.YELLOW}{'-'*50}")
                        except Exception:
                            break
                        if played == 0:
                            start_time = time.time()
                            while time.time() - start_time < 3:
                                self.driver.find_element(By.XPATH, '//*[@id="blue-box"]/div[3]/a[1]').click()
                except KeyboardInterrupt:
                    print(f"{Fore.RED}{Style.BRIGHT}{self.get_text('operations_terminated')}")
                    break
        except Exception as e:
            print(f"{Fore.RED}{self.get_text('error')}: {e}")

    def run_youtube_video_120sn(self):
        try:
            while True:
                try:
                    print(f"{Fore.YELLOW}{'-'*50}")
                    print(f"{Fore.MAGENTA}{self.get_text('press_ctrl_c_to_stop')}")
                    print(f"{Fore.YELLOW}{'-'*50}")

                    self.driver.execute_script('window.location.href = "https://www.takipcilekazan.com/?page=module&md=ytozel"')
                    time.sleep(1)
                    self.driver.find_element(By.CLASS_NAME, 'visit_button').click()
                    time.sleep(2)
                    self.driver.execute_script("""
                    if(window.player === undefined){
                        window.player = new YT.Player('ytPlayer', {
                            events: {
                                'onReady': function(event) { event.target.playVideo(); }
                            }
                        });
                    } else {
                        window.player.playVideo();
                    }
                    """)
                    onVideoPoint = ((self.driver.find_element(By.ID, "n_coins").text).split()[0])
                    self.videoCount+=1
                    while True:
                        time.sleep(1)
                        try:
                            element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Başka bir video izlemek için burayı tıklayın')]")
                            if element.is_displayed():
                                element.click()
                                self.videoCount += 1
                                print(f"{Fore.CYAN}{self.get_text('video_watched')} #{self.videoCount} {Fore.GREEN}{self.get_text('watched')}{Fore.RESET}")
                                print(f"{Fore.YELLOW}{'-'*50}")
                                break
                        except NoSuchElementException:
                            pass
                        try:
                            played = int(self.driver.execute_script("return played;"))
                            if played >= 120:
                                self.point += int(onVideoPoint)
                            os.system("cls")
                            print(f"{Fore.MAGENTA}{self.get_text('press_ctrl_c_to_stop')}")
                            print(f"{Fore.YELLOW}{'-'*50}")
                            print(f"{Fore.BLUE}{self.get_text('total_points_earned')}: {Fore.WHITE}{self.point}")
                            print(f"{Fore.CYAN}{self.videoCount}.video {Fore.MAGENTA}{played}{Fore.RESET}/{Fore.MAGENTA}120")
                            print(f"{Fore.YELLOW}{'-'*50}")
                        except Exception:
                            break
                        if played == 0:
                            start_time = time.time()
                            while time.time() - start_time < 3:
                                self.driver.find_element(By.XPATH, '//*[@id="blue-box"]/div[3]/a[1]').click()
                except KeyboardInterrupt:
                    print(f"{Fore.RED}{Style.BRIGHT}{self.get_text('operations_terminated')}")
                    break
        except Exception as e:
            print(f"{Fore.RED}{self.get_text('error')}: {e}")

    def run_youtube_izledigin_kadar(self):
        try:
            while True:
                try:
                    print(f"{Fore.YELLOW}{'-'*50}")
                    print(f"{Fore.MAGENTA}{self.get_text('press_ctrl_c_to_stop')}")
                    print(f"{Fore.YELLOW}{'-'*50}")

                    self.driver.execute_script('window.location.href = "https://takipcilekazan.com/?page=module&md=ytizlediginkadar"')
                    time.sleep(1)
                    self.driver.find_element(By.CLASS_NAME, 'visit_button').click()
                    time.sleep(2)

                    self.driver.execute_script("""
                    if(window.player === undefined){
                        window.player = new YT.Player('ytPlayer', {
                            events: {
                                'onReady': function(event) { event.target.playVideo(); }
                            }
                        });
                    } else {
                        window.player.playVideo();
                    }
                    """)

                    video_point = 0
                    while True:
                        time.sleep(31.5)
                        if "skip" in self.driver.current_url:
                            self.videoCount += 1
                            totalPoint = self.point
                            print(f"{Fore.CYAN}{self.get_text('video_watched')} #{self.videoCount} {Fore.GREEN}{self.get_text('watched')}{Fore.RESET}")
                            print(f"{Fore.YELLOW}{'-'*50}")
                            break
                        else:
                            try:
                                get_point = self.driver.execute_script("return kazanilan;")
                                video_point = get_point
                                if self.videoCount == 0:
                                    self.point = video_point
                                else:
                                    self.point = totalPoint + video_point
                                os.system('cls')
                                print(f"{Fore.MAGENTA}{self.get_text('press_ctrl_c_to_stop')}")
                                print(f"{Fore.YELLOW}{'-'*50}")
                                print(f"{Fore.BLUE}{self.get_text('total_points_earned')}: {Fore.WHITE}{self.point}")
                                print(f"{Fore.CYAN}{self.get_text('points_from_this_video')}: {Fore.WHITE}{video_point}")
                                print(f"{Fore.YELLOW}{'-'*50}")
                            except Exception:
                                break
                except KeyboardInterrupt:
                    print(f"{Fore.RED}{Style.BRIGHT}{self.get_text('operations_terminated')}")
                    break
        except Exception as e:
            print(f"{Fore.RED}{self.get_text('error')}: {e}")

    def run_youtube_otomatik_video(self):
        try:
            while True:
                try:
                    print(f"{Fore.YELLOW}{'-'*50}")
                    print(f"{Fore.MAGENTA}{self.get_text('press_ctrl_c_to_stop')}")
                    print(f"{Fore.YELLOW}{'-'*50}")

                    self.driver.execute_script('window.location.href = "https://www.takipcilekazan.com/?page=module&md=surf"')
                    time.sleep(1)
                    self.driver.find_element(By.XPATH, '//*[@id="surfButton"]').click()
                    time.sleep(2)

                    self.driver.execute_script("""
                    if(window.player === undefined){
                        window.player = new YT.Player('ytPlayer', {
                            events: {
                                'onReady': function(event) { event.target.playVideo(); }
                            }
                        });
                    } else {
                        window.player.playVideo();
                    }
                    """)
                    already_counted = False
                    lastplayed = 0
                    self.videoCount+=1
                    while True:
                        time.sleep(1)
                        try:
                            played_value = self.driver.execute_script("return played;")
                            if played_value is not None:
                                played = int(played_value) + 1
                                if played == lastplayed:
                                    self.driver.execute_script("""
                                    if (window.YT && YT.Player) {
                                        if (!window.player) {
                                            window.player = new YT.Player('ytPlayer', {});
                                        }
                                        window.player.seekTo(0);
                                        window.player.playVideo();
                                    }
                                    """)
                                if played == 1:
                                    already_counted = False
                                
                                if played >= 180:
                                    played = 180
                                    if played == 180 and not already_counted:
                                        self.videoCount += 1
                                        self.point += 75
                                        already_counted = True
                                os.system("cls")
                                print(f"{Fore.MAGENTA}{self.get_text('press_ctrl_c_to_stop')}")
                                print(f"{Fore.YELLOW}{'-'*50}")
                                print(f"{Fore.BLUE}{self.get_text('total_points_earned')}: {Fore.WHITE}{self.point}")
                                print(f"{Fore.CYAN}{self.videoCount}.video: {Fore.BLUE}{str(played)}{Fore.RESET}/{Fore.BLUE}180")
                                print(f"{Fore.YELLOW}{'-'*50}")
                                lastplayed = played
                            else:
                                print(f"{Fore.RED}[DEBUG] played value returned None")
                                time.sleep(2)
                        except Exception as e:
                            print(f"{Fore.RED}[ERROR] {e}")
                            time.sleep(2)
                except KeyboardInterrupt:
                    print(f"{Fore.RED}{Style.BRIGHT}{self.get_text('operations_terminated')}")
                    break
        except Exception as e:
            print(f"{Fore.RED}{self.get_text('error')}: {e}")

    def run(self):
        try:
            self.main_app.clear_screen()
            self.print_banner()
            
            if not self.get_credentials():
                return
                
            self.setup_driver()
            self.login()
            
            choice = self.show_main_menu()
            if choice is None:
                return
                
            if choice == 1:
                print(f"\n{Fore.GREEN}[CHOICE] Youtube Watch As Long As You Watch module selected")
                self.run_youtube_izledigin_kadar()
            elif choice == 2:
                print(f"\n{Fore.GREEN}[CHOICE] Youtube Automatic Video module selected")
                self.run_youtube_otomatik_video()
            elif choice == 3:
                print(f"\n{Fore.GREEN}[CHOICE] Youtube Video 60 Seconds module selected")
                self.run_youtube_video_60sn()
            elif choice == 4:
                print(f"\n{Fore.GREEN}[CHOICE] Youtube Video 120 Seconds module selected")
                self.run_youtube_video_120sn()
                
        except Exception as e:
            print(f"{Fore.RED}{self.get_text('error')}: {e}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Fore.RESET}")
        finally:
            if self.driver:
                self.driver.quit()
