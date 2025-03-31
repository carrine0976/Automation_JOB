import schedule
import time,random
import requests,logging,json
from datetime import datetime,timedelta

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

def create_bonus(player:str,bonusAmount:int,bonusPointAmount:int,ticketId:int,ticketQuantity:int,prmotion_id:int):
    token=get_token()
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
    "Authorization": token,
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
        response.raise_for_status()
        
        
        response_data = response.json()
        logging.info(f"狀態碼: {response.status_code}")
        logging.info(f"響應內容: {response_data}")
        
        
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
def Search_Customer_bonus(player:str):
    token=get_token()
    API_URL = "http://sit-admin2.tcg.com/tac/api/relay/get/mcs-manualPromotion-search" 
    start_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
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
    "Authorization": token,
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
        logging.info(f"狀態碼: {response.status_code}")
        logging.info(f"響應內容: {response_data}")
        
        
        if response_data.get("success") == True:
            customer_list=response_data.get("value",[])
            
            if customer_list:
                customer_info=customer_list[0]
                CustomerID=customer_info.get("customerId")
                claimid=customer_info.get("id")
    
                if CustomerID and claimid:
                    logging.info(f"拿到 CustomerID: {CustomerID} 和 claimid: {claimid}")
                    return CustomerID, claimid
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
  
def Confirm_Customer_bonus(Customerid:int,claimid:int ):
    token=get_token()
    API_URL = f"http://sit-admin2.tcg.com/tac/api/relay/post/mcs-manual-promotion-approveClaimStatus?claimStatus=I&customerId={Customerid}&claimId={claimid}" 
    payload = {
    "claimStatus": "I",
    "customerId":str(Customerid),
    "claimId": str(claimid),
    "internalRemark": "g"
    
}

    headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
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
        response.raise_for_status()
        
        
        response_data = response.json()
        logging.info(f"狀態碼: {response.status_code}")
        logging.info(f"響應內容: {response_data}")
        
        
        if response_data.get("success") == True:
            logging.info(f"審核活動紅利成功 ")
            return True
        else:
            error_msg = response_data.get("value" )
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
if __name__ == "__main__":
    try:
        token = get_token()
        print("取得的 token:", token)
    except Exception as e:
        print("啟動時取得 token 發生錯誤:", e)

    #填入玩家帳號
    CREATE_BONUS_PLAYER = "carrine017"
    bonusAmount=1000
    bonusPointAmount=0
    count=2
    random_ticket=random.choice([1004007,1004006,1004008,1004010,1004009,1010009])
    ticketQuantity=30
    #ticket=1034007
    prmotion_id=["3638044", "3758047", "3762068"]
    for promo in prmotion_id:
        create_bonus(CREATE_BONUS_PLAYER,bonusAmount=bonusAmount,bonusPointAmount=bonusPointAmount,ticketId=random_ticket,ticketQuantity=ticketQuantity,prmotion_id=promo)
        Customerid,claimid = Search_Customer_bonus(CREATE_BONUS_PLAYER)
        if Customerid is not None and claimid is not None:
            Confirm_Customer_bonus(Customerid,claimid)
        else:
            logging.error("沒有拿到ID")
   
    
    
    

   