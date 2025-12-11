import requests,logging,time
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
def search_customerid(token,player:str):
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
def get_register_time(token,customer_id):
    API_URL2=f"http://sit-admin2.tcg.com/tac/api/relay/get/mcs-player-basic-information-getPlayerDetail"  
    headers={
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": token,
                "Content-Type": "application/json",
                "Connection": "keep-alive",
                "Language": "zh_CN",
                "Merchant": "gi8viet",
                "MerchantCode": "gi8viet",
                "Tac-Trace-Id":"6oqC9fITw8UXUOwy",
                "Referer": f"http://sit-admin2.tcg.com/20106/{customer_id}-gi8viet",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                "environment": "TCG3",
                "merchantCode": "gi8viet",
                "notPending": "true",
                "platform": "TCG"
        }
    params={
                "merchantCode":"gi8viet",
                "customerId": customer_id

    }
    cookies = {
                "language": "zh_CN",
            }
    try:
        response=requests.get(API_URL2,headers=headers,params=params,cookies=cookies,verify=False)
        response_data=response.json()
        if response_data.get("success")==True:
            value_list=response_data.get("value",{})
            register_time=value_list.get("registerTime")
            if register_time:
                register_time_str=datetime.fromtimestamp(register_time/1000).strftime("%Y-%m-%d %H:%M:%S")
                logging.info(f"register_time_str: {register_time_str}")
            return register_time_str
        else:
            logging.error(f"API Response: {response.text}")

    except Exception as e:
            logging.error(f"{e}")

      
def get_deposit_counts(token,regester_date,player):
    API_URL2=f"http://sit-admin2.tcg.com/tac/api/relay/post/ods-v2-user-member-psersonal-info"  
    end_time = datetime.now().strftime("%Y-%m-%d 23:59:59")
    headers={
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": token,
                "Content-Type": "application/json",
                "Connection": "keep-alive",
                "Language": "zh_CN",
                "Merchant": "gi8viet",
                "MerchantCode": "gi8viet",
                "Tac-Trace-Id":"aWLRJDWh(xK*ofqR",
                "Referer": f"http://sit-admin2.tcg.com/20106/{player}-gi8viet",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
                "environment": "TCG3",
                "merchantCode": "gi8viet",
                "notPending": "true",
                "platform": "TCG"
    }
    params={
                "customerName":player,
                "regStartDate":regester_date,
                "regEndDate":end_time,
                "page":1,
                "size":10,
                "subordinateType":"SELF",
                "pageable":True,
                "pagedExport":False,
                "needTotalCount":False,
                "needTotalCount":False,
                "privilege":False,
                "merchantCode":"gi8viet",
                "withdrawerNamePrivilege":False

    }
    payload={
                "customerName":player,
                "regStartDate":regester_date,
                "regEndDate":end_time,
                "page":1,
                "size":10,
                "subordinateType":"SELF",
                "pageable":True,
                "pagedExport":False,
                "needTotalCount":False,
                "needTotalCount":False,
                "privilege":False,
                "withdrawerNamePrivilege":False

    }
    cookies = {
                "language": "zh_CN",
            }
    try:
        response=requests.post(API_URL2,headers=headers,params=params,json=payload,cookies=cookies,verify=False)
        response_data=response.json()
        if response_data.get("success")==True:
            value_list=response_data.get("value",{})
            deposit_count_list=value_list.get("list", [])
            if deposit_count_list:
                deposit_count=deposit_count_list[0].get("depositCounts")
                logging.info(f"取得存款次數: {deposit_count}")
                return deposit_count
            else:
                logging.error(f"沒有拿到list")
        else:
            logging.error(f"API Response: {response.text}")

    except Exception as e:
            logging.error(f"{e}")
             
def implement_function(player):
    token=get_token()
    customer_id=search_customerid(token,player)
    time.sleep(1)
    regester_date=get_register_time(token,customer_id)
    deposit_count=get_deposit_counts(token,regester_date,player)
    if deposit_count==None:
        deposit_count=0
        return deposit_count
    else:
        return int(deposit_count)
     
'''
if __name__=="__main__":
    try:
        token=get_token()
    except Exception as e:
        print("啟動時取得 token 發生錯誤:", e)
    
    implement_function()   
    '''



