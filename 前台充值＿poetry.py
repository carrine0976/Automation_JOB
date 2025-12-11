import requests
import logging
import time
from datetime import datetime,timedelta
import urllib3
import os
import yaml
from datetime import datetime
import oracledb
import random
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
def DB_connect(SQL):
    host="10.80.1.11"
    port = 1521              
    service_name = "tcgsit"
    username = "TCG_MCSDB"
    password = "Jv7UrDc7rsqJ87Km"

    dsn=f"{host}:{port}/{service_name}"

    conn=oracledb.connect(
        user=username,
        password=password,
        dsn=dsn
    )
    cursor=conn.cursor()
    cursor.execute(f"{SQL}")
    rows=cursor.fetchall()
    try:
        if rows:
            colums=[]
            for desc in cursor.description:
                colums.append(desc[0])
            for row in rows:
                print("="*60)
                print("資訊")
                print("="*60)
                for col,val in zip(colums,row):
                    if isinstance(val,datetime):
                        val_str=val.strftime('%Y-%m-%d %H:%M:%S')
                    elif val==" ":
                        val_str='(空白)'
                        
                    elif val is None:
                        val_str='NULL'
                        
                    else:
                        val_str=str(val)
                    
                    print(f"{col:25s}: {val_str}")
                    
        else:
            logging.info("查無資料")
        return str(rows[0][0])
            
    except oracledb.DatabaseError as e:
        logging.error(f"❌ 資料庫錯誤: {e}")
    except Exception as e:
        logging.error(f"❌ 未預期的錯誤: {str(e)}")
    finally:
        if cursor in locals() and cursor:
            cursor.close()
        if conn in locals() and conn:
            conn.close()
def get_claim_id(CustomerId):
    try:
        CustomerIP=".".join(str(random.randint(0,255)) for _ in range(4))
        URL="http://10.80.1.19:8084/promo-fe/resources/extra_reward/claim_list/unapplied"
        header={
            "accept":"application/json",
            "CustomerIP":CustomerIP,
            "CustomerId":CustomerId
        }
        response=requests.get(URL,headers=header,verify=False)
        response_json=response.json()
        if response_json.get("success"):
            value=response_json.get("value")
            claim_list=value.get("claims",[])
            if not claim_list  :
                logging.error("拿到空 cliam_list")
                return None
            else :
                claim_id=claim_list[0].get("claimId")
                if claim_id is not None:
                    logging.info(f"拿到cliam_id:{claim_id}")
                    return claim_id
                else:
                    logging.error("沒有拿到cliam_id")
                    return None
            
            
    except Exception as e:
            logging.error(f"系統錯誤{e}")
            
class Frontend:
    def __init__(self,credential:dict):
        self.session=requests.Session()
        self.username=''
        self.userid=''
        self.credential=credential
        self.token=None
        self.token_expire=None
        self.token=self.get_token_login(credential['username'],credential['password'])
        self.type=''
    def get_token_login(self, username, password):
        try:

            if self.token is not None and self.token_expire is not None and datetime.now()<self.token_expire:
                return self.token
            
            login_url='http://www.sit2.sit-gi8viet.com/wps/session/login/unsecure'
            
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
            return self.token
        
        except requests.RequestException as e:
            logging.error(f"請求失敗{e}")
            return None
    def is_token_valid(self):
        
        return (self.token is not None and 
                self.token_expire is not None and 
                datetime.now() < self.token_expire)
    
        
    def deposit_QAD(self,username,amount):
        success_fail=0
        success_count=0

        
        if not self.is_token_valid():
            logging.info("token 過期, 重新登入")
            self.get_token_login(self.credential['username'],self.credential['password'])
        if self.token is None:
            return
        current_time=datetime.now()
        unit_time=str(int(current_time.timestamp()*1000))
        login_URL="http://www.sit-gi8viet.com/wps/relay/MCSFE_depositByQRImageUrl"

        headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Merchant': 'gi8viet',
            "Authorization":self.token,
            'Connection': 'keep-alive',
            'Language': 'EN',
            'Origin': 'http://www.sit-gi8viet.com',
            'Referer': 'http://www.sit-gi8viet.com/',
            'ModuleId': 'DPSTBAS3',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',  
            'x-timestamp': unit_time     
        }
        customer_id=DB_connect(f"SELECT CUSTOMER_ID FROM TCG_CORE.US_CUSTOMER WHERE CUSTOMER_NAME='gi8viet@{username}'")
        promoClaimId=get_claim_id(customer_id)
        payload={
            "targetUsername": username,
            "amount":amount,
            "bankCode": "SS For Modify Bank",
            "bankType": "BTC",
            "showQrImageOnly":1,
            "vendorId":29089,
            "deviceId": "b3422fd0-9519-47cf-a03d-6bce63e25885",
            "mcsBankCode": "SS For Modify Bank",
            "token":self.token,
            "promotionId":4308094,
            "promoClaimId":promoClaimId
        }
        cookies={
            'SHELL_deviceId': '8c5bdbd3-b2cd-b350-4c4e-5967bb9d7966',
        }
        
        response=self.session.post(login_URL,headers=headers,json=payload,cookies=cookies,verify=False)
        response_json=response.json()
        
        if response_json.get('success'):
            logging.info("成功充值 交易ID")
            success_count+=1
            
        else:
            logging.error("充值失敗")
            success_fail+=1
        time.sleep(1)
        
class Backend:
    def __init__(self, credential: dict):
        self.credential = credential
        self.token = self.get_token()
        
    def header(self,merchantCode):
        return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": self.token,
        "Connection": "keep-alive",
        "Language": "zh_CN",
        "Merchant": merchantCode,
        "Origin": "http://sit-admin2.tcg.com",
        "Referer": "http://sit-admin2.tcg.com/20000",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "environment": "TCG3",
        "merchantCode": merchantCode,
        "platform": "TCG"
        }
    def get_token(self):
        login_url = "http://sit-admin2.tcg.com/tac/api/login/password"
        payload = {
            "operatorName": self.credential['operatorName'],
            "password": self.credential['password']
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": "",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "http://sit-admin2.tcg.com",
            "Referer": "http://sit-admin2.tcg.com/",
        }
        cookies = {
            "language": "zh_CN"
        }
        response = requests.post(login_url, json=payload, headers=headers, cookies=cookies, verify=False)
        token_data = response.json()
        self.token = token_data.get("token")
        return self.token  
    def deposit(self,test_username,merchantCode):
        API_URL = "http://sit-admin2.tcg.com/tac/api/relay/get/mcs-player-deposit-search" 
        start_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")
        end_time = datetime.now().strftime("%Y-%m-%d 23:59:59")
        params={
            "username":"",
            "depositId":"",
            "bankRef":"",
            "depositStatus":"",
            "amountFromStr":"",
            "amountToStr":"",
            "depositType":"",
            "bankAcctIdList":"",
            "searchDateMode":"requestTime",
            "dateFrom":start_time,
            "dateTo":end_time,
            "tcpBankCode":"",
            "merchantCode":merchantCode,
            "pageNo":1,
            "pageSize":1000

            }

        headers = self.header(merchantCode)
        cookies = {
            "language": "zh_CN"
        }
        try:
            response = requests.get(API_URL, headers=headers,params=params, cookies=cookies, verify=False)
            response.raise_for_status()
            
            
            response_data = response.json()
            
            if response_data.get('success') :
                logging.info("搜尋充值id成功: ")
                value_list=response_data.get('value',[])
                for value in value_list:
                    if value["username"]==test_username:
                        return value["depositId"]  
            else:
                error_msg = response_data.get("message", "未知錯誤")
                logging.error(f"搜尋充值對象失敗: {error_msg}")
                return []
            
        except Exception as e:
            logging.error(f"狀態碼: {response.status_code}",e)
            return []
    def approve_deposit(self,deposit_Info,merchantCode):
        try:
            API_URL="http://sit-admin2.tcg.com/tac/api/relay/post/mcs-v3-deposit-processAndApprove"
            if deposit_Info.get("requestAmount") is None:
                logging.error(f"充值ID: {deposit_Info['depositId']} 缺少存款金額，無法處理")
                return False
            payload={
            
            "depositId": deposit_Info["depositId"],
            "tpRefNo": None,
            "payerBankAcctName": None,
            "payerBankAcctNum": None,
            "depositAmount": deposit_Info.get("requestAmount"),
            "bankRef":deposit_Info.get("bankRef"),
            "operatorRemark": None,
            "internalRemark": None,
            "version": 1,
            "merchantCode":merchantCode,
            "isProcessAndApprove": True
            }
            headers = self.header(merchantCode)
            cookies = {
            "language": "zh_CN"
            }
            response=requests.post(API_URL, json=payload,cookies=cookies,verify=False, headers=headers)
            response_data = response.json()

            if response_data.get('success'):
                logging.info(f"成功批准ID: {deposit_Info['depositId']} , 金額: {deposit_Info['requestAmount']}")
                return True
            else:
                logging.info(f"未成功批准ID: {deposit_Info["depositId"]}")
                return False
        except Exception as e:
            logging.error(f"處理充值 ID: {deposit_Info['depositId']} 時發生錯誤: {e}")
            return False
def procedure():
        merchantCode='gi8viet'
        password = "123qwe"
       
        current_dir=os.path.dirname(__file__)
        yaml_path=os.path.join(current_dir,"config_poetry.yaml")
        with open(yaml_path,"r",encoding="utf-8") as f:
            config=yaml.safe_load(f)
        testing_account=config.get("testing_account")
        
        for username, deposit_info in testing_account.items():

            print("正在處理帳號:", username)

            credential = {
            "username": username,
            "password": password
            }
            credential_be = {"operatorName": "carrine03", "password": "Test@1234"}
            try:
                frontend = Frontend(credential)
                if frontend.token:
                    first_amount=deposit_info.get("first_depost")
                    second_amount=deposit_info.get("second_depost")
                    third_amount=deposit_info.get("third_depost")
                    four_amount=deposit_info.get("four_depost")
                    five_amount=deposit_info.get("five_depost")
                    if first_amount:
                        frontend.deposit_QAD(credential['username'],first_amount)
                        backend=Backend(credential_be)
                        if backend.token:
                            deposit_id=backend.deposit(username,merchantCode)
                            backend.approve_deposit(deposit_id,merchantCode)
                        
                        time.sleep(1)
                    if second_amount:
                        frontend.deposit_QAD(credential['username'],second_amount)
                        time.sleep(1)
                    if third_amount:
                        frontend.deposit_QAD(credential['username'],third_amount)
                        time.sleep(1)
                    if four_amount:
                        frontend.deposit_QAD(credential['username'],four_amount)
                        time.sleep(1)
                    if five_amount:
                        frontend.deposit_QAD(credential['username'],five_amount)
                        time.sleep(1)
            
            except Exception as e:
                logging.error(f"系統錯誤{e}")
        time.sleep(2)


def main():
    procedure()
main()