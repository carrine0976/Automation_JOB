import requests,logging,time
from datetime import datetime,timedelta
import traceback

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
class Frontend:
    def __init__(self,credential:dict):
        self.session=requests.Session()
        self.username=''
        self.userid=''
        self.credential=credential
        self.token=None
        self.token_expire=None
        self.token=self.get_token_login(credential['username'],credential['password'])
        self.trans_id=''
        self.configId_1=0
        self.configId_2=0
        self.configId_3=0
        self.configId_4=0
        self.configId_5=0
        self.configId_6=0
        self.configId_7=0
        self.configId_8=0
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
            
            requests_data=self.session.post(login_url,json=login_data,headers=headers)
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
            '_ga': 'GA1.1.343769134.1743155195',
            'SHELL_deviceId': '9248aea2-32ed-4b1a-afa9-d039ed6d1b95',
            '_ga_ABCD123456789': 'GS1.1.1743402506.3.1.1743402698.0.0.0'
        }
        
        response=self.session.get(login_URL,headers=headers,cookies=cookies)
        response.raise_for_status()
        response_json=response.json()
        try:
            if response_json.get('success')==True:
                self.response_value_list=response_json.get('value',[])
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
        
        except requests.exceptions.RequestException as e:
            logging.error(f"get_Ticket_transaction_ID 失敗: {e}")
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
        }
        payload={
             "transactionId": self.trans_id,
             "isApp": "N"
        }
        cookies={
            'SHELL_deviceId': '81787dd4-3200-e7f3-5da9-bcd3a92fe636',
        }
        
        response=self.session.post(login_URL,headers=headers,json=payload,cookies=cookies)
        response_json=response.json()
        try:
            if response_json.get('success')==True:
                self.response_value_list=response_json.get('value')
                if self.response_value_list:
                    Trans_id=self.response_value_list.get('value') 
                    configId=str(self.response_value_list.get('configId'))
                    logging.info(f"領到的 configId: {configId}")
                    
                    if configId == '1198040':
                        self.configId_1+=1
                    elif configId == '1198041':
                        self.configId_2+=1
                    elif configId == '1198042':
                        self.configId_3+=1
                    elif configId == '1198043':
                        self.configId_4+=1
                    elif configId == '1198044':
                        self.configId_5+=1
                    elif configId == '1198045':
                        self.configId_6+=1
                    elif configId == '1198046':
                        self.configId_7+=1
                    elif configId == '1198047':
                        self.configId_8+=1
                    

                    logging.info(f"成功領取票卷 交易ID: {self.trans_id} 獎勵 {Trans_id} ")
                return True
                
            else:
                logging.error(f"領取票卷失敗")
                logging.error(traceback.format_exc())
                return False
        except Exception as e:
            logging.error("領取票卷失敗")
            logging.error(traceback.format_exc())
            return False
    def poccess_all_ticket(self):
        success_count=0
        rewards = {
        "a": {"id": "1198040", "rate": 12.5, "used_up":True, "custom":True},
        "b": {"id": "1198041", "rate": 12.5, "used_up":True, "custom":True},
        "c": {"id": "1198042", "rate": 12.5 ,"used_up":False, "custom":False},
        "d": {"id": "1198043", "rate": 12.5, "used_up":False, "custom":False},
        "e": {"id": "1198044", "rate": 12.5, "used_up":False, "custom":False},
        "f": {"id": "1198045", "rate": 12.5, "used_up":False, "custom":False},
        "g": {"id": "1198046", "rate": 12.5, "used_up":False, "custom":False},
        "h": {"id": "1198047", "rate": 12.5, "used_up":False, "custom":False},
        }
        remaining_rewards = {k: v for k, v in rewards.items() if not v["used_up"]}
        remaining_total=sum(v["rate"] for v in remaining_rewards.values())
        try:
            while True:
                trans_id=self.get_Ticket_transaction_ID()
                if not trans_id:
                    break
                self.approve_to_receive_ticket()
                success_count+=1
                logging.info(f"領取到第{success_count}次")
                time.sleep(1)
            if success_count == 0:
                logging.warning("沒有成功領取任何票券")
                return
        except KeyboardInterrupt:
            logging.info("手動終止")
        id_to_count = {
            "1198040": self.configId_1,
            "1198041": self.configId_2,
            "1198042": self.configId_3,
            "1198043": self.configId_4,
            "1198044": self.configId_5,
            "1198045": self.configId_6,
            "1198046": self.configId_7,
            "1198047": self.configId_8,
        }
        for name,reward in rewards.items():
            prize_id=reward['id']
            hit_count = id_to_count.get(prize_id, 0)
            actual_rate=hit_count/success_count
            if not reward["used_up"] and not reward["custom"]:
                average_pass_rate=(reward["rate"]/remaining_total)
                logging.info(f"獎品 {name.upper()} (ID: {prize_id}) - 實際中獎率: {actual_rate:.2%}, 分配後機率: {average_pass_rate:.2%} 領取{hit_count}次")
            elif not reward["used_up"] and reward["custom"]:
                average_pass_rate=0
                logging.info(f"獎品 {name.upper()} (ID: {prize_id}) - 實際中獎率: {actual_rate:.2%}, 分配後機率: {average_pass_rate:.2%} 領取{hit_count}次")
            elif reward["used_up"] and reward["custom"]:
                average_pass_rate=0
                logging.info(f"獎品 {name.upper()} (ID: {prize_id}) - 實際中獎率: {actual_rate:.2%}, 分配後機率: {average_pass_rate:.2%} 領取{hit_count}次")
        
if __name__ == "__main__":
  
    #填入玩家帳號
    credential = {
        "username": "pvp006",
        "password": "123qwe"
    }
    try:    
        frontend = Frontend(credential)
        if frontend.token:
            logging.info(f"登入成功 Token: {frontend.token}")
            frontend.poccess_all_ticket()
            
        else:
            logging.error("登入失敗 無法取得Token")
    
    except Exception as e:
        logging.error(f"啟動時發生錯誤: {e}")
        logging.error(traceback.format_exc())

   