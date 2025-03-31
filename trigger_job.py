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

def check_ticket_status():
    token=get_token()
    API_URL = "http://sit-admin2.tcg.com/tac/api/relay/get/promo-ticket-claim-report-list" 
    params = {
    "relayDisableEncode": "true",
    "searchDateMode": "claimDate",
    "userName": "rrr361",
    "startDate": "1741104000000",
    "endDate": "1741190399000",
    "page": "1",
    "size": "3000"
    }

    headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
    "Connection": "keep-alive",
    "Language": "zh_CN",
    "Merchant": "gi8viet",
    "Referer": "http://sit-admin2.tcg.com/24786",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "environment": "TCG3",
    "merchantCode": "gi8viet",
    "platform": "TCG"
    }
    response = requests.get(API_URL, params=params, headers=headers, verify=False)

    try:
        data = response.json()  
        formatted_data = json.dumps(data, indent=4, ensure_ascii=False)
    except ValueError:
        data = response.text

    logging.info(f"API data: {formatted_data}")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M")  
    file_path = f"ticket_status_log_{timestamp}.txt"
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{now} - API Response: {formatted_data}\n")
    print(f"{now} - Checked ticket status.")
if __name__ == "__main__":
    try:
        token = get_token()
        print("取得的 token:", token)
    except Exception as e:
        print("啟動時取得 token 發生錯誤:", e)

    check_ticket_status()
    # 設定每天凌晨 12:00 執行
    schedule.every().day.at("23:50").do(check_ticket_status)  
    schedule.every().day.at("23:58").do(check_ticket_status)   
    schedule.every().day.at("00:00").do(check_ticket_status)

    # 每分鐘檢查一次是否有任務
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("程式中断") 
