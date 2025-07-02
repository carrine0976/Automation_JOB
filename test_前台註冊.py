import requests,logging,schedule,time
from datetime import datetime,timedelta

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

    def get_token_login(self, username, password):
        try:

            if self.token is not None and self.token_expire is not None and datetime.now()<self.token_expire:
                return self.token
            
            login_url='http://www.sit-gi8viet.com/wps/member/register/unsecure'
            
            headers = {
                'Content-Type': 'application/json',
                'Merchant': 'gi8viet',
                
            }
            register_data={
                'username':username,
                'password':password
            } 
            
            requests_data=self.session.put(login_url,json=register_data,headers=headers)
            print(requests_data.text)
            self.username = requests_data.json()['value']['userName']
            self.userid = requests_data.json()['value']['id']
            self.token=requests_data.json()['value']['token']

            return self.token
        
        except requests.RequestException as e:
            logging.error(f"請求失敗{e}")
            return None
    def is_token_valid(self):
        
        return (self.token is not None and 
                self.token_expire is not None and 
                datetime.now() < self.token_expire)
        
    
if __name__ == "__main__":
  
    #填入玩家帳號
    credential = {
        "username": "ttt676",
        "password": "123qwe"
    }
    
    try:    
        frontend = Frontend(credential)
        if frontend.token:
            logging.info(f"註冊成功 Token: {frontend.token}")
            #frontend.click_promo_code()
            #schedule.every().day.at(f"{run_time}").do(frontend.click_promo_code,promo)
            
        else:
            logging.error("註冊失敗 ")
    
    except Exception as e:
        logging.error(f"啟動時發生錯誤: {e}")
        

   