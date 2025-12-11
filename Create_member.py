import requests,logging
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def Create_member(CustomerName,mobile_num,uuid):
    URL="http://10.80.1.22:7001/tcg-uss-ae/customer-create/register"

    header={
        "Language":"CN",
        "Content-Type":"application/json"
    }
    payload={ 
            "activeFlag":0,
            "customerName":f"gi8viet@{CustomerName}", 
            "email":f"{CustomerName}@gi8viet.com", 
            "hashAlgorithm":0, 
            "loginLanguage":"CN", 
            "merchantCode":"gi8viet", 
            "password":"123qwe", 
            "glifeId":f"{CustomerName}", 
            "mayaId":f"{CustomerName}", 
            "profile":{ 
            "address":"Osaka", 
            "city":"Osaka", 
            "countryCode":"Taipei", 
            "createSuboFlag":0, 
            "gender":0, 
            "idType":0, 
            "mobileNo":f"{mobile_num}", 
            "sourceOfIncome":0, 
            "type":0, 
            "zipcode":"111", 
            "idVerification":1, 
            "idVerificationStatus":"Y", 
            "appleId":f"{CustomerName}", 
            "facebookId":f"{CustomerName}", 
            "lineId":f"{CustomerName}", 
            "lineUuid":f"U80b36f48e3bc89b7bd8f{uuid}d00429d", 
            "qqNo":f"{CustomerName}", 
            "telegram":f"{CustomerName}", 
            "viber":f"{CustomerName}", 
            "twitter":f"{CustomerName}", 
            "twitterId":f"{CustomerName}", 
            "wechat":f"{CustomerName}", 
            "whatsAppId":f"{CustomerName}", 
            "zalo":f"{CustomerName}", 
            "recommenderId":2151008, 
            "level_id":2151008 
            } 
            }
    print(CustomerName)
    resposne=requests.post(URL,headers=header,json=payload,verify=False)
    resposne_json=resposne.json()
    if resposne_json.get("success"):
        logging.info("創建會員玩家成功")
    else:
        logging.error(f"觸發失敗{resposne.text}")

def reset_to_123qwe(customerId:list):
        for customer_id in customerId:
            URL="http://10.80.1.22:7001/tcg-uss-ae/password"
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/json",
                "Connection": "keep-alive",
                "Accept":"application/json"
            }
            payload={ 
                "customerId": customer_id, 
                "needLogInToChangePassword": True, 
                "password": "123qwe" 
        }
            response=requests.put(URL,headers=headers,json=payload,verify=False)
            response_data=response.json()
            if response_data.get("success")==True:
                logging.info("修改密碼成功")
                continue
            else:
                logging.info("修改密碼失敗")
        
        logging.info("修改密碼完成")
def get_token(credential:dict):
        login_url="http://sit-admin2.tcg.com/tac/api/login/password"
        payload={
            "operatorName": credential['operatorName'],
            "password": credential['password']
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
        token=token_data.get("token")
        return token
def search_customerid(token,player:str,MerchantCode:str):
        
        API_URL2=f"http://sit-admin2.tcg.com/tac/api/relay/get/player-search-non-bankcard?merchantCode={MerchantCode}&isWildcard=false&sortType=desc&pageable=true&data={player}&searchCode=USERNAME"  
        
        headers={
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": token,
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Language": "zh_CN",
            "Merchant": str(MerchantCode),
            "MerchantCode": str(MerchantCode),
            "Origin": "http://sit-admin2.tcg.com",
            "Referer": "http://sit-admin2.tcg.com/311792",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "environment": "TCG3",
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
            if response_data.get("success") == True:
                value_data=response_data.get('value',{})
                player_list=value_data.get('list',[])
                if player_list:
                    customerId=player_list[0].get("customerId")
                    if customerId:
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
def main():
    credential = {
        "operatorName": "carrine03",
        "password": "Test@1234"
        }
    account_name=str(input("請輸入帳號標題:"))
    start=int(input("起始數"))
    end=int(input("結尾數"))
    customer_list=[]
    token=get_token(credential)
    MerchantCode="gi8viet"
    if start>end:
         print("起始數要大於尾數")
         return
    else:
        for i in range(start,end+1):
            create_member_name=f"{account_name}{i}"
            mobile_num=random.randint(1000000000,9999999999)
            uuid=random.randint(10000,99999)
            Create_member(create_member_name,mobile_num,uuid)
            customer_id=search_customerid(token,create_member_name,MerchantCode)
            if customer_id:
                customer_list.append(customer_id)
            else:
                 logging.error("查無此customer_id")

        reset_to_123qwe(customer_list)
    
main()

