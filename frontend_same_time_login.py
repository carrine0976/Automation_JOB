import requests,logging
import threading
import concurrent.futures,time,datetime,time
from datetime import datetime,timedelta
import traceback,random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
start_event=threading.Event()
request_lock = threading.Lock()


class B_end:
    def __init__(self,credential:dict):
        self.session=requests.Session()
        self.username=''
        self.userid=''
        self.credential=credential
        self.token=None
        self.token_expire=None
        self.token=self.get_token_login(credential['username'],credential['password'])
        self.trans_id=''
        self.lock=threading.Lock()
    def rate_limit(self,method,url,max_retries=3,**kwargs):
        for attempt in range(max_retries):
            try:
                with request_lock:
                    time.sleep(random.uniform(0.3, 0.5))
                    if method.upper()=='GET':
                        response=self.session.get(url,**kwargs)
                    else:
                        response=self.session.post(url,**kwargs)

                    response_json=response.json()
                    if response.status_code==200 and response_json.get('success')==True:
                        return response
                    else:
                        error_code = response_json.get('errorCode', '')
                        if 'TOO_MANY_REQUEST' in error_code:
                            time.sleep(random.uniform(0.1, 0.5))
                            if attempt<max_retries-1:
                                continue
                    return response

            except requests.RequestException as e:
                logging.error(f"[{self.username}] 請求失敗: {e}")
                if attempt<max_retries-1:
                    time.sleep(random.uniform(0.1, 0.5))
    def rate_limit_approve(self,method,url,max_retries=3,**kwargs):
        for attempt in range(max_retries):
            try:
               
                if method.upper()=='GET':
                    response=self.session.get(url,**kwargs)
                else:
                    response=self.session.post(url,**kwargs)

                response_json=response.json()
                if response.status_code==200 and response_json.get('success')==True:
                    return response
                else:
                    error_code = response_json.get('errorCode', '')
                    if 'TOO_MANY_REQUEST' in error_code:
                        time.sleep(random.uniform(0.1, 0.3))
                        if attempt<max_retries-1:
                            continue
                return response

            except requests.RequestException as e:
                logging.error(f"[{self.username}] 請求失敗: {e}")
                if attempt<max_retries-1:
                    time.sleep(random.uniform(0.1, 0.3))

    def get_token_login(self, username, password):
        try:

            if self.token is not None and self.token_expire is not None and datetime.now()<self.token_expire:
                return self.token
            
            login_url='http://www.sit-gi8viet.com/wps/session/login/unsecure'
            
            headers = {
                'Content-Type': 'application/json',
                'Merchant': 'gi8viet',
                
            }
            login_data={
                'username':username,
                'password':password
            } 
            
            requests_data=self.rate_limit("POST",login_url,json=login_data,headers=headers)
            print(requests_data.text)
            self.username = requests_data.json()['value']['userName']
            self.userid = requests_data.json()['value']['id']
            self.token=requests_data.json()['value']['token']

            self.token_expire=datetime.now()+timedelta(minutes=25)
            logging.info(f"token 將在{self.token_expire}過期 ")
            return self.token
        
        except requests.RequestException as e:
            logging.error(f"請求失敗{e}")
            return None
    def is_token_valid(self):
        
        return (self.token is not None and 
                self.token_expire is not None and 
                datetime.now() < self.token_expire)
    def get_Ticket_transaction_ID(self):
        if not self.is_token_valid():
            logging.info("token 過期, 重新登入")
            self.get_token_login(self.credential['username'],self.credential['password'])
        if self.token is None:
            return
        current_time=datetime.now()
        unit_time=str(int(current_time.timestamp()*1000))
        login_URL=f"http://www.sit-gi8viet.com/wps/relay/PROMOFE_getClaimTicketList?isApp=N&status=AVAILABLE&_={unit_time}"

        headers={
            'Content-Type': 'application/json',
            'Merchant': 'gi8viet',
            "Authorization":self.token
        }
        
        cookies={
            'SHELL_deviceId': '8c5bdbd3-b2cd-b350-4c4e-5967bb9d7966',
            'afUserId': '04953ba2-ce16-4b15-8ed4-05c43b9a3153-p',
            'AF_SYNC': '1751265971390'
        }
        
        response=self.rate_limit("GET",login_URL,headers=headers,cookies=cookies)
        response_json=response.json()
        
        if response_json.get('success')==True:
            self.response_value_list=response_json.get('value',{})
            if self.response_value_list:
                self.response_value_info=self.response_value_list[0]
                Trans_id=self.response_value_info.get('transactionId') 
                Condition_status=self.response_value_info.get('conditionStatus',[])
                if Trans_id and not Condition_status:
                    self.trans_id=Trans_id
                    logging.info(f"成功拿到交易ID{self.trans_id}")
                    return self.trans_id
            return None
        else:
            logging.error(f"交易ID查詢失敗")
            return None
    def approve_to_receive_ticket(self):
        if not self.is_token_valid():
            logging.info("token 過期, 重新登入")
            self.get_token_login(self.credential['username'],self.credential['password'])
        if self.token is None:
            return
        login_URL=f"http://www.sit-gi8viet.com/wps/relay/PROMOFE_claimTicket"

        headers={
            'Content-Type': 'application/json',
            'Merchant': 'gi8viet',
            "Authorization":self.token,
            'Connection': 'keep-alive',
            'Language': 'VI',
            'Origin': 'http://www.sit-gi8viet.com',
            'Referer': 'http://www.sit-gi8viet.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'Origin':'http://www.sit-gi8viet.com',
            'Referer':'http://www.sit-gi8viet.com/',
            
        }
        payload={
             "transactionId": self.trans_id,
             "isApp": "N"
        }
        cookies={
            'SHELL_deviceId': '8c5bdbd3-b2cd-b350-4c4e-5967bb9d7966',
            'afUserId': '04953ba2-ce16-4b15-8ed4-05c43b9a3153-p',
            'AF_SYNC': '1751265971390'
        }

        
        response=self.rate_limit_approve("POST",login_URL,headers=headers,json=payload,cookies=cookies)
        response_json=response.json()
        
        if response_json.get('success')==True:
            self.response_value_list=response_json.get('value',{})
            if self.response_value_list:
                Trans_id=self.response_value_list.get('transactionId') 
                Type=self.response_value_list.get('type') 
                logging.info(f"成功領取票卷 交易ID: {self.trans_id} 獎勵 {Trans_id} 類別{Type}")
            return True
            
        else:
            logging.error(f"領取票卷失敗")
            logging.error(traceback.format_exc())
            return False
        

    
def main():
    b_object=[]
    credentials = [
        {
            "username": "pmp006",
            "password": "123qwe"
        },
        {
            "username": "pmp909",
            "password": "123qwe"
        },
        {
            "username": "tty777",
            "password": "123qwe"
        },
        {
            "username": "pmp908",
            "password": "123qwe"
        }
        
    ]
    for credential in credentials:
            b_end = B_end(credential)
            if b_end.token:
                trans_id=b_end.get_Ticket_transaction_ID()
                if trans_id:
                    b_object.append(b_end)
            else:
                logging.error(f"[{credential['username']}] 登入失敗 無法取得Token")
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(b_object)) as executor:
        future= [executor.submit(b_end.approve_to_receive_ticket) for b_end in b_object]

        complete_future=concurrent.futures.as_completed(future,timeout=10)
        for futures in complete_future:
            try:
                futures.result()
            except Exception as e :
                logging.error(f"操作異常{e}")
    logging.info("所有玩家操作完成")
main()

            



   