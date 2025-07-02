import requests,logging,schedule,time
from datetime import datetime,timedelta
from urllib.parse import urlparse, parse_qs


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
    
    def Launch_Sport_game_FB(self):
        if not self.is_token_valid():
            logging.info("token 過期, 重新登入")
            self.get_token_login(credential['username'],credential['password'])
        if self.token is None:
            return
        login_URL=f"http://www.sit-gi8viet.com/wps/game/launchGame?gameId=FB0001&nodeId=1605492&accountType=1&confirmTrans=0&vassalage=FB&launchMode=GLS&platform=html5-desktop&clientType=3&language=VI&merchantCode=gi8viet"

        headers={
            'Content-Type': 'application/json',
            'Merchant': 'gi8viet',
            "Authorization":self.token,
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept':'application/json, text/plain, */*',
            'Connection':'keep-alive',
            'Device':'Web',
            'Language':'VI',
            


        }
        
        cookies={
            'tcg-sid': 'c8900c3c-b2be-4995-b05a-b5567fd9683e',
            'SHELL_deviceId': '45fcebb4-8393-f955-97e3-9820a7899b78',
        }
        
        response=self.session.get(login_URL,headers=headers,cookies=cookies)
        response.raise_for_status()
        response_json=response.json()
        
        if response_json.get('success') == True:
            
            game_url = None
            
            if 'content' in response_json:
                content = response_json['content']
                if isinstance(content, dict) and 'game_url' in content:
                    game_url = content['game_url']
                    logging.info(f"Found game_url in content: {game_url}")
                    return game_url
                else :
                    logging.error("沒有拿到game_url")
                    return None
        else:
            logging.error(f"系統錯誤")
            return None
        
    def search_game(self,url):
        
        login_URL=f"{url}"
        FB_SPORT=self.session.get(login_URL)
        parsed_url=urlparse(url)
        query_string=parsed_url.fragment
        query_prams=parse_qs(query_string)
        token=query_prams.get('token',[None])[0]
        if not token:
            logging.error("無法取得token")
            return
        Bet_Url="https://app-2.server.st-newsports.com/v1/order/bet/singlePass"

        header={
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "authorization": token,
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://pc.st-newsports.com",
            "priority": "u=1, i",
            "referer": "https://pc.st-newsports.com/",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "cookie": "JSESSIONID=4B87448BD5CB256F186A32616DD604E3"


        }
        payload = {
            "languageType": "ENG",
            "singleBetList": [
            {
                "unitStake": 100,
                "oddsChange": 1,
                "betOptionList": [
                    {
                        "marketId": 7322220,
                        "odds": 2.44,
                        "optionType": 1,
                        "oddsFormat": 1
                        }
                    ]
                }
            ],
            "currencyId": 1
        }


        
        response=self.session.post(Bet_Url,headers=header,json=payload)
        response_json=response.json()
        if response_json.get('success')==True:
            logging.info(f"成功投注體育 ")
            
        else:
            logging.error(f"投注失敗")
            
if __name__ == "__main__":
  
    #填入玩家帳號
    credential = {
        "username": "rrr362",
        "password": "123qwe"
    }
    try:    
        frontend = Frontend(credential)
        if frontend.token:
            logging.info(f"登入成功 Token: {frontend.token}")
            game_url=frontend.Launch_Sport_game_FB()
            if game_url:
                frontend.search_game(game_url)
            else:
                logging.error("沒有拿到game_url")
            
        else:
            logging.error("登入失敗 無法取得Token")
    
    except Exception as e:
        logging.error(f"啟動時發生錯誤: {e}")

   