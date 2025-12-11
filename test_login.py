import requests,logging,time
from datetime import datetime,timedelta
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
        self.reward_id=''
        self.promotion_type=''
    def get_token_login(self, username, password):
        try:

            if self.token is not None and self.token_expire is not None and datetime.now()<self.token_expire:
                return self.token
            
            login_url='http://www.sit-huamei.com/wps/session/login/unsecure'
            
            headers = {
                'Content-Type': 'application/json',
                'Merchant': 'huamei',
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
    def test_logout(self):
        logout_url='http://www.sit-huamei.com/wps/session/logout/unsecure'
            
        headers = {
                'Content-Type': 'application/json',
                'Merchant': 'huamei',
            }
        
        self.session.delete(logout_url,headers=headers)
        logging.info("登出成功")
    

if __name__ == "__main__":
  
    try:   
        for _ in range(20):
            credential = {
                "username": "bob111",
                "password": "qwe123"
            } 
            time.sleep(2)
            frontend = Frontend(credential)
            if frontend.token:
                logging.info(f"登入成功 Token: {frontend.token}")
                frontend.test_logout()
            
            
            else:
                logging.error("登入失敗 無法取得Token")
    
    except Exception as e:
        logging.error(f"啟動時發生錯誤: {e}")

   