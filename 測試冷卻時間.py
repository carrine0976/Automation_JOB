import requests
import logging
import oracledb
from datetime import datetime
import time

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
            
def request_code(customer_id):
    count=0
    URL="http://10.80.1.19:8084/promo-fe/resources/postcard_code/request_code"

    header={
        "Content-Type":"application/json",
        "CustomerId":customer_id,
        "CustomerIP":"100.100.100.100"
    }
    
    resposne=requests.post(URL,headers=header,verify=False)
    endTime=datetime.now()
    logging.info(f"第一次領取後的時間{endTime}")
    count+=1
    resposne_json=resposne.json()
    value=resposne_json.get("value")
    postcardCode=value.get("postcardCode")
    logging.info(postcardCode)
    max_retry=50
    if resposne_json.get("success"):
        for attemp in range(1, max_retry+1):
            time.sleep(1)
            startTime=datetime.now()
            resposne=requests.post(URL,headers=header,verify=False)  
            count+=1
            resposne_json=resposne.json()
            value=resposne_json.get("value")
            postcardCode=value.get("postcardCode")
            if not postcardCode:
                logging.info(postcardCode)
                logging.info(f"第{count}次嘗試領取時間{startTime}")
            else:
                logging.info(postcardCode)
                logging.info(f"最後次嘗試領取時間{startTime}")
                CostTime=startTime-endTime
                logging.info(f"時間間隔{CostTime}")
                break
                
    else:
        logging.error(f"{resposne.text}")


def main():
    customer_id=DB_connect("SELECT CUSTOMER_ID FROM TCG_CORE.US_CUSTOMER WHERE CUSTOMER_NAME='gi8viet@bnm005'")
    request_code(customer_id)
    
main()
