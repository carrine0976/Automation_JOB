import requests,logging,schedule,time
from datetime import datetime,timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
class Frontend:
    def __init__(self,credential:dict,PromoCode_list:list):
        self.session=requests.Session()
        self.username=''
        self.userid=''
        self.credential=credential
        self.token=None
        self.token_expire=None
        self.token=self.get_token_login(credential['username'],credential['password'])
        self.promo_list=PromoCode_list
        self.promo=''
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
        
    def click_promo_code(self,promo):
        if not self.is_token_valid():
            logging.info("token 過期, 重新登入")
            self.get_token_login(self.credential['username'],self.credential['password'])
        if self.token is None:
            return
        current_time=datetime.now()
        unit_time=str(int(current_time.timestamp()*1000))
        login_URL="http://www.sit-gi8viet.com/wps/relay/PROMOFE_claimPromoCode"
        headers={
            'Content-Type': 'application/json',
            'X-Timestamp':unit_time,
            "Authorization":self.token,
            'Connection': 'keep-alive',
            'Language': 'VI',
            'Merchant': 'gi8viet',
            'Origin': 'http://www.sit-gi8viet.com',
            'Referer': 'http://www.sit-gi8viet.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        payload={
             "promoCode": self.promo
        }
        
        cookies = {
            '_ga': 'GA1.1.343769134.1743155195',
            'SHELL_deviceId': '9248aea2-32ed-4b1a-afa9-d039ed6d1b95',
            '_ga_ABCD123456789': 'GS1.1.1743388368.2.1.1743390818.0.0.0'
        }
        response = self.session.post(login_URL, headers=headers, json=payload, cookies=cookies)
        response.raise_for_status()
        response_json=response.json()
        print("API Response:", response.text)

        if response_json.get('success')==True:
            logging.info(f"領取優惠碼成功 當前時間{current_time}")
            return True
        else:
            logging.error(f"領取優惠碼失敗")
            return False
    
    def proccess_all_promoCode(self):
        success_count=0
        for promo in self.promo_list:
            if self.click_promo_code(promo):
                success_count+=1
                logging.info(f"共{len(self.promo_list)}組優惠碼, 領取{success_count}組成功")
        time.sleep(1)
if __name__ == "__main__":
  
    #填入玩家帳號
    credential = {
        "username": "ggg444",
        "password": "123qwe"
    }
    PromoCode_list=['HEOOOMY2J','BNOCZQ7CFM','O7KKKH']
    run_time="12:19"
    try:    
        frontend = Frontend(credential,PromoCode_list)
        if frontend.token:
            logging.info(f"登入成功 Token: {frontend.token}")
            #frontend.click_promo_code()
            #schedule.every().day.at(f"{run_time}").do(frontend.click_promo_code,promo)
            frontend.proccess_all_promoCode()
            
            
        else:
            logging.error("登入失敗 無法取得Token")
    
    except Exception as e:
        logging.error(f"啟動時發生錯誤: {e}")
        

   