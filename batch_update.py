import requests
import logging
import time
from datetime import datetime,timedelta
import urllib3
import os
import yaml
from datetime import datetime
import oracledb
import random

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
def get_list():
    url="http://10.80.1.49:9999/api/teams/3/test-run-configs/356/items/?limit=10000"
    headers={
        "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxOSwidXNlcm5hbWUiOiJjYXJyaW5lIiwicm9sZSI6InVzZXIiLCJqdGkiOiIxY2FhMTY1ZC1mMmY0LTQxYjQtYjZmMi1kMTNmZTM3NDg4YjkiLCJleHAiOjE3NjgyMDE5OTEsImlhdCI6MTc2NzU5NzE5MSwiaXNzIjoidGVzdC1jYXNlLXJlcG8tYXV0aCJ9.RyDbjK4OK4w8JJBF_U1lfzoysTg7DOooxMKx9KlX7aE",
        "Origin":"http://10.80.1.49:9999",
        "Referer":"http://10.80.1.49:9999/test-run-execution?config_id=356&team_id=3",
        "Cookie":"_ga=GA1.1.42528586.1742807541; _ga_FVWC4GKEYS=GS1.1.1742807541.1.0.1742807577.0.0.0; jenkins-timestamper-offset=-28800000"
    }
    param={
        "limit":10000
    }
    require_list=[]
    response=requests.get(url,headers=headers,params=param,verify=False)
    if response.status_code==200:
        response_json=response.json()
        for value in response_json:
            if "TCG119341" in value["test_case_number"] :
                test_case_id=value.get("id")
                require_list.append(test_case_id)
        return require_list
     
def auto_approve(require_list:list):
    for test_id in require_list:
        url="http://10.80.1.49:9999/api/teams/3/test-run-configs/356/items/batch-update-results"
        headers={
            "Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxOSwidXNlcm5hbWUiOiJjYXJyaW5lIiwicm9sZSI6InVzZXIiLCJqdGkiOiIxY2FhMTY1ZC1mMmY0LTQxYjQtYjZmMi1kMTNmZTM3NDg4YjkiLCJleHAiOjE3NjgyMDE5OTEsImlhdCI6MTc2NzU5NzE5MSwiaXNzIjoidGVzdC1jYXNlLXJlcG8tYXV0aCJ9.RyDbjK4OK4w8JJBF_U1lfzoysTg7DOooxMKx9KlX7aE",
            "Origin":"http://10.80.1.49:9999",
            "Referer":"http://10.80.1.49:9999/test-run-execution?config_id=356&team_id=3",
            "Cookie":"_ga=GA1.1.42528586.1742807541; _ga_FVWC4GKEYS=GS1.1.1742807541.1.0.1742807577.0.0.0; jenkins-timestamper-offset=-28800000"
        }
        payload={
        "updates": [
            {
                "id": test_id,
                "assignee_name": "Carrine Shih",
                "test_result": "Passed",
                "executed_at": "2026-01-06T10:07:39.831Z",
                "comment": "https://drive.google.com/drive/u/0/folders/1ey9rPYmAOBFn7iwHxnOiG-7EJGWXCLAz"
            }
        ]
    }
        resposne=requests.post(url,headers=headers,json=payload,verify=False)
        if resposne.status_code==200:
            logging.info("更新完成")
            

def main():
    require_list=get_list()
    auto_approve(require_list)
    
    
    
main()
        