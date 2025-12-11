import requests
import logging
from datetime import datetime
import yaml
import os
import sys
import deposit_api

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
class Backend:
    def __init__(self,credentail:dict):
        self.credential=credentail
        self.token=self.get_token()

    def get_token(self):
        login_url="http://sit-admin2.tcg.com/tac/api/login/password"
        payload={
            "operatorName": self.credential['operatorName'],
            "password": self.credential['password']
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "http://sit-admin2.tcg.com",
            "Referer": "http://sit-admin2.tcg.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "environment": "",
            "language": "zh_CN",
            "noErrorNotice": "true",
            "platform": ""
        }
        
        cookies = {
            "language": "zh_CN"
        }
        requests_data=requests.post(login_url,json=payload,headers=headers,cookies=cookies,verify=False)
        token_data=requests_data.json()
        self.token=token_data.get("token")
        return self.token


    def Deposit_API(self,player:str,MerchantCode:str,deposit_amount:int):
        
        API_URL2="http://sit-admin2.tcg.com/mcs_console/api/deposit/createDeposit"  
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": self.token,
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Language": "zh_CN",
            "Merchant": str(MerchantCode),
            "MerchantCode": str(MerchantCode),
            "Origin": "http://sit-admin2.tcg.com",
            "Referer": "http://sit-admin2.tcg.com/20000",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "environment": "TCG3",
            "notPending": "true",
            "platform": "TCG"
        }
        payload={
            "merchantCode": MerchantCode,
            "username": player,
            "depositType": 22,
            "bankAcctId": 28886,
            "requestDateString":start_time,
            "requestAmount": deposit_amount,
            "customerBankCharge": 0,
            "bankCharge": ""
        }
        cookies = {
            "language": "zh_CN"
        }
        try:
            response=requests.post(API_URL2, headers=headers, cookies=cookies, json=payload,verify=False)
            response.raise_for_status()

            response_data=response.json()
            if response_data.get("success"):
                logging.info("充值成功")
            else:
                logging.error("充值失敗")
           
                
        except Exception as e:
            logging.error(f"狀態碼: {response.status_code},{e}")


    def procedure(self,merchantCode):
        try:
            current_dir=os.path.dirname(__file__)
            yaml_path=os.path.join(current_dir,"config_poetry.yaml")
            with open(yaml_path,"r",encoding="utf-8") as f:
                config=yaml.safe_load(f)
            testing_account=config.get("testing_account")
            
            for username, deposit_info in testing_account.items():
                first_amount=deposit_info.get("first_depost")
                second_amount=deposit_info.get("second_depost")
                third_amount=deposit_info.get("third_depost")
                four_amount=deposit_info.get("four_depost")
                five_amount=deposit_info.get("five_depost")
                if first_amount:
                    self.Deposit_API(username,merchantCode,first_amount)
                   
                if second_amount:
                    self.Deposit_API(username,merchantCode,second_amount)
                    
                if third_amount:
                    self.Deposit_API(username,merchantCode,third_amount)
                    
                if four_amount:
                    self.Deposit_API(username,merchantCode,four_amount)
                    
                if five_amount:
                    self.Deposit_API(username,merchantCode,five_amount)
                    

            deposit_api.batch_approve()

        except Exception as e:
            logging.error(e)
        except KeyboardInterrupt:
            print("退出程式")
            sys.exit()

def main_batch():
        merchantCode="gi8viet"
        credential = {
        "operatorName": "carrine03",
        "password": "Test@1234"
        }
        try:
            b_end=Backend(credential)
            if b_end.token:
                b_end.procedure(merchantCode)

        except Exception as e:
            logging.error(e)
        
main_batch()
   