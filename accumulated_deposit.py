import requests,logging,time,yaml,os
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
    token_data=requests_data.json()
    return token_data.get("token")
def search_deposit_count(token):
    API_URL2=f"http://sit-admin2.tcg.com/tac/api/relay/get/mcs-depositPromotion-searchDetails"  
    
    headers={
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": token,
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "Language": "zh_CN",
        "Merchant": "gi8viet",
        "MerchantCode": "gi8viet",
        "Referer": "http://sit-admin2.tcg.com/24782",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "environment": "TCG3",
        "merchantCode": "gi8viet",
        "notPending": "true",
        "platform": "TCG",
        "Tac-Trace-Id":"xXaTikW@z5rJ7J9W"
    }
    params={
        "promotionId": "4023099", # 累計存款
        "merchantCode": "gi8viet",
        }
    
    try:
        response=requests.get(API_URL2, headers=headers, params=params, verify=False)

        response_data=response.json()
        if response_data.get("success") == True:
            value_data=response_data.get('value',{})
            deposit_config=value_data.get('depositPromotionConfigs',[])
            if deposit_config:
                first_config=deposit_config[0]
                depositCount=first_config.get('depositCount')
                logging.info(f"拿到要求存款次數: {depositCount}")
                return depositCount
            else:
                logging.error("沒有拿到deposit_config")
                return None
            
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.error(f"未拿到活動資訊: {error_msg}")
            return False
    except Exception as e:
        logging.error(e)

def implement_accumulated_function():
    token=get_token()
    deposit_count=search_deposit_count(token)
    time.sleep(1)
    return deposit_count
     

if __name__=="__main__":
    try:
        token=get_token()
    except Exception as e:
        print("啟動時取得 token 發生錯誤:", e)
    implement_accumulated_function()



