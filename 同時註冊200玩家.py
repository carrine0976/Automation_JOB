import requests,logging
import random
import aiohttp
import asyncio,json,time,datetime
from datetime import timedelta
import Search_Customer_id


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
URL="http://10.80.1.22:7001/tcg-uss-ae/customer-create/register"
login_url='http://www.sit-gi8viet.com/wps/session/login/unsecure'




async def get_token_login(session, username, password):
        
            
        login_url='http://www.sit-gi8viet.com/wps/session/login/unsecure'
            
        headers = {
                'Content-Type': 'application/json',
                'Merchant': 'gi8viet',
                
            }
        login_data={
                'username':username,
                'password':password
            } 
        try:
            async with session.post(login_url,json=login_data,headers=headers,ssl=False) as resp:
                request_data=await resp.json()
                if request_data.get("value"):
                    username = request_data['value']['userName']
                    userid = request_data['value']['id']
                    token=request_data['value']['token']

                    return token
                else:
                    logging.error(f"{username} 登入失敗: {request_data}")
                    return None
        
        except requests.RequestException as e:
            logging.error(f"請求失敗{e}")
            return None

async def Create_member(session,CustomerName):
    start=time.time()
    mobile_num=random.randint(1000000000,9999999999)
    uuid=random.randint(100000000,999999999)
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
            "lineUuid":f"U80b36f48e3bc89b7{uuid}d00429d", 
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
    
    try:
        async with session.post(URL,headers=header,json=payload,ssl=False)as resp:
            text=await resp.text()
            end=time.time()
            try:
                data=json.loads(text)
            except:
                logging.info(f"[{CustomerName}] 非 JSON 回應：{text}")
                return
            if data.get("success"):
                logging.info(f"創建會員玩家成功{CustomerName} 完成時間{end} CostTime{end-start:.2f}s")
                
            else:
                logging.error(f"觸發失敗{text}")
    except Exception as e:
        logging.error(f"[{CustomerName}] 請求錯誤: {e}")

async def batch_login(session,member_list,batch_size=1,delay=1):
    for i in range(0,len(member_list),batch_size):
        batch=member_list[i:i+batch_size]
        logging.info("批次登入")
        task=[
            get_token_login(session,name,"123qwe")
            for name in batch
        ]
        await asyncio.gather(*task)
        await asyncio.sleep(delay)

async def get_customer_id(session,member_list,MerchantCode):
    CustomerID_list=[]
    task=[]
    for name in member_list:
        URL=f"http://10.80.1.20:7001/promo-fe/resources/version/auto_qa/get_customer_id?merchant={MerchantCode}&customerName={name}"

        task.append(
            session.get(URL,ssl=False)
        )
    response=await asyncio.gather(*task, return_exceptions=True)
    for customer_id,resp in zip(member_list,response):
        if isinstance(resp, Exception):
            logging.error(f" 請求錯誤: {resp}")
            continue
        try:
            text=await resp.text()
            text=text.strip()
            print(text)
            if text.isdigit():
                customer_id=int(text)
                CustomerID_list.append(customer_id)

            else:
                customer_id = text
                CustomerID_list.append(customer_id)
        except:
            logging.info(f"[ 非 JSON 回應：{text}")
    return CustomerID_list

async def create_wallet(session,customer_id_list):
    
    task=[]
    for customer_id in customer_id_list:
        URL=f"http://10.80.1.23:7001/ac-service-service/resources/accounts/customer/{customer_id}"
        headers = {
                'Content-Type': 'application/json',
                
            }
        task.append(
            session.post(URL,data="",headers=headers,ssl=False)
        )
    response=await asyncio.gather(*task, return_exceptions=True)
    print(response)
    

    for customer_id, resp in zip(customer_id_list,response):
        if isinstance(resp, Exception):
            logging.error(f"[{customer_id}] 請求錯誤: {resp}")
            continue
        print("status:", resp.status)
        
        try:
            text=await resp.text()
            data=json.loads(text)
        except:
            logging.info(f"[ 非 JSON 回應：{text}")

        if data.get("success"):
            logging.info(f"創建會員錢包成功：{customer_id} ")
            
        else:
            logging.error(f"創建會員錢包失敗{text}")


async def main():
   
    MerchantCode="gi8viet"
    member_list=[]
    
    for i in range(300):
        acount=f"ijijwe{i}"
        member_list.append(acount)
    async with aiohttp.ClientSession() as session:
        tasks=[
            Create_member(session,name)
            for name in member_list
        ]
        await asyncio.gather(*tasks)
        
        customer_id_list=Search_Customer_id.main_batch(member_list,MerchantCode)
        #get_customer_id(session,member_list,MerchantCode)
        await create_wallet(session,customer_id_list)
        await batch_login(session,member_list,batch_size=1,delay=1)
      
    
asyncio.run(main())

