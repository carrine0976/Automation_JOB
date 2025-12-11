import requests,logging
from datetime import datetime,timedelta
import threading
import concurrent.futures
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
def run_operator(credential):
    try:
        b_end = B_end(credential)
        if b_end.token:
            b_end.implement()
        else:
            logging.error(f"[{credential['operatorName']}] 登入失敗 無法取得Token")
    except Exception as e:
        logging.error(f"[{credential['operatorName']}] 執行時發生錯誤: {e}")

class B_end:
    def __init__(self,credential:dict):
        self.session=requests.Session()
        self.username=''
        self.password=''
        self.credential=credential  
        self.token=self.get_token(credential['operatorName'],credential['password'])
        self.token_data=self.token
        self.record_data_list=[]
        self.claimid_list=[]
        self.success_count=0
        self.claimid=''
        self.lock=threading.Lock()
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
            "Merchant": 'gi8viet',
            "MerchantCode": 'gi8viet',
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

    def get_executionNo(self):
        API_URL = "http://sit-admin2.tcg.com/tac/api/relay/get/mcs-manual-promotion-cond-progress?merchantCode=gi8viet" 
        
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": self.token,
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Language": "zh_CN",
            "Origin": "http://sit-admin2.tcg.com",
            "Referer": "http://sit-admin2.tcg.com/20000",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            "environment": "TCG3",
            "Merchant": self.credential["Merchant"],
            "MerchantCode": self.credential["MerchantCode"],
            "platform": "TCG"
        }
        
        try:
            response = requests.get(API_URL, headers=headers, verify=False)
            response.raise_for_status()
            
            response_data = response.json()
            
            if response_data.get('success') == True:
                value=response_data.get('value',[])
                executionNo=value[0].get("executionNo")
                
                logging.info(f"拿到補派id {executionNo} ")
                return executionNo
                
            else:
                error_msg = response_data.get("message", "未知錯誤")
                logging.error(f"沒有拿到補派id: {error_msg}")
                return []
            
        except Exception as e:
            logging.error(f"狀態碼: {response.status_code}",e)
            return []
    def manual_retry_function(self,executionNo):
        API_URL = "http://10.80.1.19:7001/mcs-console/promotion/manual/retry" 
        payload={ 
            "executionNo": executionNo, 
            "merchantCode": "gi8viet" 
        }
        headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": self.token,
        "Connection": "keep-alive",
        }
        
        try:
            response = requests.post(API_URL, headers=headers,json=payload, verify=False)
            response.raise_for_status()
            
            response_data = response.json()
            
            if response_data.get('success') == True:
                logging.info(f"補派成功: ")
                return True
                
            else:
                error_msg = response_data.get("message", "未知錯誤")
                logging.error(f"補派失敗: {error_msg}")
                return False
            
        except Exception as e:
            logging.error(f"狀態碼: {response.status_code}",{e})
            return False
    
    def implement(self):
        executionNo=self.get_executionNo()
        isSuccess=self.manual_retry_function(executionNo)
        if isSuccess:
            logging.info("操作成功")
        else:
            logging.error("操作失敗")
def main():
    credentials = [
        {
            "operatorName": "parisv01",
            "password": "Aa123456@",
            "Merchant": "gi8viet",
            "MerchantCode": "gi8viet",
        },
        {
            "operatorName": "carrine01",
            "password": "Test@1234",
            "Merchant": "gi8viet",
            "MerchantCode": "gi8viet",
            #"Merchant": "huamei",
            #"MerchantCode": "huamei",
        }
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(credentials)) as executor:
        future= [executor.submit(run_operator, credential) for credential in credentials]
        concurrent.futures.wait(future)
    logging.info("品牌管理員操作完成")

main()


    

   