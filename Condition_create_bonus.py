import requests,logging,datetime,time
from datetime import datetime,timedelta


def header(token,MerchantCode)->dict:
    return {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Language": "zh_CN",
    "Merchant": MerchantCode,
    "Origin": "http://sit-admin2.tcg.com",
    "Referer": "http://sit-admin2.tcg.com/24785",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "environment": "TCG3",
    "merchantCode": MerchantCode,
    "platform": "TCG"
    }
def cookie():
    return{
        "language": "zh_CN"
    }
def implement_time():
    last_current_time=(datetime.now()- timedelta(days=30)).replace(hour=0,minute=0,second=0,microsecond=0)
    unit_time=str(int(last_current_time.timestamp()*1000))
    end_time = datetime.now().replace(hour=23,minute=59,second=59,microsecond=999999)
    endDate=str(int(end_time.timestamp()*1000))
    return unit_time,endDate
def get_cond_type_function(type):
    configs={
        0:[ #紅利贈送方式：無
            {
            "gamePnlFrom": None,
            "bonusAmt": 10.55,
            "turnoverLimitAmt": 10.55
            }
        ],
        1:[{ #紅利贈送方式：有效投注
            "betAmtFrom": 5,
            "gamePnlFrom": None,
            "bonusAmt": 10.55,
            "turnoverLimitAmt": 10.55
        }],
        2:[{ #紅利贈送方式：存款金額
            "depositAmtFrom": 1000,
            "gamePnlFrom": None,
            "bonusAmt": 10.55,
            "turnoverLimitAmt": 10.55
        }],
        3:[{ #紅利贈送方式：存款次數 
            "depositCntFrom": 5,
            "gamePnlFrom": None,
            "bonusAmt": 10.55,
            "turnoverLimitAmt": 10.55
        }],
        4:[{ #紅利贈送方式：存款次數+存款金額
            "depositCntFrom": 1,
            "depositAmtFrom": 1,
            "gamePnlFrom": None,
            "bonusAmt": 10.55,
            "turnoverLimitAmt": 10.55
        }],
        5:[{ #紅利贈送方式：存款金額+投充比
            "depositAmtFrom": 1,
            "multipleOfBettingAndDeposit": 1,
            "gamePnlFrom": None,
            "bonusAmt": 10.55,
            "turnoverLimitAmt": 10.55
        }],
        7:[{ #紅利贈送方式：玩家盈虧
            "playerProfitFrom": 100,
            "gamePnlFrom": None,
            "bonusAmt": 10.55,
            "turnoverLimitAmt": 10.55
        }],
        8:[{ #紅利贈送方式：統計區間首存
            "depositAmtFrom": 1000,
            "gamePnlFrom": None,
            "bonusAmt": 10.55,
            "turnoverLimitAmt": 10.55
        }],
        9:[{ #紅利贈送方式：遊戲輸贏
            "gamePnlFrom": -10,
            "bonusAmt": 10.55,
            "turnoverLimitAmt": 10.55
        }]
    }
    return configs.get(type, configs[0])
def get_cond_type_function_ratio_without_ticket(type):
    configs={
        0:[ #紅利贈送方式：無
            {
            "gamePnlFrom": None,
            "amtRatio": 15,
            "bonusTurnoverRatio": 1.5
            }
        ],
        1:[{ #紅利贈送方式：有效投注
            "betAmtFrom": 5,
            "gamePnlFrom": None,
            "amtRatio": 1.5,
            "bonusTurnoverRatio": 1.8
        }],
        2:[{ #紅利贈送方式：存款金額
            "depositAmtFrom": 1000,
            "gamePnlFrom": None,
            "amtRatio": 15,
            "bonusTurnoverRatio": 1.9
        }],
        3:[{ #紅利贈送方式：存款次數 
            "depositCntFrom": 5,
            "gamePnlFrom": None,
            "amtRatio": 15,
            "bonusTurnoverRatio": 1.8
        }],
        4:[{ #紅利贈送方式：存款次數+存款金額
            "depositCntFrom": 1,
            "depositAmtFrom": 1,
            "gamePnlFrom": None,
            "amtRatio": 15,
            "bonusTurnoverRatio": 2.5
        }],
        5:[{ #紅利贈送方式：存款金額+投充比
            "depositAmtFrom": 1,
            "multipleOfBettingAndDeposit": 1,
            "gamePnlFrom": None,
            "amtRatio": 15,
            "bonusTurnoverRatio": 4.1
        }],
        7:[{  #紅利贈送方式：玩家盈虧
            "playerProfitFrom": 100,
            "gamePnlFrom": None,
            "amtRatio": 1.5,
            "bonusTurnoverRatio": 7.7
        }],
        8:[{ #紅利贈送方式：統計區間首存
            "depositAmtFrom": 1000,
            "gamePnlFrom": None,
            "amtRatio": 15,
            "bonusTurnoverRatio": 3.5
        }],
        9:[{ #紅利贈送方式：遊戲輸贏
            "gamePnlFrom": -100,
            "amtRatio": 1,
            "bonusTurnoverRatio": 4.5
        }]
    }
    return configs.get(type, configs[0])
def get_cond_type_function_cash_ticket(type):
    configs={
        0:[ #紅利贈送方式：無
            {
            "gamePnlFrom": None,
            "bonusAmt": 1.5,
            "turnoverLimitAmt": 1.5,
            "ticketId": 1129014,
            "ticketQuantity": 1
            }
        ],
        1:[{ #紅利贈送方式：有效投注
            "betAmtFrom": 5,
            "gamePnlFrom": None,
            "bonusAmt": 1.5,
            "turnoverLimitAmt": 1.5,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        2:[{ #紅利贈送方式：存款金額
            "depositAmtFrom": 1000,
            "gamePnlFrom": None,
            "bonusAmt": 1.5,
            "turnoverLimitAmt": 1.5,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        3:[{ #紅利贈送方式：存款次數 
            "depositCntFrom": 5,
            "gamePnlFrom": None,
            "bonusAmt": 1.5,
            "turnoverLimitAmt": 1.5
        }],
        4:[{ #紅利贈送方式：存款次數+存款金額
            "depositCntFrom": 1,
            "depositAmtFrom": 1,
            "gamePnlFrom": None,
            "bonusAmt": 1.5,
            "turnoverLimitAmt": 1.5,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        5:[{ #紅利贈送方式：存款金額+投充比
            "depositAmtFrom": 1,
            "multipleOfBettingAndDeposit": 1,
            "gamePnlFrom": None,
            "bonusAmt": 1.5,
            "turnoverLimitAmt": 1.5,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        7:[{ #紅利贈送方式：玩家盈虧
            "playerProfitFrom": 100,
            "gamePnlFrom": None,
            "bonusAmt": 1.5,
            "turnoverLimitAmt": 1.5,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        8:[{ #紅利贈送方式：統計區間首存
            "depositAmtFrom": 1000,
            "gamePnlFrom": None,
            "bonusAmt": 1.5,
            "turnoverLimitAmt": 1.5,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        9:[{ #紅利贈送方式：遊戲輸贏
            "gamePnlFrom": -100,
            "bonusAmt": 1.5,
            "turnoverLimitAmt": 1.5,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }]
    }
    return configs.get(type, configs[0])
def get_cond_type_function_ratio_with_cash_ticket(type):
    configs={
        0:[ #紅利贈送方式：無
            {
            "gamePnlFrom": None,
            "amtRatio": 15,
            "bonusTurnoverRatio": 1.5,
            "ticketId": 1129014,
            "ticketQuantity": 1
            }
        ],
        1:[{ #紅利贈送方式：有效投注
            "betAmtFrom": 5,
            "gamePnlFrom": None,
            "amtRatio": 1.6,
            "bonusTurnoverRatio": 1.9,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        2:[{ #紅利贈送方式：存款金額 
            "depositAmtFrom": 1000,
            "gamePnlFrom": None,
            "amtRatio": 17,
            "bonusTurnoverRatio": 4.7,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        3:[{ #紅利贈送方式：存款次數 
            "depositCntFrom": 5,
            "gamePnlFrom": None,
            "amtRatio": 38,
            "bonusTurnoverRatio": 3.7,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        4:[{  #紅利贈送方式：存款次數+存款金額
            "depositCntFrom": 1,
            "depositAmtFrom": 1,
            "gamePnlFrom": None,
            "amtRatio": 17,
            "bonusTurnoverRatio": 7.7,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        5:[{ #紅利贈送方式：存款金額+投充比
            "depositAmtFrom": 1,
            "multipleOfBettingAndDeposit": 1,
            "gamePnlFrom": None,
            "amtRatio": 25,
            "bonusTurnoverRatio": 22.9,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        7:[{ #紅利贈送方式：玩家盈虧
            "playerProfitFrom": 100,
            "gamePnlFrom": None,
            "amtRatio": 6.7,
            "bonusTurnoverRatio": 9.9,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        8:[{ #紅利贈送方式：統計區間首存
            "depositAmtFrom": 100,
            "gamePnlFrom": None,
            "amtRatio": 16,
            "bonusTurnoverRatio": 7.9,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }],
        9:[{ #紅利贈送方式：遊戲輸贏
            "gamePnlFrom": -1,
            "amtRatio": 34,
            "bonusTurnoverRatio": 21.9,
            "ticketId": 1129014,
            "ticketQuantity": 1
        }]
    }
    return configs.get(type, configs[0])
def build_common_payload(MerchantCode):
    unit_time, endDate=implement_time()
    return {
    "merchantCode": MerchantCode,
    "specifyDate": True,
    "startDate": unit_time,
    "endDate": endDate,
    "filterPnlData": True,
    "registerRequire": False,
    "registerStart": None,
    "registerEnd": None,
    "specifyNotLoginDate": False,
    "notLoginStartDate": None,
    "notLoginEndDate": None,
    "mobileLinked": False,
    "mobileVerified": False,
    "rankLabels": [],
    "rewardContent": "CASH_VOUCHER_X", #CASH_VOUCHER_X BONUS
    "rewardCalcMethod": "FIXED_BONUS",
    "exclusionType": None,
    "excludeCustomer": [],
    "excludeFileName": None,
    "excludeOperationLabel": [],
    "promotionId": 4023090,
    "appTO": None,
    "customerRemark": "55",
    "internalRemark": "5"
    }
def build_common_payload_deposit_ratio(MerchantCode):
    unit_time, endDate=implement_time()
    return {
    "merchantCode": MerchantCode,
    "specifyDate": True,
    "startDate": unit_time,
    "endDate": endDate,
    "filterPnlData": True,
    "registerRequire": False,
    "registerStart": None,
    "registerEnd": None,
    "specifyNotLoginDate": False,
    "notLoginStartDate": None,
    "notLoginEndDate": None,
    "mobileLinked": False,
    "mobileVerified": False,
    "rankLabels": [],
    "rewardContent": "CASH_VOUCHER_X",#CASH_VOUCHER_X BONUS
    "rewardCalcMethod": "DEPOSIT_RATIO",
    "exclusionType": None,
    "excludeCustomer": [],
    "excludeFileName": None,
    "excludeOperationLabel": [],
    "promotionId": 4023090,
    "appTO": None,
    "customerRemark": "55",
    "internalRemark": "5"
    }
def build_common_payload_profit_ratio(MerchantCode):
    unit_time, endDate=implement_time()
    return {
    "merchantCode": MerchantCode,
    "specifyDate": True,
    "startDate": unit_time,
    "endDate": endDate,
    "filterPnlData": True,
    "registerRequire": False,
    "registerStart": None,
    "registerEnd": None,
    "specifyNotLoginDate": False,
    "notLoginStartDate": None,
    "notLoginEndDate": None,
    "mobileLinked": False,
    "mobileVerified": False,
    "rankLabels": [],
    "rewardContent": "CASH_VOUCHER_X", #CASH_VOUCHER_X
    "rewardCalcMethod": "PROFIT_RATIO",
    "exclusionType": None,
    "excludeCustomer": [],
    "excludeFileName": None,
    "excludeOperationLabel": [],
    "promotionId": 4023090,
    "appTO": None,
    "customerRemark": "55",
    "internalRemark": "5"
    }

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
def get_token():
    login_url="http://sit-admin2.tcg.com/tac/api/login/password"
    payload={
        "operatorName": "carrine03",
        "password": "Test@1234"
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": "",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "http://sit-admin2.tcg.com",
        "Referer": "http://sit-admin2.tcg.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "environment": "",
        "language": "zh_CN",
        "noErrorNotice": "true",
        "platform": ""
    }
    
    cookies = cookie()
    requests_data=requests.post(login_url,json=payload,headers=headers,cookies=cookies,verify=False)
    token_data=requests_data.json()
    return token_data.get("token")

def preview_task(token,MerchantCode:str,type:int):

    API_URL = f"http://sit-admin2.tcg.com/tac/api/relay/post/promo-manual-cond-preview-task" 
    
    payload = build_common_payload_profit_ratio(MerchantCode)
    payload["condType"]=type
    payload["configs"]=get_cond_type_function_ratio_with_cash_ticket(type)
    if type in [1,5,7,9]:
        payload["gameType"]=["rng"]
    headers = header(token,MerchantCode)
    cookies = cookie()
    try:
        response = requests.post(API_URL,json=payload, headers=headers, cookies=cookies, verify=False)
        response.raise_for_status()
            
            
        response_data = response.json()
            
        if response_data.get("success") == True:
            value=response_data.get("value")
            task_id=value["taskId"]
            logging.info(task_id)
            return task_id
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.error(f"條件派發失敗: {error_msg}")
            return False
                
    except requests.RequestException as e:
        logging.error(f"HTTP錯誤 {e}")
        return False
    except ValueError as e:
        logging.error(f"JSON解析錯誤: {e}")
        return False
    except Exception as e:
            logging.error(f"其他錯誤: {e}")
    return False
def create_bonus(token,MerchantCode:str,task_id,type):

    API_URL = f"http://sit-admin2.tcg.com/tac/api/relay/post/promo-manual-cond-approve-claim-task" 
    
    payload =build_common_payload_profit_ratio(MerchantCode)
    payload["configs"]=get_cond_type_function_ratio_with_cash_ticket(type)
    payload["condType"]=type
    payload["taskId"]=task_id
    if type in [1,5,7,9]:
        payload["gameType"]=["rng"]

    headers = headers = header(token,MerchantCode)
    cookies = cookie()
    try:
        response = requests.post(API_URL,json=payload, headers=headers, cookies=cookies, verify=False)
        response.raise_for_status()
        
        
        response_data = response.json()
        
        if response_data.get("success") == True:
            logging.info("條件派發成功")
            return True
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.info(response_data)
            logging.error(f"條件派發失敗: {error_msg}")
            return False
            
    except requests.RequestException as e:
        logging.error(f"HTTP錯誤 {e}")
        return False
    except ValueError as e:
        logging.error(f"JSON解析錯誤: {e}")
        return False
    except Exception as e:
        logging.error(f"其他錯誤: {e}")
        return False


def main():
    try:
        token = get_token()
        print("取得的 token:", token)
    except Exception as e:
        print("啟動時取得 token 發生錯誤:", e)
    MerchantCode="gi8viet"
    condType_list=[0,3,2,4,8,5,1,9,7]
    for type in condType_list:
        task_id=preview_task(token,MerchantCode,type)
        time.sleep(3)
        if task_id:
            isSuccess=create_bonus(token,MerchantCode,task_id,int(type))
            if isSuccess:
                logging.info(f"條件類型 {type} ")
            else:
                logging.warning(f"未找到條件類型")
main()
        



    
        
        

   