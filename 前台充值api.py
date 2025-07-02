import requests,logging,time
from datetime import datetime,timedelta
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
class Frontend:
    def __init__(self,credential:dict):
        self.session=requests.Session()
        self.username=''
        self.userid=''
        self.credential=credential
        self.token=None
        self.token_expire=None
        self.token=self.get_token_login(credential['username'],credential['password'])
        self.type=''
    def get_token_login(self, username, password):
        try:

            if self.token is not None and self.token_expire is not None and datetime.now()<self.token_expire:
                return self.token
            
            login_url='http://www.sit2.sit-gi8viet.com/wps/session/login/unsecure'
            
            headers = {
                'Content-Type': 'application/json',
                'Merchant': 'gi8viet',
            }
            login_data={
                'username':username,
                'password':password
            } 
            
            requests_data=self.session.post(login_url,json=login_data,headers=headers)
            print(requests_data.text)
            self.username = requests_data.json()['value']['userName']
            self.userid = requests_data.json()['value']['id']
            self.token=requests_data.json()['value']['token']

            self.token_expire=datetime.now()+timedelta(minutes=25)
            return self.token
        
        except requests.RequestException as e:
            logging.error(f"請求失敗{e}")
            return None
    def is_token_valid(self):
        
        return (self.token is not None and 
                self.token_expire is not None and 
                datetime.now() < self.token_expire)
    
        
    def deposit_QAD(self,username):
        success_fail=0
        success_count=0
        bank_types=["PAYID","WECHAT"]
        for bank_type in bank_types:
            if not self.is_token_valid():
                logging.info("token 過期, 重新登入")
                self.get_token_login(credential['username'],credential['password'])
            if self.token is None:
                return
            current_time=datetime.now()
            unit_time=str(int(current_time.timestamp()*1000))
            login_URL=f"http://www.sit-gi8viet.com/wps/relay/MCSFE_depositByQRImageUrl"

            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/json',
                'Merchant': 'gi8viet',
                "Authorization":self.token,
                'Connection': 'keep-alive',
                'Language': 'EN',
                'Origin': 'http://www.sit-gi8viet.com',
                'Referer': 'http://www.sit-gi8viet.com/',
                'ModuleId': 'DPSTBAS3',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',  
                'x-timestamp': unit_time     
            }
            payload={
                "targetUsername": username,
                "amount":500,
                "bankCode":"QADPAYID001",
                "bankType":bank_type, 
                "showQrImageOnly":1,
                "vendorId":21306,
                "mcsBankCode":"QADPAYID001",
                "token":self.token
            }
            cookies={
                'SHELL_deviceId': '8c5bdbd3-b2cd-b350-4c4e-5967bb9d7966',
            }
            
            response=self.session.post(login_URL,headers=headers,json=payload,cookies=cookies,verify=False)
            response_json=response.json()
            
            if response_json.get('success')==True:
                logging.info(f"成功充值 交易ID")
                success_count+=1
                
            else:
                logging.error(f"充值失敗")
                success_fail+=1
            time.sleep(1)
        logging.info(f"總共充值{success_count}筆")
        logging.info(f"總共失敗{success_fail}筆")
            
    def deposit_TBQR(self,username):
        bank_codes=["2600","2101","2284","5832","2280","2279","6101","0400"]
        bank_types=["TBQR","VA","THREE65PAY","PAYVALIDA","ABPAY","KPAY","KBZPAY","UN"]
        success_fail=0
        success_count=0
        for bank_code,bank_type in zip(bank_codes,bank_types):
                if not self.is_token_valid():
                    logging.info("token 過期, 重新登入")
                    self.get_token_login(credential['username'],credential['password'])
                if self.token is None:
                    return
                current_time=datetime.now()
                unit_time=str(int(current_time.timestamp()*1000))
                login_URL=f"http://www.sit-gi8viet.com/wps/relay/MCSFE_depositByQRImageUrl"

                headers={
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Content-Type': 'application/json',
                    'Merchant': 'gi8viet',
                    "Authorization":self.token,
                    'Connection': 'keep-alive',
                    'Language': 'EN',
                    'Origin': 'http://www.sit-gi8viet.com',
                    'Referer': 'http://www.sit-gi8viet.com/',
                    'ModuleId': 'DPSTBAS3',
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',  
                    'x-timestamp': unit_time     
                }
                payload={
                    "targetUsername": username,
                    "amount":500,
                    "bankCode":bank_code,
                    "bankType":bank_type,
                    "vendorId":28270,
                    "mcsBankCode":"TCG-106324 depositByLaunchUrl",
                    "token":self.token
                }
                cookies={
                    'SHELL_deviceId': '8c5bdbd3-b2cd-b350-4c4e-5967bb9d7966',
                }
                
                response=self.session.post(login_URL,headers=headers,json=payload,cookies=cookies,verify=False)
                response_json=response.json()
                
                if response_json.get('success')==True:
                    logging.info(f"成功充值 交易ID")
                    success_count+=1
                    
                else:
                    logging.error(f"充值失敗")
                    success_fail+=1
                time.sleep(0.5)
        logging.info(f"總共充值{success_count}筆")
        logging.info(f"總共失敗{success_fail}筆")
    def quick_deposit(self,username):
        success_fail=0
        success_count=0
        bank_types=["null"]
        bank_codes=["TCG-106324"]
        for bank_type, bank_code in zip(bank_types,bank_codes):
            if not self.is_token_valid():
                logging.info("token 過期, 重新登入")
                self.get_token_login(credential['username'],credential['password'])
            if self.token is None:
                return
            current_time=datetime.now()
            unit_time=str(int(current_time.timestamp()*1000))
            login_URL=f"http://www.sit-gi8viet.com/wps/relay/MCSFE_manualTransferByAccountName"

            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/json',
                'Merchant': 'gi8viet',
                "Authorization":self.token,
                'Connection': 'keep-alive',
                'Language': 'EN',
                'Origin': 'http://www.sit-gi8viet.com',
                'Referer': 'http://www.sit-gi8viet.com/',
                'ModuleId': 'DPSTBAS3',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',  
                'x-timestamp': unit_time     
            }
            payload={
                "targetUsername": username,
                "payeeName":"bbbb",
                "amount":500,
                "bankCode":bank_type,
                "vendorId":28166,
                "mcsBankCode":bank_code,
                "token":self.token
            }
            cookies={
                'SHELL_deviceId': '8c5bdbd3-b2cd-b350-4c4e-5967bb9d7966',
            }
            
            response=self.session.post(login_URL,headers=headers,json=payload,cookies=cookies,verify=False)
            response_json=response.json()
            
            if response_json.get('success')==True:
                logging.info(f"成功充值 交易ID")
                success_count+=1
                
            else:
                logging.error(f"充值失敗")
                success_fail+=1
            time.sleep(1)
        logging.info(f"總共充值{success_count}筆")
        logging.info(f"總共失敗{success_fail}筆")
    def depositbyURL(self,username):
        success_fail=0
        success_count=0
        bank_types=["WCFQR","ALIFQR","KAMI"]
        bank_codes=["TCG-106324 depositByQRImageUrl"]
        for bank_type, bank_code in zip(bank_types,bank_codes):
            if not self.is_token_valid():
                logging.info("token 過期, 重新登入")
                self.get_token_login(credential['username'],credential['password'])
            if self.token is None:
                return
            current_time=datetime.now()
            unit_time=str(int(current_time.timestamp()*1000))
            login_URL=f"http://www.sit-gi8viet.com/wps/relay/MCSFE_depositByQRImageUrl"

            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/json',
                'Merchant': 'gi8viet',
                "Authorization":self.token,
                'Connection': 'keep-alive',
                'Language': 'EN',
                'Origin': 'http://www.sit-gi8viet.com',
                'Referer': 'http://www.sit-gi8viet.com/',
                'ModuleId': 'DPSTBAS3',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',  
                'x-timestamp': unit_time     
            }
            payload={
                "targetUsername": username,
                "amount":500,
                "bankCode":bank_code,
                "bankType":bank_type,
                "vendorId":28268,
                "mcsBankCode":bank_code,
                "token":self.token
            }
            cookies={
                'SHELL_deviceId': '8c5bdbd3-b2cd-b350-4c4e-5967bb9d7966',
            }
            
            response=self.session.post(login_URL,headers=headers,json=payload,cookies=cookies,verify=False)
            response_json=response.json()
            
            if response_json.get('success')==True:
                logging.info(f"成功充值 交易ID")
                success_count+=1
                
            else:
                logging.error(f"充值失敗")
                success_fail+=1
            time.sleep(1)
        logging.info(f"總共充值{success_count}筆")
        logging.info(f"總共失敗{success_fail}筆")
    def BTC_deposit(self,username):
        success_fail=0
        success_count=0
        bank_types=["BTC","TRX"]
        bank_codes=["TCG-106324 depositVirtualWallet"]
        for bank_type, bank_code in zip(bank_types,bank_codes):
            if not self.is_token_valid():
                logging.info("token 過期, 重新登入")
                self.get_token_login(credential['username'],credential['password'])
            if self.token is None:
                return
            current_time=datetime.now()
            unit_time=str(int(current_time.timestamp()*1000))
            login_URL=f"http://www.sit-gi8viet.com/wps/relay/MCSFE_depositVirtualWallet"

            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/json',
                'Merchant': 'gi8viet',
                "Authorization":self.token,
                'Connection': 'keep-alive',
                'Language': 'EN',
                'Origin': 'http://www.sit-gi8viet.com',
                'Referer': 'http://www.sit-gi8viet.com/',
                'ModuleId': 'DPSTBAS3',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',  
                'x-timestamp': unit_time     
            }
            payload={
                "targetUsername": username,
                "amount":500,
                "bankType":bank_type, 
                "vendorId":28269,
                "bankCode":bank_code,
                "showQrImageOnly":1,
                "mcsBankCode":bank_code,
            }
            cookies={
                'SHELL_deviceId': '8c5bdbd3-b2cd-b350-4c4e-5967bb9d7966',
            }
            
            response=self.session.post(login_URL,headers=headers,json=payload,cookies=cookies,verify=False)
            response_json=response.json()
            
            if response_json.get('success')==True:
                logging.info(f"成功充值 交易ID")
                success_count+=1
                
            else:
                logging.error(f"充值失敗")
                success_fail+=1
            time.sleep(1)
        logging.info(f"總共充值{success_count}筆")
        logging.info(f"總共失敗{success_fail}筆")
    def mpesa_deposit(self,username):
        success_fail=0
        success_count=0
        bank_types=["MPESA"]
        bank_codes=["XXBangkokCentral"]
        for bank_type, bank_code in zip(bank_types,bank_codes):
            if not self.is_token_valid():
                logging.info("token 過期, 重新登入")
                self.get_token_login(credential['username'],credential['password'])
            if self.token is None:
                return
            current_time=datetime.now()
            unit_time=str(int(current_time.timestamp()*1000))
            login_URL=f"http://www.sit-gi8viet.com/wps/relay/MCSFE_depositByLaunchUrl"

            headers={
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/json',
                'Merchant': 'gi8viet',
                "Authorization":self.token,
                'Connection': 'keep-alive',
                'Language': 'EN',
                'Origin': 'http://www.sit-gi8viet.com',
                'Referer': 'http://www.sit-gi8viet.com/',
                'ModuleId': 'DPSTBAS3',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',  
                'x-timestamp': unit_time     
            }
            payload={
                "targetUsername": username,
                "amount":500,
                "bankCode":bank_code,
                "bankType":bank_type, 
                "vendorId":28206,
                "mcsBankCode":bank_code,
                "token":self.token,
            }
            cookies={
                'SHELL_deviceId': '8c5bdbd3-b2cd-b350-4c4e-5967bb9d7966',
            }
            
            response=self.session.post(login_URL,headers=headers,json=payload,cookies=cookies,verify=False)
            response_json=response.json()
            
            if response_json.get('success')==True:
                logging.info(f"成功充值 交易ID")
                success_count+=1
                
            else:
                logging.error(f"充值失敗")
                success_fail+=1
            time.sleep(1)
        logging.info(f"總共充值{success_count}筆")
        logging.info(f"總共失敗{success_fail}筆")
        
        
        
if __name__ == "__main__":
    while True:
        username = input("請輸入帳號：")
        password = "123qwe"
        #填入玩家帳號
        credential = {
            "username": username,
            "password": password
        }
        try:    
            frontend = Frontend(credential)
            if frontend.token:
                frontend.deposit_QAD(credential['username'])
                frontend.deposit_TBQR(credential['username'])
                frontend.quick_deposit(credential['username'])
                frontend.depositbyURL(credential['username'])
                frontend.BTC_deposit(credential['username'])
                frontend.mpesa_deposit(credential['username'])
                
            else:
                logging.error("登入失敗 無法取得Token")
        
        except Exception as e:
            logging.error(f"啟動時發生錯誤: {e}")

    