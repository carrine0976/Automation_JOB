import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def Change_Password(customer_id:str):
    URL="http://10.80.1.22:7001/tcg-uss-ae/password"

    header={
        "Content-Type":"application/json"
    }
    payload={ 
        "customerId": customer_id, 
        "needLogInToChangePassword": True, 
        "password": "123qwe"
        }
    resposne=requests.put(URL,headers=header,json=payload,verify=False)
    resposne_json=resposne.json()
    if resposne_json.get("success"):
        logging.info("更改密碼完成")
    else:
        logging.error(f"更改失敗{resposne.text}")

def get_customer_id(MerchantCode,Account):
    
    URL=f"http://10.80.1.20:7001/promo-fe/resources/version/auto_qa/get_customer_id?merchant={MerchantCode}&customerName={Account}"
    
    response=requests.get(URL,verify=False)
    
    resposne_text=int(response.text)
    if resposne_text:
        logging.info("拿到id")
        logging.info(resposne_text)
        return resposne_text
    else:
        logging.error(f"沒有拿到id{response.text}")
        return None
        
def main():
    MerchantCode="gi8viet"
    Account=str(input("輸入帳號"))
    customer_id=get_customer_id(MerchantCode,Account)
    Change_Password(customer_id)
    
main()
