import yaml,os
import time,random
import requests,logging
from datetime import datetime
from openpyxl import Workbook

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
class B_end:
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
        
        API_URL = "http://sit-admin2.tcg.com/tac/api/relay/post/mcs-manual-promotion-addManualPromotionClaim?" 
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

        headers = {
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
        cookies = {
            "language": "zh_CN"
        }
        try:
            response = requests.post(API_URL, json=payload, headers=headers, cookies=cookies, verify=False)
            
            
            response_data = response.json()
            
            if response_data.get("success") == True:
                logging.info(f"手動紅利發放成功 ")
                return True
            else:
                error_msg = response_data.get("message", "未知錯誤")
                logging.error(f"手動紅利發放失敗: {error_msg}")
                return False
                
        except requests.RequestException as e:
            logging.error(f"HTTP錯誤 {e}")
            return False
        except ValueError as e:
            logging.error(f"JSON解析錯誤: {e}")
            return False
        except Exception as e:
            logging.error(f"其他錯誤: {e}")
            return False
    def Search_Customer_bonus(self,player:str):
      
        API_URL = "http://sit-admin2.tcg.com/tac/api/relay/get/mcs-manualPromotion-search" 
        start_time = datetime.now().strftime("%Y-%m-%d 00:00:00")
        end_time = datetime.now().strftime("%Y-%m-%d 23:59:59")
        payload = {
        "merchantCode": "gi8viet",
        "status": "P",
        "customerName":player,
        "searchDateMode": "issuedDateSearch",
        "startTime": start_time,
        "endTime": end_time,
        "pageSize": 10,
        "pageNo": 1
    }

        headers = {
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
        cookies = {
            "language": "zh_CN"
        }
        try:
            response = requests.get(API_URL, params=payload, headers=headers, cookies=cookies, verify=False)
            response.raise_for_status()
            
            response_data = response.json()
            
            if response_data.get("success") == True:
                customer_list=response_data.get("value",[])
                
                if not customer_list:
                    logging.error("回應中找不到 customerlist")

                customer_info=customer_list[0]
                CustomerID=customer_info.get("customerId")
                claimid=customer_info.get("id")
                promotion_type=customer_info.get("promotionType")
        
                if CustomerID and claimid:
                    return CustomerID, claimid,promotion_type
                
            else:
                    logging.error("回應中找不到 customerId 或 claimid")
                    return None, None 
            
                
        except requests.RequestException as e:
            logging.error(f"HTTP錯誤 {e}")
            return None, None
        except ValueError as e:
            logging.error(f"JSON解析錯誤: {e}")
            return None, None
        except Exception as e:
            logging.error(f"其他錯誤: {e}")
            return None, None
    
    def Confirm_Customer_bonus(self):
    
        API_URL = f"http://sit-admin2.tcg.com/tac/api/relay/post/mcs-manual-promotion-batchApproveRejectManualPromotion" 
        payload = {
            "status": "I",
            "promotionClaims": self.claimid_list
        }

        headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": self.token_data,
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
        
        try:
            response = requests.post(API_URL, json=payload, headers=headers, verify=False)
            response.raise_for_status()
            logging.info(self.claimid_list)
            response_data = response.json()
            if response_data.get("success") == True:
                logging.info(f"批量審核活動紅利成功 ")
                return True
            else:
                error_msg = response_data.get("value")
                logging.error(f"未審核成功 value: {error_msg}")
                return False
                
        except requests.RequestException as e:
            logging.error(f"HTTP錯誤 {e}")
            return False
        except ValueError as e:
            logging.error(f"JSON解析錯誤: {e}")
            return False
        except Exception as e:
            logging.error(f"其他錯誤: {e}")
            return False
    def process_procedure(self,username:str):
        
        CREATE_BONUS_PLAYER=username
        bonusAmount=1
        bonusPointAmount=2        
        current_dir=os.path.dirname(__file__)
        yaml_path=os.path.join(current_dir,"config.yaml")
        with open(yaml_path,"r",encoding="utf-8") as f:
            config=yaml.safe_load(f)
        ticket_list=config.get("ticket_id")
        ticketQuantity=1
        prmotion_id=4023102
        for ticket in ticket_list:
            is_success=self.create_bonus(CREATE_BONUS_PLAYER,bonusAmount=bonusAmount,bonusPointAmount=bonusPointAmount,ticketId=ticket,ticketQuantity=ticketQuantity,prmotion_id=prmotion_id)
            if is_success:
                CustomerID,claimid,promotion_type = self.Search_Customer_bonus(CREATE_BONUS_PLAYER)
                if claimid :
                    self.claimid_list.append({
                        "promoClaimId":claimid,
                        "promotionType":promotion_type
                    }
                    )
                        
                else:
                    logging.error("沒有claimid")
                    
        self.Confirm_Customer_bonus()
           
if __name__ == "__main__":

    credential = {
        "operatorName": "carrine03",
        "password": "Test@1234"
    }
    username="bnm302"
    try:
        
        b_end=B_end(credential)
        if b_end.token:
            b_end.process_procedure(username)
        else:
            logging.error("登入失敗 無法取得Token")
    except Exception as e:
        logging.error(f"啟動時發生錯誤: {e}")
    
    

   