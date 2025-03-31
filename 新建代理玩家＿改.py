import requests,logging,json
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
def get_token():
    login_url="http://sit-admin2.tcg.com/tac/api/login/password"
    payload={
        "operatorName": "carrine03",
        "password": "Test@1234"
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

def create_agent(player:str):
    token=get_token()
    API_URL = f"http://sit-admin2.tcg.com/mcs_console/api/agentInfo/createAgent?agentName={player}&masterAgentType=2" 
    payload = {
    "merchantCode": "gi8viet",
    "agentName": player,
    "configs": [
        {"type": "VIETNAM_LOTTO", "rebateValue": 100, "rebateSubordinateLimit": 100},
        {"type": "SBO", "rebateValue": 1.5, "rebateSubordinateLimit": 1.5},
        {"type": "FISH", "rebateValue": 1.5, "rebateSubordinateLimit": 1.5},
        {"type": "ELOTTO", "rebateValue": 120, "rebateSubordinateLimit": 120}
    ]
}


    headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Language": "zh_CN",
    "Merchant": "gi8viet",
    "Origin": "http://sit-admin2.tcg.com",
    "Referer": "http://sit-admin2.tcg.com/20200",
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
        response.raise_for_status()
        
        
        response_data = response.json()
        logging.info(f"狀態碼: {response.status_code}")
        logging.info(f"響應內容: {response_data}")
        
        
        if response_data.get("success") == True:
            logging.info(f"新建代理玩家成功: {player}")
            return True
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.error(f"創建代理失敗: {error_msg}")
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
def search_customerid(player:str):
    token=get_token()
    API_URL2=f"http://sit-admin2.tcg.com/tac/api/relay/get/player-search-non-bankcard?merchantCode=gi8viet&isWildcard=false&sortType=desc&pageable=true&data={player}&searchCode=USERNAME"  
    
    headers={
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": token,
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Language": "zh_CN",
        "Merchant": "gi8viet",
        "MerchantCode": "gi8viet",
        "Origin": "http://sit-admin2.tcg.com",
        "Referer": "http://sit-admin2.tcg.com/311792",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "environment": "TCG3",
        "merchantCode": "gi8viet",
        "notPending": "true",
        "platform": "TCG"
    }
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
        logging.error(f"狀態碼: {response.status_code}")
def reset_password(customerId:int,player:str):
    token=get_token()
    API_URL3=f"http://sit-admin2.tcg.com/tac/api/relay/post/mcs-player-security-information-resetLoginPasswordDefault?remark=t&remarks=t&customerId={customerId}"
    
    headers={
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": token,
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
        "operatorName": "carrine01"
    }
    cookies = {
        "language": "zh_CN"
    }
    try:
        response=requests.post(API_URL3, cookies=cookies, headers=headers, verify=False)
        response.raise_for_status()

        response_data=response.json()
        if response_data.get('success') == True:
            value_data=response_data.get('value')
            logging.info(f"玩家密碼 {value_data}")
            return value_data    
        else:
            logging.error("沒有拿到value")
            return False
    
    except Exception as e:
        logging.error("重設密碼請求失敗")

class Frontend:
    def __init__(self):
        self.session=requests.Session()
        self.token=None
    def get_token_login(self, username, password):
        try:
            login_url='http://www.sit-gi8viet.com/wps/session/login/unsecure'
            
            headers = {
                'Content-Type': 'application/json',
                'Merchant': 'gi8viet',
                #"Accept":"application/json, text/plain, */*",
                #"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
            }
            login_data={
                'userName':username,
                'password':password
            } 
            
            requests_data=self.session.post(login_url,json=login_data,headers=headers)
            print(requests_data.text)
            self.username = requests_data.json()['value']['userName']
            self.userid = requests_data.json()['value']['id']
            self.token=requests_data.json()['token']
            return self.token
        
        except requests.RequestException as e:
            logging.error(f"請求失敗{e}")
            return None
        

    def reset_password_to_123qwe(self):
        try:
            password={
                "oldPassword":"",
                "password":"123qwe",
                "confirmPassword":"123qwe"
            }
            
            API_URL="http://www.sit-gi8viet.com/wps/member/password/unsecure"
            
            headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'Merchant': 'gi8viet'
            
            }
            
            requests_data=self.session.post(API_URL,json=password,headers=headers)
            requests_data.raise_for_status()
            response_data=requests_data.json()

            if response_data.get("success")==True:
                logging.info(f"密碼重置成功{response_data}")
                return True
            else:
                logging.error(f"密碼重置失敗{e}")
                return False
        except Exception as e:
            logging.error(f"重置密碼時出錯: {e}")
            return False
        
if __name__ == "__main__":
    try:
        token = get_token()
        print("取得的 token:", token)

        #填入玩家帳號
        NEW_REGISTER = "ww74de0"
        create_agent(NEW_REGISTER)
        
        customer_id=search_customerid(NEW_REGISTER)
        if customer_id:
            new_password=reset_password(customer_id,NEW_REGISTER)
            
            frontend = Frontend()
            login_token=frontend.get_token_login(NEW_REGISTER,new_password)
            print(f"登入 Token: {login_token}")

            if not login_token:
                logging.error("登入失敗")
                exit()
                
            if frontend.reset_password_to_123qwe(login_token):
                logging.info(f"成功將{NEW_REGISTER}的密碼重置123qwe")
            else:
                logging.error("重置密碼失敗")
    except Exception as e:
        print(f"啟動時取得 token 發生錯誤:{e}")
    

   