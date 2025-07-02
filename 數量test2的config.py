import requests,logging,time
from datetime import datetime,timedelta
import traceback

 #產生log在output
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
                        logging.info(f"======= 成功拿到交易ID{self.trans_id} =======")
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
                    Type=self.response_value_list.get('type')
                    logging.info(f"領到的 configId: {configId}")
                    
                    if configId == '1195064':
                        self.configId_1+=1
                    elif configId == '1195065':
                        self.configId_2+=1
                    elif configId == '1195066':
                        self.configId_3+=1
                    elif configId == '1195067':
                        self.configId_4+=1
                    elif configId == '1195068':
                        self.configId_5+=1
                    elif configId == '1195069':
                        self.configId_6+=1
                    elif configId == '1195070':
                        self.configId_7+=1
                    elif configId == '1195071':
                        self.configId_8+=1
                    

                    logging.info(f"成功領取票卷 交易ID: {self.trans_id} 獎勵 {Trans_id} 類別 {Type}")
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
        success_count=0 #給總領取次數一個初始值
        rewards = {
        "a": {"id": "1195064", "rate": 10.5, "used_up":False, "custom":False},  #把8個獎品的資訊寫在一個dict id 是該獎品的configid rate是中獎機率
        "b": {"id": "1195065", "rate": 12, "used_up":True, "custom":True},      #used_up, custom是自己設的變數 1.用完 2.自訂
        "c": {"id": "1195066", "rate": 5 ,"used_up":True, "custom":True},
        "d": {"id": "1195067", "rate": 5, "used_up":True, "custom":True},
        "e": {"id": "1195068", "rate": 12.5, "used_up":True, "custom":True},
        "f": {"id": "1195069", "rate": 45, "used_up":True, "custom":True},
        "g": {"id": "1195070", "rate": 5, "used_up":True, "custom":True},
        "h": {"id": "1195071", "rate": 5, "used_up":True, "custom":True},
        }
        remaining_rewards = {k: v for k, v in rewards.items() if not v["used_up"]} #根據後端給的邏輯去寫的算法 整句的邏輯是遍歷reward這個字典找到 “used_up" =False的item
        remaining_total=sum(v["rate"] for v in remaining_rewards.values()) #加總remaining_rewards的 "rate" value() 
        try:
            while True: #寫while迴圈而不是for 主要是讓他持續抓trans_id 沒有抓到的話while迴圈就會結束 
                trans_id=self.get_Ticket_transaction_ID()
                if not trans_id:
                    break
                self.approve_to_receive_ticket()
                success_count+=1
                logging.info(f"領取到第{success_count}次\n")
                time.sleep(1)
            if success_count == 0:
                logging.warning("沒有成功領取任何票券")
                return
        except KeyboardInterrupt:
            logging.info("========手動終止程式========")
        id_to_count = {
            "1195064": self.configId_1,
            "1195065": self.configId_2,
            "1195066": self.configId_3,
            "1195067": self.configId_4,
            "1195068": self.configId_5,
            "1195069": self.configId_6,
            "1195070": self.configId_7,
            "1195071": self.configId_8,
        }
        for name,reward in rewards.items():
            prize_id=reward['id']  #這裡是config_id
            hit_count = id_to_count.get(prize_id, 0) #每次中獎次數都會+1並且更新記錄在 id_to_count這個字典
            actual_rate=hit_count/success_count #實際中獎機率=中獎次數/全部獎品總共領取次數

            '''這裡的判斷是根據reward的字典後方兩個"used_up, "custom"的booleam值來判斷 也就是True or False '''
            if not reward["used_up"] and not reward["custom"]: # "used_up, "custom" 都是Fasle =不限制獎品 可參與分配自訂商品抽完後的機率
                average_pass_rate=(reward["rate"]/remaining_total)
                logging.info(f"獎品 {name.upper()} (ID: {prize_id}) - 實際中獎率: {actual_rate:.2%}, 分配後機率: {average_pass_rate:.2%} 領取{hit_count}次")
            elif not reward["used_up"] and reward["custom"]: # "used_up=False, custom=True =自訂商品且有可抽獎的數量 自訂商品不參加分配後的機率 
                average_pass_rate=0
                logging.info("==========自訂獎品不會被分配機率==========")
                logging.info(f"獎品 {name.upper()} (ID: {prize_id}) - 實際中獎率: {actual_rate:.2%}, 分配後機率: {average_pass_rate:.2%} 領取{hit_count}次")
            elif reward["used_up"] and reward["custom"]: # "used_up=True, custom=True =自訂商品且數量=0 自訂商品不參加分配後的機率 
                average_pass_rate=0
                logging.info("==========自訂獎品不會被分配機率==========")
                logging.info(f"獎品 {name.upper()} (ID: {prize_id}) - 實際中獎率: {actual_rate:.2%}, 分配後機率: {average_pass_rate:.2%} 領取{hit_count}次")
        
# 主程式
if __name__ == "__main__":
  
    #填入玩家帳號
    credential = {
        "username": "pop999",
        "password": "123qwe"
    }
    try:    
        frontend = Frontend(credential)
        if frontend.token:  #如果token有效 就執行poccess_all_ticket()函式
            logging.info(f"登入成功 Token: {frontend.token}")
            frontend.poccess_all_ticket()
            
        else:
            logging.error("登入失敗 無法取得Token")
    
    except Exception as e:
        logging.error(f"啟動時發生錯誤: {e}")
        logging.error(traceback.format_exc())

   