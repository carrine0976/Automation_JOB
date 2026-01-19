import requests
import logging
import copy
import pytest
from datetime import datetime,timedelta
from unittest.mock import patch
import requests
import time

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
            "Cookie":"language=zh_CN",
            "Referer":"http://sit-admin2.tcg.com/24781",
            "Origin":"http://sit-admin2.tcg.com",
            "customTimezone": "Etc/GMT-8"
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

base_payload_update = {
    "promotionId": 4338133,
    "monthlyCountLimit": 300,
    "dailyCountLimit":None,
    "weeklyCountLimit":None,
    "cooldownMinutes": 1,
    "cooldownSeconds": 0,
    "mobileVerified": "N",
    "idRequired": "N",
    "kycRequired": "Y",
    "excludeRebate": "N",
    "bonusAmount": 11.05,
    "pointAmount": 25.55,
    "requiredTurnover": 3.5,
    "claimMethod": "REQUEST",
    "codeEffectiveTime": 5,
    "ruleEnabled": "Y",
    "defaultLang": "CN",
    "ruleLocales": [
        {
            "langCode": "CN",
            "title": "ccc",
            "content": "<p>ccc</p>\n"
        }
    ]
}


CLAIM_EXPIRED_ID = 34139652
CLAIM_CLAIMED_ID = 34140749
CLAIM_REJECTED_ID = 34140519

postcard_payload={
    "claimId": 34138652,
    "remark": "x",
    "status": "A"
}


test_cases = [
    
    pytest.param("bonusAmount", 3.987, "[BONUS_AMOUNT_SCALE_EXCEEDED] max: 2", "bonus_amount_scale_exceeded",id="TCG122553.010.070"),
    pytest.param("pointAmount", 3.987, "[POINT_AMOUNT_SCALE_EXCEEDED] max: 2", "point_amount_scale_exceeded",id="TCG122553.010.080"),
    pytest.param("requiredTurnover", 3.98, "[REQUIRED_TURNOVER_SCALE_EXCEEDED] max: 1", "required_turnover_scale_exceeded",id="TCG122553.010.090"),
    pytest.param("promotionId", 543454, "postcard_code_setting_not_found", "postcard_code_setting_not_found",id="TCG122553.010.100"),
    pytest.param("cooldownMinutes", 4, "cooldown_time_minimum_required", "cooldown_time_minimum_required",id="TCG122553.010.120"),
    pytest.param("cooldownSeconds", 65, "postcard_code_invalid_cooldown_time", "postcard_code_invalid_cooldown_time",id="TCG122553.010.110"),
    pytest.param("monthlyCountLimit", None, "postcard_code_count_limit_required", "postcard_code_count_limit_required",id="TCG122553.010.130"),
    pytest.param("monthlyCountLimit", -1, "postcard_code_invalid_count_limit", "postcard_code_invalid_count_limit",id="TCG122553.010.150"),
    pytest.param("dailyCountLimit", -1, "postcard_code_invalid_count_limit", "postcard_code_invalid_count_limit",id="TCG122553.010.160"),
    pytest.param("weeklyCountLimit", -1, "postcard_code_invalid_count_limit", "postcard_code_invalid_count_limit",id="TCG122553.010.170"),
    pytest.param("codeEffectiveTime", -2, "postcard_code_invalid_code_effective_time", "postcard_code_invalid_code_effective_time",id="TCG122553.010.180"),
    pytest.param("codeEffectiveTime", 400, "[EFFECTIVE_TIME_EXCEEDS_MAX_LIMIT] max: 365", "postcard_code_effective_time_exceeds_max_limit",id="TCG122553.010.190"),
    pytest.param("codeEffectiveTime", 0, "postcard_code_invalid_code_effective_time", "postcard_code_invalid_code_effective_time",id="TCG122553.010.200"),
    pytest.param("bonusAmount", -1, "postcard_code_invalid_bonus_amount", "postcard_code_invalid_bonus_amount",id="TCG122553.010.210"),
    pytest.param("pointAmount", -1, "postcard_code_invalid_point_amount", "postcard_code_invalid_point_amount",id="TCG122553.010.220"),
    pytest.param("requiredTurnover", -1, "postcard_code_invalid_required_turnover", "postcard_code_invalid_required_turnover",id="TCG122553.010.230"),
    
    ]

test_case_for_postcard_available = [
    
    pytest.param("claimId", "34139652", "postcard_code_expired", "postcard_code_expired",id="TCG122553.010.270"),
    pytest.param("claimId", "34140749", "[POSTCARD_CODE_CLAIMED] postcard code claimed", "postcard_code_claimed",id="TCG122553.010.280"),
    pytest.param("claimId", "34140519", "[POSTCARD_CODE_CLAIMED] postcard code claimed", "postcard_code_claimed",id="TCG122553.010.290"),
    
]


@pytest.mark.parametrize("field_path,bad_value,expected_msg,expected_code", test_cases)
def test_postCard(backend, merchant_code, field_path, bad_value, expected_msg, expected_code):
    test_copy = copy.deepcopy(base_payload_update)
    
    if field_path == "dailyCountLimit":
        test_copy.pop("monthlyCountLimit", None)
        test_copy.pop("weeklyCountLimit", None)  
    elif field_path == "weeklyCountLimit":
        test_copy.pop("monthlyCountLimit", None)
        test_copy.pop("dailyCountLimit", None)  
    elif field_path == "monthlyCountLimit":
        test_copy.pop("dailyCountLimit", None)   
        test_copy.pop("weeklyCountLimit", None)  
        if bad_value == 2:  
            test_copy["dailyCountLimit"] = 1
    logging.info(f"=== 測試 {field_path} ===")
    logging.info(f"測試值: {bad_value}")
    logging.info(f"payload before set: {test_copy}")
    backend.set_value(test_copy, field_path, bad_value)
    logging.info(f"payload after set: {test_copy}")
    print(field_path)
    logging.info(f"=== 執行測試：{field_path}")
    API_URL2 = "http://sit-admin2.tcg.com/tac/api/relay/put/promo-promotion-postcard-code-setting?pid=247813"
    headers = backend.header(merchant_code)

    
    response = requests.put(API_URL2, headers=headers, json=test_copy, verify=False)
    response_data = response.json()

    if response.status_code == 200:
        response_error_message = response_data.get('message')
        response_error_code = response_data.get('errorCode')
        if response_data.get("success") is True:
            print(response_error_message,response_error_code,expected_msg)
            assert response_error_message is None and response_error_code is None,f"預期錯誤:msg={expected_msg}"
        else:
            print(response_error_message,response_error_code,expected_msg)
            assert response_error_message == expected_msg and response_error_code == expected_code, \
                f"訊息: {response_error_message}, 錯誤碼: {response_error_code}"
    else:
        error_msg = response_data.get("message", "未知錯誤")
        logging.error(f"{error_msg}")
        
@pytest.mark.parametrize("payload,expected_msg,expected_code", 
    [pytest.param(
        {
            
    "promotionId": 4338133,
    "dailyCountLimit": 300,
    "cooldownMinutes": 1,
    "cooldownSeconds": 0,
    "mobileVerified": "N",
    "idRequired": "N",
    "kycRequired": "Y",
    "excludeRebate": "N",
    "bonusAmount": 11.05,
    "pointAmount": 25.55,
    "requiredTurnover": 3.5,
    "claimMethod": "REQUEST",
    "codeEffectiveTime": 5,
    "ruleEnabled": "Y",
    "defaultLang": "CN",
    "ruleLocales": [
        {
            "langCode": "CN",
            "title": None,
            "content": "<p>ccc</p>\n"
        }
    ]

        },
        "postcard_code_rule_locales_required",
        "postcard_code_rule_locales_required",
        id="TCG122553.010.240"
    ),
        pytest.param(
         {
   
    "promotionId": 4338133,
    "dailyCountLimit": 300,
    "cooldownMinutes": 1,
    "cooldownSeconds": 0,
    "mobileVerified": "N",
    "idRequired": "N",
    "kycRequired": "Y",
    "excludeRebate": "N",
    "bonusAmount": 11.05,
    "pointAmount": 25.55,
    "requiredTurnover": 3.5,
    "claimMethod": "REQUEST",
    "codeEffectiveTime": 5,
    "ruleEnabled": "Y",
    "defaultLang": None,
    "ruleLocales": [
        {
            "langCode": "CN",
            "title": "ccc",
            "content": "<p>ccc</p>\n"
        }
    ]

},              "postcard_code_default_lang_required",
                "postcard_code_default_lang_required",
                id="TCG122553.010.250"
        ),
])
def test_local(backend, merchant_code,payload, expected_msg, expected_code):
    
    API_URL2 = "http://sit-admin2.tcg.com/tac/api/relay/put/promo-promotion-postcard-code-setting?pid=247813"
    headers = backend.header(merchant_code)

    
    response = requests.put(API_URL2, headers=headers, json=payload, verify=False)
    response_data = response.json()

    if response.status_code == 200:
        response_error_message = response_data.get('message')
        response_error_code = response_data.get('errorCode')
        if response_data.get("success") is True:
            print(response_error_message,response_error_code,expected_msg)
            assert response_error_message is None and response_error_code is None,f"預期錯誤:msg={expected_msg}"
        else:
            print(response_error_message,response_error_code,expected_msg)
            assert response_error_message == expected_msg and response_error_code == expected_code, \
                f"訊息: {response_error_message}, 錯誤碼: {response_error_code}"
    else:
        error_msg = response_data.get("message", "未知錯誤")
        logging.error(f"{error_msg}")
        
@pytest.mark.parametrize("field_path,bad_value,expected_msg,expected_code", test_case_for_postcard_available)
def test_postCard_verified(backend, merchant_code, field_path, bad_value, expected_msg, expected_code):
    test_copy = copy.deepcopy(postcard_payload)

    backend.set_value(test_copy, field_path, bad_value)
    logging.info(f"=== 執行測試：{field_path}")
    API_URL2 = "http://sit-admin2.tcg.com/tac/api/relay/put/promo-promotion-postcard-code-claim-approve?pid=247815"
    headers = backend.header(merchant_code)
    params={
        "pid":247815
    }
    
    response = requests.put(API_URL2, headers=headers, params=params,json=test_copy, verify=False)
    response_data = response.json()

    if response.status_code == 200:
        response_error_message = response_data.get('message')
        response_error_code = response_data.get('errorCode')
        if response_data.get("success") is True:
            print(response_error_message,response_error_code,expected_msg)
            assert response_error_message is None and response_error_code is None,f"預期錯誤:msg={expected_msg}"
        else:
            print(response_error_message,response_error_code,expected_msg)
            assert response_error_message == expected_msg and response_error_code == expected_code, \
                f"訊息: {response_error_message}, 錯誤碼: {response_error_code}"
    else:
        error_msg = response_data.get("message", "未知錯誤")
        logging.error(f"{error_msg}")


        




   