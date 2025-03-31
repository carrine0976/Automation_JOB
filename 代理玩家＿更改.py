import schedule
import time
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
        "operatorName": "carrine01",
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
    payload={
        "remark": "t",
        "remarks": "t",
        "customerId": customerId
    }
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
        if response_data.get("success") == True:
            value_data=response_data.get('value')
            logging.info(f"成功reset玩家密碼{response_data}")
            return value_data    
        else:
            logging.error("沒有拿到value")
            return False
    
    except Exception as e:
        logging.error("重設密碼請求失敗")
if __name__ == "__main__":
    try:
        token = get_token()
        print("取得的 token:", token)
    except Exception as e:
        print("啟動時取得 token 發生錯誤:", e)

    NEW_REGISTER="rrr391"
    create_agent(NEW_REGISTER)
    customer_id=search_customerid(NEW_REGISTER)
    if customer_id:
        reset_password(customer_id,NEW_REGISTER)
    else:
        logging.error("沒有拿到CustomerID")
    

   