import logging
from datetime import datetime
import oracledb

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


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
cursor.execute("SELECT * FROM TCG_CORE.US_CUSTOMER WHERE CUSTOMER_NAME='gi8viet@opop1224'")
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
         
    cursor.close()
    conn.close()
except oracledb.DatabaseError as e:
    logging.error(f"❌ 資料庫錯誤: {e}")
except Exception as e:
    logging.error(f"❌ 未預期的錯誤: {str(e)}")
finally:
    if cursor in locals() and cursor:
        cursor.close()
    if conn in locals and conn:
        conn.close()