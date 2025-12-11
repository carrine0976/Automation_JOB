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
            "merchantCode": merchantCode,
        }

    def set_value(self, payload, field_path, value):
        keys = field_path.split(".")
        temp = payload
        for k in keys[:-1]:
            if k.isdigit():
                temp = temp[int(k)]
            else:
                temp = temp.get(k, {})
        last_key = keys[-1]
        if last_key.isdigit():
            temp[int(last_key)] = value
        else:
            temp[last_key] = value
    def get_ticket_id(self,merchantCode="gi8viet"):
        URL="http://sit-admin2.tcg.com/tac/api/relay/get/promo-ticket-CASH-VOUCHER-list-get"
        header=self.header(merchantCode)
        params={
            "page":1,
            "size":10,
            "merchantCode":"gi8viet",
            "status":"ISSUING"
        }
        response=requests.get(URL,params=params,headers=header,verify=False)
        response_data=response.json()
        if response_data.get("success"):
            value=response_data.get("values")
            first_item_id=value[0].get("id")
            logging.info(f"創建票券id={first_item_id}")
            return first_item_id
        else:
            logging.error(f"沒有拿到id:{response.status_code}")
            return None


@pytest.fixture(scope="module")
def backend():
    credential = {"operatorName": "carrine03", "password": "Test@1234"}
    return Backend(credential)


@pytest.fixture
def merchant_code():
    return "gi8viet"

start_time = datetime.now()
start_time_past_a_day=(datetime.now()-timedelta(days=1))
start_time_next_day=(datetime.now()+timedelta(days=1))


base_payload_create ={
    "merchantCode": "gi8viet",
    "type": "CASH_VOUCHER",
    "status": "ISSUING",
    "defaultLanguage": "CN",
    "turnoverMultiplier": 0,
    "dayValidity": 1,
    "hourValidity": 0,
    "claimDevice": None,
    "hasRewardTickets": False,
    "rewardTickets": [],
    "configs": [
        {
            "type": "BONUS",
            "winningPercentage": 100,
            "amount": 1
        }
    ],
    "localizations":[{
                
            "language": "CN",
            "name": "CASH_005",
            "description": None,
            "lossMessage": None,
            "imageUrl": None,
            "imageName": None
        
            }],
    "effectType": "IMMEDIATE",
    "rewardTicketValidityType": "TICKET_PROMOTION",
    "rewardStrategy": "FIXED",
    "extraRewardPromotionId": None,
    "internalRemark": "c",
    "validityType": "DAY_VALIDITY",
    "validMode": "PERIOD_VALIDITY",
    "productType": "RNG_OR_LIVE",
    "fixedTimeFrom": None,
    "fixedTimeTo": None,
    "claimCondition": {
        "bankCardRequired": False,
        "bankCardTypeRequired": False,
        "requireBankCardType": [],
        "payeeNameRequired": False,
        "addressRequired": False,
        "emailRequired": False,
        "whatsAppRequired": False,
        "lineRequired": False,
        "qqRequired": False,
        "zaloRequired": False,
        "wechatRequired": False,
        "facebookRequired": False,
        "telegramRequired": False,
        "viberRequired": False,
        "appleIdRequired": False,
        "twitterRequired": False,
        "birthdayRequired": False,
        "mobileNumRequired": False,
        "idNoRequired": False,
        "depositRequired": False,
        "turnoverRequired": False,
        "negativeProfitRequired": False,
        "shareContactRequired": False,
        "inviteFriendsRequired": False,
        "depositAmountRequired": False,
        "paymentMethodRequired": False,
        "requirePaymentMethod": [],
        "depositAmountDuration": "AFTER_CLAIM",
        "requireDepositAmount": 0,
        "depositCountRequired": False,
        "depositCountDuration": "AFTER_CLAIM",
        "requireDepositCount": 0,
        "minTurnoverRequired": False,
        "minTurnoverAmt": 0,
        "minTurnoverDuration": "AFTER_CLAIM",
        "gameRequired": False,
        "gameType": "ALL",
        "gameVendor": "ALL",
        "negativeProfitDuration": "AFTER_CLAIM",
        "negativeProfitAmount": 0,
        "inviteFriendsCount": 0,
        "sharedMessage": "欢迎加入 gi8viet越南彩！",
        "shareContactCount": 0
    }
}
test_cases = [
    pytest.param("extraRewardPromotionId","4294092", None, None,id="TCG120280.010.050"),
    
]


@pytest.mark.parametrize("field_path,test_value,expected_msg,expected_code", test_cases)
def test_CREATE_TICKET_BACKEND(backend, merchant_code, field_path, test_value, expected_msg, expected_code):

    test_copy = copy.deepcopy(base_payload_create)
    backend.set_value(test_copy, field_path, test_value)
    logging.info(f"=== 執行測試：{field_path}")
    API_URL2 = "http://10.80.1.20:7001/promo-be/resources/ticket/CASH_VOUCHER"
    headers = backend.header(merchant_code)

    
    response = requests.post(API_URL2, headers=headers, json=test_copy, verify=False)
    response_data = response.json()

    if response.status_code == 200:
        response_error_message = response_data.get('message')
        response_error_code = response_data.get('errorCode')
        actual_extra_id=response_data.get("value").get("extraRewardPromotionId")
        expect_value=4294092
        if response_data.get("success") is True:
            assert actual_extra_id ==expect_value,f"預期錯誤:msg={expected_msg}"
        '''else:
            assert response_error_message == expected_msg and response_error_code == expected_code, \
                f"訊息: {response_error_message}, 錯誤碼: {response_error_code}" '''
    else:
        error_msg = response_data.get("message", "未知錯誤")
        logging.error(f"{error_msg}")
        
@pytest.mark.parametrize("field_path,test_value,expected_msg,expected_code", test_cases)
def test_CREATE_TICKET_FRONTEND(backend, merchant_code, field_path, test_value, expected_msg, expected_code):
    
    test_copy = copy.deepcopy(base_payload_create)
    backend.set_value(test_copy, field_path, test_value)
    logging.info(f"=== 執行測試：{field_path}")
    API_URL2 = "http://sit-admin2.tcg.com/tac/api/relay/post/promo-ticket-CASH-VOUCHER-create"
    headers = backend.header(merchant_code)

    
    response = requests.post(API_URL2, headers=headers, json=test_copy, verify=False)
    response_data = response.json()

    if response.status_code == 200:
        response_error_message = response_data.get('message')
        response_error_code = response_data.get('errorCode')
        actual_extra_id=response_data.get("value").get("extraRewardPromotionId")
        expect_value=4294092
        if response_data.get("success") is True:
            assert actual_extra_id ==expect_value,f"預期錯誤:msg={expected_msg}"
        '''else:
            assert response_error_message == expected_msg and response_error_code == expected_code, \
                f"訊息: {response_error_message}, 錯誤碼: {response_error_code}" '''
    else:
        error_msg = response_data.get("message", "未知錯誤")
        logging.error(f"{error_msg}")
        
def test_CHECK_TICKET(backend, merchant_code):
    
    ticket_id=backend.get_ticket_id()
    logging.info(f"=== 執行測試 查看票券：{ticket_id}")
    API_URL2 = f"http://sit-admin2.tcg.com/tac/api/relay/get/promo-ticket-CASH-VOUCHER-get/{ticket_id}"
    headers = backend.header(merchant_code)

    
    response = requests.get(API_URL2, headers=headers, verify=False)
    response_data = response.json()

    if response.status_code == 200:
        response_error_message = response_data.get('message')
        response_error_code = response_data.get('errorCode')
        actual_extra_id=response_data.get("value").get("extraRewardPromotionId")
        expect_value=4294092
        logging.info(f"拿到的extra_id:{actual_extra_id}")
        if response_data.get("success") is True:
            assert actual_extra_id ==expect_value,"預期錯誤:"
        '''else:
            assert response_error_message == expected_msg and response_error_code == expected_code, \
                f"訊息: {response_error_message}, 錯誤碼: {response_error_code}" '''
    else:
        error_msg = response_data.get("message", "未知錯誤")
        logging.error(f"{error_msg}")


   