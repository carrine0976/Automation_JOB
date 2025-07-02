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
        self.configId_counters = {
            '1195069': 0,  
            '1195070': 0,  
            '1195071': 0,  
            '1195066': 0, 
            '1195067': 0,  
            '1195064': 0,  
            '1195065': 0,  
            '1195068': 0, 
        }
        
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
            response_json = requests_data.json()
            
            self.username = response_json['value']['userName']
            self.userid = response_json['value']['id']
            self.token = response_json['value']['token']

            self.token_expire=datetime.now()+timedelta(minutes=25)
            logging.info(f"token 將在{self.token_expire}過期 ")
            return self.token
        
        except requests.RequestException as e:
            logging.error(f"請求失敗{e}")
            return None
        except KeyError as e:
            logging.error(f"登入回應格式錯誤: {e}")
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
            return None
            
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
        
        try:
            response=self.session.get(login_URL,headers=headers,cookies=cookies)
            response.raise_for_status()
            response_json=response.json()
            
            if response_json.get('success')==True:
                self.response_value_list=response_json.get('value',[])
                if self.response_value_list:
                    self.response_value_info=self.response_value_list[0]
                    Trans_id=self.response_value_info.get('transactionId') 
                    Condition_status=self.response_value_info.get('conditionStatus',[])
                    if Trans_id and not Condition_status:
                        self.trans_id=Trans_id
                        logging.info(f"成功拿到交易ID: {self.trans_id}")
                        return self.trans_id
                return None
            else:
                logging.error(f"交易ID查詢失敗: {response_json}")
                return None
        
        except requests.exceptions.RequestException as e:
            logging.error(f"get_Ticket_transaction_ID 失敗: {e}")
            return None
    
    def approve_to_receive_ticket(self):
        if not self.is_token_valid():
            logging.info("token 過期, 重新登入")
            self.get_token_login(self.credential['username'],self.credential['password'])
        if self.token is None:
            return False
            
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
        
        try:
            response=self.session.post(login_URL,headers=headers,json=payload,cookies=cookies)
            response_json=response.json()
            
            if response_json.get('success')==True:
                response_value=response_json.get('value')
                if response_value:
                    # Fixed: Get configId correctly
                    configId=str(response_value.get('configId'))
                    reward_value = response_value.get('value')  # This might be the actual reward
                    
                    logging.info(f"領到的 configId: {configId}, 獎勵值: {reward_value}")
                    
                    # Update counter using the dictionary
                    if configId in self.configId_counters:
                        self.configId_counters[configId] += 1
                        logging.info(f"ConfigId {configId} 計數更新為: {self.configId_counters[configId]}")
                    else:
                        logging.warning(f"configId: {configId}")

                    logging.info(f"成功領取票卷 交易ID: {self.trans_id}")
                    return True
                else:
                    logging.error("回應中沒有 value 欄位")
                    return False
            else:
                logging.error(f"領取票卷失敗: {response_json}")
                return False
                
        except Exception as e:
            logging.error(f"領取票卷失敗: {e}")
            logging.error(traceback.format_exc())
            return False
    
    def process_all_ticket(self):
        success_count=0
        rewards = {
            "a": {"id": "1195069", "rate": 12.5, "used_up":False, "custom":False},
            "b": {"id": "1195070", "rate": 12.5, "used_up":False, "custom":False},
            "c": {"id": "1195071", "rate": 12.5, "used_up":False, "custom":False},
            "d": {"id": "1195066", "rate": 12.5, "used_up":False, "custom":False},
            "e": {"id": "1195067", "rate": 12.5, "used_up":False, "custom":False},
            "f": {"id": "1195064", "rate": 12.5, "used_up":True, "custom":False},
            "g": {"id": "1195065", "rate": 12.5, "used_up":False, "custom":False},
            "h": {"id": "1195068", "rate": 12.5, "used_up":False, "custom":False},
        }
        
        remaining_rewards = {k: v for k, v in rewards.items() if not v["used_up"] and not v["custom"]}
        remaining_total=sum(v["rate"] for v in remaining_rewards.values())
        
        logging.info(f"開始領取票券流程，可領取獎品總機率: {remaining_total}%")
        
        try:
            while True:
                trans_id=self.get_Ticket_transaction_ID()
                if not trans_id:
                    logging.info("沒有更多可領取的票券")
                    break
                    
                if self.approve_to_receive_ticket():
                    success_count+=1
                    logging.info(f"領取到第{success_count}次")
                else:
                    logging.error("領取失敗，跳出循環")
                    break
                    
                time.sleep(1)

        except KeyboardInterrupt:
            logging.info("手動終止程式")

        if success_count == 0:
            logging.warning("沒有成功領取任何票券")
            return
        
        # Display results
        logging.info(f"(總共領取 {success_count} 次)")
        
        # Calculate total available rate (excluding used_up items)
        available_rewards = {k: v for k, v in rewards.items() if not v["used_up"]}
        total_available_rate = sum(v["rate"] for v in available_rewards.values())
        
        for name, reward in rewards.items():
            prize_id = reward['id']
            hit_count = self.configId_counters.get(prize_id, 0)
            actual_rate = (hit_count / success_count) * 100 if success_count > 0 else 0
            
            if not reward["used_up"]:
                # Calculate expected rate based on available rewards only
                expected_rate = (reward["rate"] / total_available_rate) * 100 if total_available_rate > 0 else 0
                expected_rate_str = f"{expected_rate:.2f}%"
            else:
                expected_rate_str = "0.00% (已用完)"

            logging.info(f"獎品 {name.upper()} (ID: {prize_id}) - 實際中獎率: {actual_rate:.2f}%, 預期機率: {expected_rate_str}, 領取 {hit_count} 次")
        
        # Summary
        total_claimed = sum(self.configId_counters.values())
        if total_claimed != success_count:
            logging.warning(f"計數不符: 總領取次數 {success_count}, 計數總和 {total_claimed}")

if __name__ == "__main__":
    # 填入玩家帳號
    credential = {
        "username": "pop777",
        "password": "123qwe"
    }
    
    try:    
        frontend = Frontend(credential)
        if frontend.token:
            logging.info(f"登入成功 Token: {frontend.token}")
            frontend.process_all_ticket()  # Fixed method name
        else:
            logging.error("登入失敗 無法取得Token")
    
    except Exception as e:
        logging.error(f"啟動時發生錯誤: {e}")
        logging.error(traceback.format_exc())