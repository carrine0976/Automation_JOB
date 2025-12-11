import yaml,os
import time
import requests,logging
from datetime import datetime
from openpyxl import Workbook
from itertools import cycle
import threading,copy
import concurrent.futures
import pytest
from itertools import product

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class B_end:
    def header(self):
        return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": self.token_data,
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Language": "zh_CN",
        "Merchant": "gi8viet",
        "Origin": "http://sit-admin2.tcg.com",
        "Referer": "http://sit-admin2.tcg.com/24785",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "environment": "TCG3",
        "merchantCode": "gi8viet",
        "platform": "TCG"
        }
    def __init__(self,credential:dict):
        self.session=requests.Session()
        self.username=''
        self.password=''
        self.token=self.get_token(credential['operatorName'],credential['password'])
        self.credential=credential
        self.token_data=self.token
        self.record_data_list=[]
        self.claimid_list=[]
        self.success_count=0
        self.claimid=''
        self.lock=threading.Lock()
    def get_token(self,operatorName,password):
        login_url="http://sit-admin2.tcg.com/tac/api/login/password"
        payload={
                "operatorName": operatorName,
                "password": password
            }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Merchant": "gi8viet",
            "MerchantCode": "gi8viet",
            "Origin": "http://sit-admin2.tcg.com",
            "Referer": "http://sit-admin2.tcg.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "environment": "",
            "language": "zh_CN",
            "noErrorNotice": "true",
            "platform": "",
            "Tac-Trace-Id":"&kZEwhHNN!Pe(Qj_"
        }
        
        cookies = {
            "language": "zh_CN",
            "JSESSIONID":"wK3EQfljeUHXxYAN8uKQcvkpKBg1WM4PaVshMx7TpsBoHDtAk4c_!-1653539373"
        }
        
        requests_data=requests.post(login_url,json=payload,headers=headers,cookies=cookies,verify=False)
        token_data=requests_data.json()
        token=token_data.get("token")
        logging.info(f"登入API回傳: {token}")
        return token

    def create_bonus(self,player:str,bonusAmount:int,bonusPointAmount:int,ticketId:int,ticketQuantity:int,prmotion_id:int):
        API_URL = "http://sit-admin2.tcg.com/tac/api/relay/post/mcs-manual-promotion-addManualPromotionClaim" 
        payload = {
        "merchantCode": "gi8viet",
        "customerName": player,
        "bonusAmount": bonusAmount,
        "bonusPointAmount": bonusPointAmount,
        "promotionId": prmotion_id,
        "toReqAmount": 0,
        "ticketId": ticketId,
        "ticketQuantity": ticketQuantity
    }

        headers = self.header()
        cookies = {
            "language": "zh_CN"
        }
        
        response = requests.post(API_URL, json=payload, headers=headers, cookies=cookies, verify=False)
        
        
        response_data = response.json()
        
        if response_data.get("success") :
            logging.info(f"手動紅利發放成功, 玩家帳號{player} ")
            self.success_count+=1
            return True
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.error(f"手動紅利發放失敗: {error_msg}")
            return False
                
        
    def Search_Customer_bonus(self):
        self.claimid_list.clear()
        API_URL = "http://sit-admin2.tcg.com/tac/api/relay/get/mcs-manualPromotion-search" 
        start_time = datetime.now().strftime("%Y-%m-%d 00:00:00")
        end_time = datetime.now().strftime("%Y-%m-%d 23:59:59")
        params = {
        "merchantCode": "gi8viet",
        "status": "P",
        "searchDateMode": "issuedDateSearch",
        "startTime": start_time,
        "endTime": end_time,
        "pageSize": 10,
        "pageNo": 1,
    }

        headers = self.header()
        
        
        result_list=[]
        response = requests.get(API_URL, params=params, headers=headers, verify=False)
        response.raise_for_status()
        
        response_data = response.json()
        
        if response_data.get("success"):
            customer_list=response_data.get("value",[])
            
            if not customer_list:
                logging.error("回應中找不到 customerlist")
            for customer_info in customer_list:
                CustomerID=customer_info.get("customerId")
                claimid=customer_info.get("id")
                promotionType=customer_info.get("promotionType")
                promotionId=customer_info.get("promotionId")
                if CustomerID and claimid:
                    claim_dict={
                        "promoClaimId": claimid,
                        "promotionType": promotionType
                    }
                    self.claimid_list.append(claim_dict)
            return self.claimid_list
        else:
            logging.error("回應中找不到 customerId 或 claimid")
            return None, None ,None
        
            
        
    
    def Confirm_Customer_bonus(self):
        API_URL = "http://sit-admin2.tcg.com/tac/api/relay/post/mcs-manual-promotion-batchApproveRejectManualPromotion" 
        payload = {
            "status": "I",
            "promotionClaims": self.claimid_list
        }

        headers = self.header()
        
        expect_result=True
        response = requests.post(API_URL, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        logging.info(self.claimid_list)
        response_data = response.json()
        if response_data.get("success") :
            success=response_data.get("success")
            value=int(response_data.get("value"))
            assert value == 0 
            assert expect_result==success
            logging.info("批量審核活動紅利成功 ")
            return True
        else:
            error_msg = response_data.get("value")
            logging.error(f"未審核成功 value: {error_msg}")
            return False
                
        
    
    def process_create(self,account,promo_id,ticket_id):
        
        if self.create_bonus(
            player=account,
            bonusAmount=10,
            bonusPointAmount=10,
            ticketId=ticket_id,
            ticketQuantity=1,
            prmotion_id=promo_id
            ):
            self.Search_Customer_bonus()
        
    def process_confirm(self):
        
        self.Confirm_Customer_bonus()
        
@pytest.fixture(scope='session')
def backend():
    credential = {
        "operatorName": "parisv01",
        "password": "Aa123456@"
    }
    client=B_end(credential)
    
    return client

def merchantCode():
    return "gi8viet"


def pytest_generate_tests(metafunc):
    current_dir=os.path.dirname(__file__)
    yaml_path=os.path.join(current_dir,"config.yaml")
    with open(yaml_path,"r",encoding="utf-8") as f:
        config=yaml.safe_load(f)
        
    params_needed={"account","promo_id","ticket_id"}
    if params_needed.issubset(set(metafunc.fixturenames)):
        prmotion_id_multiple=config.get("promtion_ids",[])
        ticket_id=config.get("ticket_id")
        testing_account=config.get("testing_account")
        test_params=[]
        for account,promo_id,ticket_id in product(testing_account,prmotion_id_multiple,ticket_id):
            test_params.append(
                pytest.param(account,promo_id,ticket_id)
                )
        metafunc.parametrize("account,promo_id,ticket_id",test_params)

def test_process_procedure(backend,account,promo_id,ticket_id):
    backend.process_create(account,promo_id,ticket_id)

def test_confirm(backend,account,promo_id,ticket_id):
    backend.process_confirm(account,promo_id,ticket_id)
        
    
        
    
    