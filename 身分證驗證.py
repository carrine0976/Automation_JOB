import requests,logging,datetime
from datetime import datetime
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
class B_end:
    def __init__(self,credential:dict):
        self.token=self.get_token()
        self.credential=credential
    def header(self,player):
        return{
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": self.token,
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Content-Length": "0",
            "Language": "zh_CN",
            "Merchant": "gi8viet",
            "MerchantCode": "gi8viet",
            "Origin": "http://sit-admin2.tcg.com",
            "Referer": f"http://sit-admin2.tcg.com/20106/{player}-gi8viet",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "environment": "TCG3",
            "merchantCode": "gi8viet",
            "notPending": "true",
            "platform": "TCG",
            "operatorId":"2113085",
            "operatorName": "carrine03"
        }
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
            "Merchant": "gi8viet",
            "MerchantCode": "gi8viet",
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
        logging.info(f"狀態碼{requests_data.status_code}")
        requests_data.raise_for_status()
        token_data=requests_data.json()
        return token_data.get("token")

    def search_customerid(self,player:str):
        API_URL2=f"http://sit-admin2.tcg.com/tac/api/relay/get/player-search-non-bankcard?merchantCode=gi8viet&isWildcard=false&sortType=desc&pageable=true&data={player}&searchCode=USERNAME"  
        
        headers=self.header(player)
        cookies = {
            "language": "zh_CN"
        }
        try:
            response=requests.get(API_URL2, headers=headers, cookies=cookies, verify=False)
            response.raise_for_status()

            response_data=response.json()
            logging.info(f"{response_data}")
            if response_data.get("success") == True:
                value_data=response_data.get('value',{})
                player_list=value_data.get('list',[])
                if player_list:
                    customerId=player_list[0].get("customerId")
                    if customerId:
                        logging.info(f"拿到玩家資訊: {player}")
                        logging.info(f"CustomerID: {customerId}")
                    else:
                        logging.error("沒有拿到CustomerID")
                    return customerId
                else:
                    logging.error("沒有拿到List")
                
            else:
                error_msg = response_data.get("message", "未知錯誤")
                logging.error(f"未拿到玩家資訊: {error_msg}")
                return False
        except Exception as e:
            logging.error(f"狀態碼: {response.status_code}",e)
    def input_personal_id(self,customerId:int,player:str,number:int):

        logging.info(f"傳入的身分證ID:{number}")
        API_URL3=f"http://sit-admin2.tcg.com/tac/api/relay/post/mcs-player-security-information-changeIdNumber?customerId={customerId}&merchantCode=gi8viet&remark=33&idNumber={number}"
        
        headers=self.header(player)
        cookies = {
            "language": "zh_CN"
        }
        try:
            response=requests.post(API_URL3, cookies=cookies, headers=headers, verify=False)
            response.raise_for_status()

            response_data=response.json()
            if response_data.get("success") == True:
                value_data=response_data.get('value')
                logging.info(f"身分證ID輸入成功")  
            else:
                logging.error("身分證ID輸入失敗")
                return False
        
        except Exception as e:
            logging.error("身分證ID輸入請求失敗")
    def input_mobile_number(self,customerId:int,number:int,player:str):

        logging.info(f"傳入的手機號:{number}")
        API_URL=f"http://sit-admin2.tcg.com/tac/api/relay/post/mcs-player-security-information-changeMobile?customerId={customerId}&merchantCode=gi8viet&countryCode=66&playerMobile={number}&remark=22"
        headers=self.header(player)
        cookies = {
            "language": "zh_CN"
        }
        try:
            response=requests.post(API_URL, cookies=cookies, headers=headers, verify=False)
            response.raise_for_status()

            response_data=response.json()
            if response_data.get("success") == True:
                logging.info(f"手機號輸入成功")  
            else:
                logging.error("手機號驗證失敗")
                return False
        
        except Exception as e:
            logging.error("手機號驗證請求失敗")
    def verify_phone_number(self,customerId:int,player:str):
        API_URL3=f"http://sit-admin2.tcg.com/tac/api/relay/post/mcs-player-security-information-verifyMobile?remark=s&remarks=s&customerId={customerId}"
        
        headers=self.header(player)
        cookies = {
            "language": "zh_CN"
        }
        try:
            response=requests.post(API_URL3, cookies=cookies, headers=headers, verify=False)
            response.raise_for_status()

            response_data=response.json()
            if response_data.get("success") == True:
                logging.info(f"手機號驗證成功")  
            else:
                logging.error("手機號驗證失敗")
                return False
        
        except Exception as e:
            logging.error("手機號驗證請求失敗")
    def procedure(self):
        while True:
            n=int(input("輸入要填哪種資訊 1:身分證 2. 手機號碼\n"))
            username= str(input("輸入玩家帳號："))
            number=random.randint(100000000,999999999)
            customer_id=self.search_customerid(username)
            if customer_id:
                self.input_personal_id(customer_id,username,number)
                self.input_mobile_number(customer_id,username,number)
                select=int(input("是否驗證手機號 1.要 2.不用\n"))
                if select==1:
                    self.verify_phone_number(customer_id,username)

if __name__ == "__main__":

    credential={
        "operatorName": "carrine03",
        "password": "Test@1234"
        }
    backend=B_end(credential)
    if backend.token:
        backend.procedure()
        
    else:
        logging.error("沒有拿到token")
        

   