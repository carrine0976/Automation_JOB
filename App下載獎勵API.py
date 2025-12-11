import requests
import logging
import random
from Search_Customer_id import main_batch

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def appDowload(CustomerId:str,CustomerName,Merchant,CustomerIP,uuid):
    URL="http://10.80.1.19:7001/tcg-mcs-fe/appDownloadPromotion/claimAppDownloadPromotion"

    header={
        "CustomerId":str(CustomerId),
        "CustomerName":CustomerName,
        "Merchant":Merchant,
        "CustomerIP":CustomerIP,
        "Language":"CN"
    }
    payload={ 
        "uuid": uuid 
        }
    print(CustomerId,CustomerName,Merchant,CustomerIP,uuid)
    resposne=requests.post(URL,headers=header,json=payload,verify=False)
    resposne_json=resposne.json()
    if resposne_json.get("success"):
        logging.info("app下載獎勵觸發完成")
    else:
        logging.error(f"觸發失敗{resposne.text}")

def main():
    while True:
        n=int(input("選擇平台 1.gi8 2.huamei 3.tcgdemov3 4.lodibet \n"))
        if n==1:
            Merchant="gi8viet"
            CustomerName=str(input("CustomerName:"))
            CustomerId=(main_batch(CustomerName,Merchant))
            
            CustomerIP=".".join(str(random.randint(0,255)) for _ in range(4))
            uuid=random.randint(100000000, 999999999)
            
            appDowload(CustomerId,CustomerName,Merchant,CustomerIP,uuid)
        elif n==2:
            Merchant="huamei"
            CustomerName=str(input("CustomerName:"))
            CustomerId=main_batch(CustomerName,Merchant)
            
            CustomerIP=".".join(str(random.randint(0,255)) for _ in range(4))
            uuid=random.randint(100000000, 999999999)
            
            appDowload(CustomerId,CustomerName,Merchant,CustomerIP,uuid)
        elif n==3:
            Merchant="tcgdemov3"
            CustomerName=str(input("CustomerName:"))
            CustomerId=(main_batch(CustomerName,Merchant))

            CustomerIP=".".join(str(random.randint(0,255)) for _ in range(4))
            uuid=random.randint(100000000, 999999999)
        
            appDowload(CustomerId,CustomerName,Merchant,CustomerIP,uuid)
        elif n==4:
            Merchant="lodibet"
            CustomerName=str(input("CustomerName:"))
            CustomerId=(main_batch(CustomerName,Merchant))
            
            CustomerIP=".".join(str(random.randint(0,255)) for _ in range(4))
            uuid=random.randint(100000000, 999999999)
        
            appDowload(CustomerId,CustomerName,Merchant,CustomerIP,uuid)
        
main()

