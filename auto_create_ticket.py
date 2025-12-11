import schedule
import time,random
import requests,logging,json
from datetime import datetime,timedelta

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
        "Merchant": "gi8viet",
        "MerchantCode": "gi8viet",
        "Origin": "http://sit-admin2.tcg.com",
        "Referer": "http://sit-admin2.tcg.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "environment": "",
        "language": "zh_CN",
        "noErrorNotice": "true",
        "platform": ""
    }
    
    cookies = {
        "language": "zh_CN"
    }
    requests_data=requests.post(login_url,json=payload,headers=headers,cookies=cookies,verify=False)
    logging.info(f"狀態碼{requests_data.status_code}")
    requests_data.raise_for_status()
    token_data=requests_data.json()
    return token_data.get("token")

def create_ticket_cash(token,ticketname,amount,turnoveramount):
    API_URL = "http://sit-admin2.tcg.com/tac/api/relay/post/promo-ticket-CASH-VOUCHER-create" 
    payload = {
    "merchantCode": "gi8viet",
    "type": "CASH_VOUCHER",
    "status": "ISSUING",
    "defaultLanguage": "CN",
    "turnoverMultiplier": turnoveramount,
    "dayValidity": 30,
    "hourValidity": 0,
    "claimDevice": None,
    "hasRewardTickets": False,
    "rewardTickets": [],
    "configs": [
        {
            "type": "BONUS",
            "winningPercentage": 100,
            "amount": amount
        }
    ],
    "localizations": [
        {
            "language": "CN",
            "name": ticketname,
            "description": None,
            "lossMessage": None,
            "imageUrl": None,
            "imageName": None
        }
    ],
    "effectType": "IMMEDIATE",
    "rewardTicketValidityType": "TICKET_PROMOTION",
    "rewardStrategy": "FIXED",
    "internalRemark": "c",
    "validityType": "DAY_VALIDITY",
    "validMode": "PERIOD_VALIDITY",
    "productType": "ALL",
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

    headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Language": "zh_CN",
    "Merchant": "gi8viet",
    "Origin": "http://sit-admin2.tcg.com",
    "Referer": "http://sit-admin2.tcg.com/24786",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "environment": "TCG3",
    "merchantCode": "gi8viet",
    "platform": "TCG"
    }
    cookies = {
        "language": "zh_CN"
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, cookies=cookies, verify=False)
        
        response_data = response.json()
        
        if response_data.get("success") == True:
            logging.info(f"創建票卷成功 ")
            return True
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.error(f"創建票卷失敗: {error_msg}")
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
def create_ticket_raffle(token,ticketname,min_amount,max_amount,turnoveramount):
    API_URL = "http://sit-admin2.tcg.com/tac/api/relay/post/promo-ticket-RAFFLE-create" 
    payload = {
    "merchantCode": "gi8viet",
    "type": "RAFFLE",
    "status": "ISSUING",
    "defaultLanguage": "CN",
    "turnoverMultiplier": turnoveramount,
    "dayValidity": 30,
    "hourValidity": 0,
    "claimDevice": None,
    "hasRewardTickets": False,
    "rewardTickets": [],
    "configs": [
        {
            "type": "BONUS",
            "winningPercentage": 100,
            "minAmount": min_amount,
            "maxAmount": max_amount
        }
    ],
    "localizations": [
        {
            "language": "CN",
            "name": ticketname,
            "description": None,
            "lossMessage": "you loose",
            "imageUrl": None,
            "imageName": None
        }
    ],
    "effectType": "IMMEDIATE",
    "rewardTicketValidityType": "TICKET_PROMOTION",
    "validityType": "DAY_VALIDITY",
    "validMode": "PERIOD_VALIDITY",
    "productType": "ALL",
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

    headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Language": "zh_CN",
    "Merchant": "gi8viet",
    "Origin": "http://sit-admin2.tcg.com",
    "Referer": "http://sit-admin2.tcg.com/24786",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "environment": "TCG3",
    "merchantCode": "gi8viet",
    "platform": "TCG"
    }
    cookies = {
        "language": "zh_CN"
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, cookies=cookies, verify=False)
        
        response_data = response.json()
        
        if response_data.get("success") == True:
            logging.info(f"創建票卷成功 ")
            return True
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.error(f"創建票卷失敗: {error_msg}")
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
def create_ticket_Egg(token,ticketname,turnoveramount):
    API_URL = "http://sit-admin2.tcg.com/tac/api/relay/post/promo-ticket-GOLDEN-EGG-create" 
    payload = {
    "merchantCode": "gi8viet",
    "type": "GOLDEN_EGG",
    "status": "ISSUING",
    "defaultLanguage": "CN",
    "turnoverMultiplier": turnoveramount,
    "dayValidity": 30,
    "hourValidity": 0,
    "claimDevice": None,
    "hasRewardTickets": False,
    "rewardTickets": [],
    "configs": [
        {
            "winningPercentage": 12.5,
            "type": "BONUS",
            "amount": 5
        },
        {
            "winningPercentage": 12.5,
            "type": "POINT",
            "amount": 5
        },
        {
            "winningPercentage": 12.5,
            "type": "BONUS",
            "amount": 50
        },
        {
            "winningPercentage": 12.5,
            "type": "POINT",
            "amount": 5
        },
        {
            "winningPercentage": 12.5,
            "type": "BONUS",
            "amount": 4
        },
        {
            "winningPercentage": 12.5,
            "type": "POINT",
            "amount": 3
        },
        {
            "winningPercentage": 12.5,
            "type": "BONUS",
            "amount": 2
        },
        {
            "winningPercentage": 12.5,
            "type": "POINT",
            "amount": 1
        }
    ],
    "localizations": [
        {
            "language": "CN",
            "name": ticketname,
            "description": None,
            "lossMessage": "ccccc",
            "imageUrl": None,
            "imageName": None
        }
    ],
    "effectType": "IMMEDIATE",
    "rewardTicketValidityType": "TICKET_PROMOTION",
    "productType": "ALL",
    "validityType": "DAY_VALIDITY",
    "validMode": "PERIOD_VALIDITY",
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

    headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Language": "zh_CN",
    "Merchant": "gi8viet",
    "Origin": "http://sit-admin2.tcg.com",
    "Referer": "http://sit-admin2.tcg.com/24786",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "environment": "TCG3",
    "merchantCode": "gi8viet",
    "platform": "TCG"
    }
    cookies = {
        "language": "zh_CN"
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, cookies=cookies, verify=False)
        
        response_data = response.json()
        
        if response_data.get("success") == True:
            logging.info(f"創建票卷成功 ")
            return True
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.error(f"創建票卷失敗: {error_msg}")
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
def create_ticket_Wheel(token,ticketname,turnoveramount):
    API_URL = "http://sit-admin2.tcg.com/tac/api/relay/post/promo-ticket-PRIZE-WHEEL-create"
    payload = {
        "merchantCode": "gi8viet",
        "type": "PRIZE_WHEEL",
        "status": "ISSUING",
        "defaultLanguage": "CN",
        "turnoverMultiplier": turnoveramount,
        "dayValidity": 30,
        "hourValidity": 0,
        "claimDevice": None,
        "hasRewardTickets": False,
        "rewardTickets": [],
        "configs": [
            {
                "winningPercentage": 12.5,
                "type": "POINT",
                "amount": 6,
                "imageUrl": "",
                "imageName": "",
                "customProductQuantity": None
            },
            {
                "winningPercentage": 12.5,
                "type": "BONUS",
                "amount": 5,
                "imageUrl": "",
                "imageName": "",
                "customProductQuantity": None
            },
            {
                "winningPercentage": 12.5,
                "type": "MERCHANDISE",
                "amount": 0,
                "imageUrl": "https://images.21947392.com/sit-images/ticket/gi8viet/2113085_1751966266669.svg",
                "imageName": "2113085_1751966266669.svg",
                "customProductQuantity": 100,
                "productName": {
                    "CN": "test"
                },
                "productDescription": {
                    "CN": "test"
                }
            },
            {
                "winningPercentage": 12.5,
                "type": "BONUS",
                "amount": 4,
                "imageUrl": "",
                "imageName": "",
                "customProductQuantity": None
            },
            {
                "winningPercentage": 12.5,
                "type": "POINT",
                "amount": 3,
                "imageUrl": "",
                "imageName": "",
                "customProductQuantity": None
            },
            {
                "winningPercentage": 12.5,
                "type": "BONUS",
                "amount": 2,
                "imageUrl": "",
                "imageName": "",
                "customProductQuantity": None
            },
            {
                "winningPercentage": 12.5,
                "type": "POINT",
                "amount": 12,
                "imageUrl": "",
                "imageName": "",
                "customProductQuantity": None
            },
            {
                "winningPercentage": 12.5,
                "type": "POINT",
                "amount": 45,
                "imageUrl": "",
                "imageName": "",
                "customProductQuantity": None
            }
        ],
        "localizations": [
            {
                "language": "CN",
                "name": ticketname,
                "description": None,
                "lossMessage": "c",
                "imageUrl": None,
                "imageName": None
            }
        ],
        "effectType": "IMMEDIATE",
        "rewardTicketValidityType": "TICKET_PROMOTION",
        "validityType": "DAY_VALIDITY",
        "validMode": "PERIOD_VALIDITY",
        "productType": "ALL",
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


    headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Language": "zh_CN",
    "Merchant": "gi8viet",
    "Origin": "http://sit-admin2.tcg.com",
    "Referer": "http://sit-admin2.tcg.com/24786",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "environment": "TCG3",
    "merchantCode": "gi8viet",
    "platform": "TCG"
    }
    cookies = {
        "language": "zh_CN"
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, cookies=cookies, verify=False)
        
        response_data = response.json()
        
        if response_data.get("success") == True:
            logging.info(f"創建票卷成功 ")
            return True
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.error(f"創建票卷失敗: {error_msg}")
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
def create_ticket_Gift(token,ticketname,turnoveramount):
    API_URL = "http://sit-admin2.tcg.com/tac/api/relay/post/promo-ticket-GIFT-CODE-create"
    payload = {
    "merchantCode": "gi8viet",
    "type": "GIFT_CODE",
    "status": "ISSUING",
    "defaultLanguage": "CN",
    "turnoverMultiplier": turnoveramount,
    "dayValidity": 30,
    "hourValidity": 0,
    "claimDevice": None,
    "hasRewardTickets": False,
    "rewardTickets": [],
    "configs": [
        {
            "type": "MERCHANDISE",
            "ticketPrizeId": 63001,
            "winningPercentage": 100
        }
    ],
    "localizations": [
        {
            "language": "CN",
            "name": ticketname,
            "description": "<p>ccc</p>\n",
            "lossMessage": "ccc",
            "imageUrl": None,
            "imageName": None
        }
    ],
    "effectType": "IMMEDIATE",
    "rewardTicketValidityType": "TICKET_PROMOTION",
    "validityType": "DAY_VALIDITY",
    "validMode": "PERIOD_VALIDITY",
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

    headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Language": "zh_CN",
    "Merchant": "gi8viet",
    "Origin": "http://sit-admin2.tcg.com",
    "Referer": "http://sit-admin2.tcg.com/24786",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "environment": "TCG3",
    "merchantCode": "gi8viet",
    "platform": "TCG"
    }
    cookies = {
        "language": "zh_CN"
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, cookies=cookies, verify=False)
        
        response_data = response.json()
        
        if response_data.get("success") == True:
            logging.info(f"創建票卷成功 ")
            return True
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.error(f"創建票卷失敗: {error_msg}")
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
def create_ticket_Free_spin(token,ticketname):
    API_URL = "http://sit-admin2.tcg.com/tac/api/relay/post/promo-ticket-FREE-SPIN-create"
    payload = {
    "merchantCode": "gi8viet",
    "status": "ISSUING",
    "defaultLanguage": "CN",
    "localizations": [
        {
            "language": "CN",
            "name": ticketname,
            "description": "<p>test</p>\n",
            "lossMessage": None,
            "imageUrl": None,
            "imageName": None
        }
    ],
    "claimDevice": None,
    "hasRewardTickets": False,
    "internalRemark": "",
    "type": "FREE_SPIN",
    "rewardStrategy": "FIXED",
    "configs": [
        {
            "type": "FREE_GAME",
            "planId": 1072,
            "freeSpinCount": 4,
            "vendorCode": "JL"
        }
    ],
    "validityType": "FIXED_TIME",
    "fixedTimeFrom": 1751299200000,
    "fixedTimeTo": 1753977599000,
    "claimCondition": {
        "bankCardRequired": False,
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
        "sharedMessage": "欢迎加入 gi8viet越南彩！"
    },
    "rewardTicketValidityType": "TICKET_PROMOTION"
}


    headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Language": "zh_CN",
    "Merchant": "gi8viet",
    "Origin": "http://sit-admin2.tcg.com",
    "Referer": "http://sit-admin2.tcg.com/24786",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "environment": "TCG3",
    "merchantCode": "gi8viet",
    "platform": "TCG"
    }
    cookies = {
        "language": "zh_CN"
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, cookies=cookies, verify=False)
        
        response_data = response.json()
        
        if response_data.get("success") == True:
            logging.info(f"創建票卷成功 ")
            return True
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.error(f"創建票卷失敗: {error_msg}")
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
def create_ticket_temu(token,ticketname,turnoveramount):
    API_URL = "http://sit-admin2.tcg.com/tac/api/relay/post/promo-temu_ticket-add"
    payload = {
    "merchantCode": "gi8viet",
    "defaultLanguage": "CN",
    "localizations": [
        {
            "language": "CN",
            "name": ticketname,
            "description": "<p>test</p>\n",
            "lossMessage": None,
            "imageUrl": None,
            "imageName": None
        }
    ],
    "initScoreConfigId": 1,
    "ticketValidity": {
        "validityType": "DAY_VALIDITY",
        "fixedTimeFrom": 0,
        "fixedTimeTo": 0,
        "effectType": None,
        "dayValidity": 30,
        "hourValidity": 0
    },
    "claimDevice": None,
    "hasRewardTickets": False,
    "targetScore": 1111,
    "ticketTurnover": {
        "turnoverType": "MULTIPLIER",
        "turnoverMultiplier": turnoveramount
    },
    "validMode": "PERIOD_VALIDITY",
    "claimConditions": [
        {
            "scoreConfigId": 1,
            "bankCardRequired": "N",
            "payeeNameRequired": "N",
            "addressRequired": "N",
            "emailRequired": "N",
            "whatsAppRequired": "N",
            "lineRequired": "N",
            "qqRequired": "Y",
            "zaloRequired": "N",
            "wechatRequired": "N",
            "facebookRequired": "N",
            "mobileNumRequired": "N",
            "idNoRequired": "N",
            "mobileNumBound": "N",
            "conditionSelect": [
                "qqRequired"
            ],
            "bankCardTypeRequired": False,
            "depositRequired": "N",
            "paymentMethodRequired": False,
            "requirePaymentMethod": [],
            "depositAmountRequired": False,
            "depositAmountDuration": "AFTER_CLAIM",
            "requireDepositAmount": None,
            "depositCountRequired": False,
            "depositCountDuration": "AFTER_CLAIM",
            "requireDepositCount": None,
            "betRequired": "N",
            "betGameRequired": False,
            "requireBetGameType": "ALL",
            "requireBetGameVendor": "ALL",
            "betAmountRequired": False,
            "betAmountDuration": "AFTER_CLAIM",
            "requireBetAmount": None,
            "negativeProfitRequired": "N",
            "negativeProfitAmountDuration": "AFTER_CLAIM",
            "requireNegativeProfitAmount": None,
            "shareContactRequired": "N",
            "shareContactCount": None,
            "sharedMessage": "欢迎加入 gi8viet越南彩！",
            "sharedDescription": "",
            "inviteFriendsCount": None,
            "inviteeRequired": "N",
            "inviteeCountRequired": False,
            "requireInviteeCount": None,
            "inviteeRewardCount": None,
            "cycleInviteeCountRequired": False,
            "requireCycleInviteeCount": None,
            "cycleInviteeRewardCount": None,
            "cycleTotalInviteeCountRequired": False,
            "requireCycleTotalInviteeCount": None,
            "cycleTotalInviteeRewardCount": None,
            "telegramRequired": "N",
            "viberRequired": "N",
            "appleIdRequired": "N",
            "twitterRequired": "N",
            "birthdayRequired": "N"
        }
    ],
    "rewardTicketValidityType": "TICKET_PROMOTION"
}


    headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Authorization": token,
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Language": "zh_CN",
    "Merchant": "gi8viet",
    "Origin": "http://sit-admin2.tcg.com",
    "Referer": "http://sit-admin2.tcg.com/24786",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "environment": "TCG3",
    "merchantCode": "gi8viet",
    "platform": "TCG"
    }
    cookies = {
        "language": "zh_CN"
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, cookies=cookies, verify=False)
        
        response_data = response.json()
        
        if response_data.get("success") == True:
            logging.info(f"創建票卷成功 ")
            return True
        else:
            error_msg = response_data.get("message", "未知錯誤")
            logging.error(f"創建票卷失敗: {error_msg}")
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
def implement(ticketname_cash,ticketname_raffle,ticketname_egg,ticketname_wheel,ticketname_gift,ticketname_free,ticketname_temu,amount,turnoveramount,min_amount,max_amount):
    token = get_token()
    create_ticket_cash(token,ticketname_cash,amount,turnoveramount)
    create_ticket_raffle(token,ticketname_raffle,min_amount,max_amount,turnoveramount)
    create_ticket_Egg(token,ticketname_egg,turnoveramount)
    create_ticket_Wheel(token,ticketname_wheel,turnoveramount)
    create_ticket_Gift(token,ticketname_gift,turnoveramount)
    create_ticket_Free_spin(token,ticketname_free)
    create_ticket_temu(token,ticketname_temu,turnoveramount)

if __name__ == "__main__":
    try:
        token = get_token()
        print("取得的 token:", token)
        implement()
    except Exception as e:
        print("啟動時取得 token 發生錯誤:", e)
   
    
    
    

   