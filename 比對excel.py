import pandas as pd


key="用户名"

set1=set(pd.read_excel('gi8viet_20251118181822_玩家红利派发记录 - Tue Nov 18 18_18_20 2025_part1_1.xlsx')[key])
set2=set(pd.read_excel('失敗名單_1763448180770-carrine01_2025-11-18 15_12_12 (1).xlsx')[key])

if set1==set2:
    print("excel username一樣")
else:
    print("兩個set沒有一樣")
    different_file1=sorted(set1-set2)
    different_file2=sorted(set2-set1)
    print(different_file1)
    print(different_file2)
