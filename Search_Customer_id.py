import requests,logging,datetime
from datetime import datetime
import yaml,os,sys
import oracledb

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
class Backend:
    def __init__(self,credentail:dict):
        self.credential=credentail
        self.token=self.get_token()

    def get_token(self):
        login_url="http://sit-admin2.tcg.com/tac/api/login/password"
        payload={
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
        token_data=requests_data.json()
        self.token=token_data.get("token")
        return self.token


    def DB_connect(self,SQL):
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
        

    def procedure(self,username):
        try:
            
            customer_id=self.DB_connect(f"SELECT CUSTOMER_ID FROM TCG_CORE.US_CUSTOMER WHERE CUSTOMER_NAME='gi8viet@{username}'")
            return customer_id

        except Exception as e:
            logging.error(e)
        except KeyboardInterrupt:
            print("退出程式")
            sys.exit()

def main_batch(memeber_list):
        credential = {
        "operatorName": "carrine03",
        "password": "Test@1234"
        }
        try:
            b_end=Backend(credential)
            customerid_list=[]
            if b_end.token:
                for member in memeber_list:
                    customerid=b_end.procedure(member)
                    customerid_list.append(customerid)
                return customerid_list

        except Exception as e:
            logging.error(e)

            
        

   