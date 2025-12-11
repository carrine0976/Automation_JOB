import requests
import logging
import copy
import pytest
from datetime import datetime,timedelta


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Backend:
    def __init__(self, credential: dict):
        self.credential = credential
        self.token = self.get_token()

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

    def header(self, merchantCode):
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": self.token,
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Language": "zh_CN",
            "Merchant": merchantCode,
            "Tac-Trace-Id":"COHI4gPAYq0$uU6b",
            "Referer":"http://sit-admin2.tcg.com/24783",
            "platform": "TCG",
            "Tac-Trace-Id": "COHI4gPAYq0$uU6b",
            "merchantCode":merchantCode,
            "environment":"TCG3",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }
    def set_value(self, params:dict, field:str, test_value):
        params[field]=test_value
        return params
            
start_time = datetime.now()
start_time_past_a_day=(datetime.now()-timedelta(days=1))
start_time_next_day=(datetime.now()+timedelta(days=1))
start_t = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
end_dt = start_time.replace(hour=23, minute=59, second=59, microsecond=0)       

params_status_ALL={
        "relayDisableEncode":True,
        "periodType":"CLAIM_PERIOD",
        "startDate":int(start_t.timestamp()*1000),
        "endDate":int(end_dt.timestamp()*1000),
        "page":1,
        "size":10
    }
params_customerName={
        "relayDisableEncode":True,
        "customerName":"bdd901",
        "periodType":"CLAIM_PERIOD",
        "startDate":int(start_t.timestamp()*1000),
        "endDate":int(end_dt.timestamp()*1000),
        "page":1,
        "size":10
    }

params_status={
        "relayDisableEncode":True,
        "periodType":"CLAIM_PERIOD",
        "startDate":int(start_t.timestamp()*1000),
        "endDate":int(end_dt.timestamp()*1000),
        "status":"P",
        "page":1,
        "size":10
    }
params_upperAgentName={
        "relayDisableEncode":True,
        "upperAgentName":"bnm555",
        "periodType":"CLAIM_PERIOD",
        "startDate":int(start_t.timestamp()*1000),
        "endDate":int(end_dt.timestamp()*1000),
        "status":"P",
        "page":1,
        "size":10
    }
params_promoName={
        "relayDisableEncode":True,
        "promoName":"test",
        "periodType":"CLAIM_PERIOD",
        "startDate":int(start_t.timestamp()*1000),
        "endDate":int(end_dt.timestamp()*1000),
        "status":"P",
        "page":1,
        "size":10
    }


@pytest.fixture(scope="module")
def backend():
    credential = {"operatorName": "carrine03", "password": "Test@1234"}
    return Backend(credential)


@pytest.fixture
def merchant_code():
    return "gi8viet"


test_cases = [
    pytest.param("customerName", "bdd801",None,None,None,id="TCG1126050.010"),
    pytest.param("customerName", "bdd8",None,None,None,id="TCG1126050.020"),
    pytest.param("periodType", "DISTRIBUTE_PERIOD",None,None,None,id="TCG1126050.030"),
    pytest.param("periodType", "CLAIM_PERIOD",None,None,None,id="TCG1126050.040"),
    pytest.param("status", "A",None,None,None,id="TCG1126050.050"),
    pytest.param("status", "R",None,None,None,id="TCG1126050.060"),
    pytest.param("status", "I",None,None,None,id="TCG1126050.070"),
    pytest.param("status", "V",None,None,None,id="TCG1126050.080"),
    pytest.param("status", "E",None,None,None,id="TCG1126050.090"),
    pytest.param("upperAgentName", "cj",None,None,None,id="TCG1126050.100"),
    pytest.param("upperAgentName", "bnm555",None,None,None,id="TCG1126050.110"),
    pytest.param("promoName", "cs",None,None,None,id="TCG1126050.120"),
    pytest.param("promoName", "3092 直接到帳",None,None,None,id="TCG1126050.130"),

]

@pytest.mark.parametrize("field_path,test_value,status,upperAgentName,promoName", test_cases)
def test_Search_Claim_history(backend, merchant_code, field_path, test_value,status,upperAgentName,promoName):
    if field_path=="status":
        test_copy = copy.deepcopy(params_status)
    elif field_path=="upperAgentName":
        test_copy = copy.deepcopy(params_upperAgentName)
    elif field_path=="promoName":
        test_copy = copy.deepcopy(params_promoName)
    elif field_path=="customerName":
        test_copy = copy.deepcopy(params_customerName)
    elif field_path=="periodType":
        test_copy = copy.deepcopy(params_status_ALL)
        
    logging.info(f"=== 執行測試：{field_path}")
    backend.set_value(test_copy,field_path,test_value)
    if field_path=="status":
        if test_value=="R" or "I" or "V" or "E" :
            test_copy["periodType"]="DISTRIBUTE_PERIOD"
        else:
            test_copy["periodType"]="CLAIM_PERIOD"
    logging.info(f"{test_copy}")
    API_URL2 = "http://sit-admin2.tcg.com/tac/api/relay/get/promo-promotion-savior-claim-history"
    headers = backend.header(merchant_code)
    logging.info(f"test_value:{test_value}")
    
    Cookie={
        "language":"zh_CN"
        }
    logging.info(f"{int(start_t.timestamp()*1000)}")
    response = requests.get(API_URL2, headers=headers,params=test_copy,cookies=Cookie, verify=False)
    response_data = response.json()
    assert response.status_code == 200,f"{response.status_code}"
    if response_data.get("success"):
        values=response_data.get("values",[])
        totalElement=int(response_data.get("totalElements",0))
        
        if totalElement >0 :
            value=values[0]
            customer_name=value.get("customerName")
            test_status=value.get("status")
            upperAgent=value.get("upperAgent")
            promotionName=value.get("promoName")
            
            if field_path=="periodType":
                assert len(values)>0
                logging.info(f"僅檢查 有搜索到資料{response_data}")
            else:
                logging.info(f"精確搜索 有搜索到資料{customer_name}{test_status}{upperAgent}{promotionName}")
                assert customer_name== test_value or test_status==test_value or upperAgent==test_value or promotionName==test_value
                
        else:
            logging.info(f"精確搜索故 沒有搜索到資料{response_data}")
            assert values == []
               
    else:
    
        error_msg = response_data.get("message", "未知錯誤")
        pytest.fail(f"API 調用失敗：{error_msg} )")
        logging.error(f"{error_msg}")
        


   