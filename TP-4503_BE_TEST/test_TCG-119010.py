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

    def GET_EXTRA_REWARD_LIST(self, test_prmo_id: int, merchantCode: str):
        API_URL = "http://10.80.1.20:7001/promo-be/resources/promotion/extra_reward/list?page=1&size=10"
        params = {"page": 1, "size": 10}
        headers = self.header(merchantCode)

        try:
            response = requests.get(API_URL, params=params, headers=headers, verify=False)
            response.raise_for_status()
            response_data = response.json()
            logging.info(response.text)

            if response_data.get("success"):
                value_list = response_data.get("values")
                for item in value_list:
                    extra_promo_id = item.get("id")
                    if extra_promo_id == test_prmo_id:
                        return extra_promo_id
                logging.error("沒有拿到extra_promo_id")
                return None
            else:
                error_msg = response_data.get("message", "未知錯誤")
                logging.error(f"API響應失敗: {error_msg}")
                return None

        except requests.RequestException as e:
            logging.error(f"HTTP錯誤 {e}")
        except ValueError as e:
            logging.error(f"JSON解析錯誤: {e}")
        except Exception as e:
            logging.error(f"其他錯誤: {e}")


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
    "name": "434444",
    "startTime": 1764234900000,
    "endTime": 1764486000000,
    "playerRemark": "testing",
    "internalRemark": "testing",
    "hourValidity": 0,
    "minuteValidity": 2,
    "rewardType": "BONUS",
    "multiplierMode": "FIXED",
    "configReqs": [
        {
            "requireMinDepositAmount": 200,
            "requireMaxDepositAmount": 200,
            "requireMinRewardAmount": 0,
            "requireMaxRewardAmount": 0,
            "rewardMultiplier": 2
        }
    ],
    "turnoverMultiplier": 2,
    "excludeRebate": "N"
}
base_payload_create_fix = {
  "name": "翻倍策略8",
  "startTime": f"{start_time}",
  "endTime": f"{start_time_next_day}",
  "playerRemark": "testing",
  "internalRemark": "testing",
  "hourValidity": 0,
  "minuteValidity": 60,
  "rewardType": "BONUS",
  "multiplierMode": "FIXED",
  "configReqs": [
    {
      "requireMinDepositAmount": 500,
      "requireMaxDepositAmount": 500,
      "requireMinRewardAmount": 0,
      "requireMaxRewardAmount": 0,
      "rewardMultiplier": 3
    }
  ],
  "turnoverMultiplier": 2,
  "excludeRebate": "N"
}
base_payload_create_deposit = {
  "name": "翻倍策略8",
  "startTime": f"{start_time}",
  "endTime": f"{start_time_next_day}",
  "playerRemark": "testing",
  "internalRemark": "testing",
  "hourValidity": 0,
  "minuteValidity": 60,
  "rewardType": "BONUS",
  "multiplierMode": "DEPOSIT_AND_REWARD",
  "configReqs": [
    {
      "requireMinDepositAmount": 0,
      "requireMaxDepositAmount": 500,
      "requireMinRewardAmount": 0,
      "requireMaxRewardAmount": 30,
      "rewardMultiplier": 3
    },
    {
      "requireMinDepositAmount": 501,
      "requireMaxDepositAmount": 600,
      "requireMinRewardAmount": 31,
      "requireMaxRewardAmount": 60,
      "rewardMultiplier": 5
    }
  ],
  "turnoverMultiplier": 2,
  "excludeRebate": "N"
}

test_cases = [
    pytest.param("name", "翻倍", None, None,id="TCG119010.020.020"),
    pytest.param("name", "1225355", None, None,id="TCG119010.020.030"),
    pytest.param("name", "@", None, None,id="TCG119010.020.040"),
    pytest.param("name", "", "name cannot be blank", "missing_required_parameter",id="TCG119010.020.050"),
    pytest.param("playerRemark", "翻倍策略UI測試", None, None,id="TCG119010.020.110"),
    pytest.param("playerRemark", "dsfddwqeqfewfrgrebhhrhtrhrthtrhrtgregccgregregregregrerevrm" * 4, None, None,id="TCG119010.020.120"),
    pytest.param("playerRemark", "dsfddwqeqfewfrgrebhhrhtrhrthtrhrtgregccgregregregregrerevrm" * 5, "remarks_length_exceeded", "remarks_length_exceeded",id="TCG119010.020.130"),
    pytest.param("internalRemark", "34235555", None, None,id="TCG119010.020.140"),
    pytest.param("internalRemark", "@", None, None,id="TCG119010.020.150"),
    pytest.param("playerRemark", "", "playerRemark cannot be blank", "missing_required_parameter",id="TCG119010.020.160"),
    pytest.param("internalRemark", "翻倍策略UI測試", None, None,id="TCG119010.020.170"),
    pytest.param("internalRemark", "dsfddwqeqfewfrgrebhhrhtrhrthtrhrtgregccgregregregregrerevrm" * 4, None, None,id="TCG119010.020.180"),
    pytest.param("internalRemark", "dsfddwqeqfewfrgrebhhrhtrhrthtrhrtgregccgregregregregrerevrm" * 5, "remarks_length_exceeded", "remarks_length_exceeded",id="TCG119010.020.190"),
    pytest.param("internalRemark", "4325664!", None, None,id="TCG119010.020.200"),
    pytest.param("internalRemark", "@#!", None, None,id="TCG119010.020.210"),
    pytest.param("internalRemark", "", None, None,id="TCG119010.020.220"),
    pytest.param("minuteValidity", 0, "invalid_parameter_time_validity", "invalid_parameter_time_validity",id="TCG119010.020.230"),
    pytest.param("minuteValidity", 1, None, None,id="TCG119010.020.240"),
    pytest.param("hourValidity", 1, None, None,id="TCG119010.020.250"),
    pytest.param("hourValidity", -1, "hourValidity: must be greater than or equal to 0", "request_param_err",id="TCG119010.020.260"),
    pytest.param("minuteValidity", -1, "minuteValidity: must be greater than or equal to 0", "request_param_err",id="TCG119010.020.261"),
    pytest.param("rewardType", "POINT", "reward_type_cannot_change", "reward_type_cannot_change",id="TCG119010.060.020"),
    pytest.param("multiplierMode", "DEPOSIT_AND_REWARD", "multiplier_mode_cannot_change", "multiplier_mode_cannot_change",id="TCG119010.060.030"),
    pytest.param("startTime", "1764903634000", "promotion_time_cannot_change", "promotion_time_cannot_change",id="TCG119010.060.040"),
    pytest.param("endTime", "1764903634000", "promotion_time_cannot_change", "promotion_time_cannot_change",id="TCG119010.060.050"),
    pytest.param("configReqs.0.rewardMultiplier", "6.89",None, None,id="TCG119010.060.080"),
    pytest.param("configReqs.0.requireMinDepositAmount", "10.78", "configReqs[0].requireMinDepositAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err"),
    pytest.param("configReqs.0.requireMinDepositAmount", "10.7", "configReqs[0].requireMinDepositAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err"),
    pytest.param("configReqs.0.requireMaxDepositAmount", "300.78", "configReqs[0].requireMaxDepositAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err"),
    pytest.param("configReqs.0.requireMaxDepositAmount", "300.7", "configReqs[0].requireMaxDepositAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err"),
    pytest.param("configReqs.0.requireMinRewardAmount", "300.78", "configReqs[0].requireMinRewardAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err"),
    pytest.param("configReqs.0.requireMinRewardAmount", "300.7", "configReqs[0].requireMinRewardAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err"),
    pytest.param("configReqs.0.requireMaxRewardAmount", "300.78", "configReqs[0].requireMaxRewardAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err"),
    pytest.param("configReqs.0.requireMaxRewardAmount", "300.7", "configReqs[0].requireMaxRewardAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err")
]
test_cases_for_complare=[
    pytest.param("hourValidity", 1, None, None,id="TCG119010.020.250"),
]
test_cases_for_create = [
    pytest.param("name", "翻倍", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.020"),
    pytest.param("name", "1225355", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.030"),
    pytest.param("name", "@", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.040"),
    pytest.param("name", "", "name cannot be blank", "missing_required_parameter","DEPOSIT_AND_REWARD",id="TCG119010.020.050"),
    pytest.param("startTime", f"{start_time}", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.070"),
    pytest.param("startTime", f"{start_time_past_a_day}", "invalid_future_start_time", "invalid_future_start_time","DEPOSIT_AND_REWARD",id="TCG119010.020.080"),
    pytest.param("startTime", f"{start_time_next_day}", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.090"),
    pytest.param("endTime", f"{start_time_past_a_day}", "invalid_end_time", "invalid_end_time","DEPOSIT_AND_REWARD",id="TCG119010.020.100"),
    pytest.param("playerRemark", "翻倍策略UI測試", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.110"),
    pytest.param("playerRemark", "dsfddwqeqfewfrgrebhhrhtrhrthtrhrtgregccgregregregregrerevrm" * 4, None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.120"),
    pytest.param("playerRemark", "dsfddwqeqfewfrgrebhhrhtrhrthtrhrtgregccgregregregregrerevrm" * 5, "remarks_length_exceeded", "remarks_length_exceeded","DEPOSIT_AND_REWARD",id="TCG119010.020.130"),
    pytest.param("internalRemark", "34235555", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.140"),
    pytest.param("internalRemark", "@", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.150"),
    pytest.param("playerRemark", "", "playerRemark cannot be blank", "missing_required_parameter","DEPOSIT_AND_REWARD",id="TCG119010.020.160"),
    pytest.param("internalRemark", "翻倍策略UI測試", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.170"),
    pytest.param("internalRemark", "dsfddwqeqfewfrgrebhhrhtrhrthtrhrtgregccgregregregregrerevrm" * 4, None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.180"),
    pytest.param("internalRemark", "dsfddwqeqfewfrgrebhhrhtrhrthtrhrtgregccgregregregregrerevrm" * 5, "remarks_length_exceeded", "remarks_length_exceeded","DEPOSIT_AND_REWARD",id="TCG119010.020.190"),
    pytest.param("internalRemark", "4325664!", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.200"),
    pytest.param("internalRemark", "@#!", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.210"),
    pytest.param("internalRemark", "", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.220"),
    pytest.param("minuteValidity", 0, "invalid_parameter_time_validity", "invalid_parameter_time_validity","DEPOSIT_AND_REWARD",id="TCG119010.020.230"),
    pytest.param("minuteValidity", 1, None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.240"),
    pytest.param("hourValidity", 1, None, None,"DEPOSIT_AND_REWARD",id="TCG119010.020.250"),
    pytest.param("hourValidity", -1, "hourValidity: must be greater than or equal to 0", "request_param_err","DEPOSIT_AND_REWARD",id="TCG119010.020.260"),
    pytest.param("minuteValidity", -1, "minuteValidity: must be greater than or equal to 0", "request_param_err","DEPOSIT_AND_REWARD",id="TCG119010.020.261"),
    pytest.param("rewardType", "POINT", None, None,"DEPOSIT_AND_REWARD",id="TCG119010.060.080"),
    pytest.param("multiplierMode", "FIXED", None, None,"FIXED",id="TCG119010.060.080"),
    pytest.param("configReqs.0.rewardMultiplier", "6.89",None, None,"DEPOSIT_AND_REWARD",id="TCG119010.060.080"),
    pytest.param("configReqs.0.requireMinDepositAmount", "10.78", "configReqs[0].requireMinDepositAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err","DEPOSIT_AND_REWARD"),
    pytest.param("configReqs.0.requireMinDepositAmount", "10.7", "configReqs[0].requireMinDepositAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err","DEPOSIT_AND_REWARD"),
    pytest.param("configReqs.0.requireMaxDepositAmount", "300.78", "configReqs[0].requireMaxDepositAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err","DEPOSIT_AND_REWARD"),
    pytest.param("configReqs.0.requireMaxDepositAmount", "300.7", "configReqs[0].requireMaxDepositAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err","DEPOSIT_AND_REWARD"),
    pytest.param("configReqs.0.requireMinRewardAmount", "300.78", "configReqs[0].requireMinRewardAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err","DEPOSIT_AND_REWARD"),
    pytest.param("configReqs.0.requireMinRewardAmount", "300.7", "configReqs[0].requireMinRewardAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err","DEPOSIT_AND_REWARD"),
    pytest.param("configReqs.0.requireMaxRewardAmount", "300.78", "configReqs[0].requireMaxRewardAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err","DEPOSIT_AND_REWARD"),
    pytest.param("configReqs.0.requireMaxRewardAmount", "300.7", "configReqs[0].requireMaxRewardAmount: numeric value out of bounds (<10 digits>.<0 digits> expected)", "request_param_err","DEPOSIT_AND_REWARD")
]

@pytest.mark.parametrize("field_path,bad_value,expected_msg,expected_code,multiplier_mode", test_cases_for_create)
def test_CREATE_EXTRA_REWARD(backend, merchant_code, field_path, bad_value, expected_msg, expected_code,multiplier_mode):
    if multiplier_mode=="FIXED":
        test_copy = copy.deepcopy(base_payload_create_fix)
    else:
        test_copy = copy.deepcopy(base_payload_create_deposit)
    backend.set_value(test_copy, field_path, bad_value)
    logging.info(f"=== 執行測試：{field_path}")
    API_URL2 = "http://10.80.1.20:7001/promo-be/resources/promotion/extra_reward"
    headers = backend.header(merchant_code)

    
    response = requests.post(API_URL2, headers=headers, json=test_copy, verify=False)
    response_data = response.json()

    if response.status_code == 200:
        response_error_message = response_data.get('message')
        response_error_code = response_data.get('errorCode')
        if response_data.get("success") is True:
            assert response_error_message is None and response_error_code is None,f"預期錯誤:msg={expected_msg}"
        else:
            assert response_error_message == expected_msg and response_error_code == expected_code, \
                f"訊息: {response_error_message}, 錯誤碼: {response_error_code}"
    else:
        error_msg = response_data.get("message", "未知錯誤")
        logging.error(f"{error_msg}")
        
@pytest.mark.parametrize("field_path,bad_value,expected_msg,expected_code", test_cases)
def test_UPDATE_EXTRA_REWARD(backend, merchant_code, field_path, bad_value, expected_msg, expected_code):
    test_copy = copy.deepcopy(base_payload_update)
    backend.set_value(test_copy, field_path, bad_value)
    logging.info(f"=== 執行測試：{field_path}")
    API_URL2 = "http://10.80.1.20:7001/promo-be/resources/promotion/extra_reward/4290133"
    headers = backend.header(merchant_code)

    
    response = requests.put(API_URL2, headers=headers, json=test_copy, verify=False)
    response_data = response.json()

    if response.status_code == 200:
        response_error_message = response_data.get('message')
        response_error_code = response_data.get('errorCode')
        if response_data.get("success") is True:
            assert response_error_message is None and response_error_code is None,f"預期錯誤:msg={expected_msg}"
        else:
            assert response_error_message == expected_msg and response_error_code == expected_code, \
                f"訊息: {response_error_message}, 錯誤碼: {response_error_code}"
    else:
        error_msg = response_data.get("message", "未知錯誤")
        logging.error(f"{error_msg}")
        
@pytest.mark.parametrize("field_path,bad_value,expected_msg,expected_code", test_cases)
def test_COMPARE_DEPOSIT_AMOUNT(backend, merchant_code, field_path, bad_value, expected_msg, expected_code):
    test_copy = copy.deepcopy(base_payload_update)
    backend.set_value(test_copy, field_path, bad_value)
    logging.info(f"=== 執行測試：{field_path}")
    API_URL2 = "http://10.80.1.20:7001/promo-be/resources/promotion/extra_reward/4290133"
    headers = backend.header(merchant_code)

    
    response = requests.put(API_URL2, headers=headers, json=test_copy, verify=False)
    response_data = response.json()

    if response.status_code == 200:
        response_error_message = response_data.get('message')
        response_error_code = response_data.get('errorCode')
        if response_data.get("success") is True:
            assert response_error_message is None and response_error_code is None,f"預期錯誤:msg={expected_msg}"
        else:
            assert response_error_message == expected_msg and response_error_code == expected_code, \
                f"訊息: {response_error_message}, 錯誤碼: {response_error_code}"
    else:
        error_msg = response_data.get("message", "未知錯誤")
        logging.error(f"{error_msg}")
        


   