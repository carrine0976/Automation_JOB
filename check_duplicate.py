import pandas as pd

def check_duplicate(file_path, sheet_name='sheet1'):

    df=pd.read_excel(file_path,sheet_name=sheet_name)

    full_dupes=df[df.duplicated(keep=False)]
    if  not full_dupes.empty:
        print(f"找到重複資料 {len(full_dupes)}組")
        print(full_dupes)
    else:
        print("沒有完全重複的資料")
    
    if df['订单号'].nunique()==len(df):
        print("每筆訂單號都是唯一")
    else:
        print(f"有重複訂單號 {len(full_dupes)}組")
        print(df[df.duplicated(subset=["订单号"], keep=False)][["订单号", "用户名", "活动名称"]])

file_path=r"gi8viet_20251015100128_玩家红利派发记录 - Wed Oct 15 10_01_22 2025_part1_1.xlsx"
check_duplicate(file_path)



'''
    subset_dupes=df[df.duplicated(subset=["用户名", "活动名称"],keep=False)]
    if  not subset_dupes.empty:
        print("找到重複資料")
        print(subset_dupes)
    else:
        print("沒有完全重複的資料")
    '''
