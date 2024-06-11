import json, requests, time
from datetime import date, timedelta
from dateutils import date_range
import pandas as pd


f = open("privatekey.config.json", "r")
j = json.load(f)
f.close()
finmindkey = j["key"]
del(j,f)

user_count = 0
request_limit = 0
wait_count = request_limit - 1000
sleep_time = 300


def fin_userinfo():
    global user_count, request_limit, wait_count, sleep_time
    url = "https://api.web.finmindtrade.com/v2/user_info"
    payload = {
        "token": finmindkey,
    }
    resp = requests.get(url, params=payload)
    user_count = resp.json()["user_count"]
    request_limit = resp.json()["api_request_limit"]
    wait_count = request_limit - 1000
    print(f"{user_count}/{request_limit}", flush=True)
fin_userinfo()


def finmindrequests(func):
    global user_count, request_limit, wait_count, sleep_time
    def warp(*args, **kwargs):
        global user_count, request_limit, wait_count, sleep_time
        if user_count >= wait_count:
            print("sleep")
            time.sleep(sleep_time)
            fin_userinfo()
        while(True):
            try:
                user_count += 1
                f = func(*args, **kwargs)
            except:
                print("sleep")
                time.sleep(sleep_time)
                fin_userinfo()
                continue
            break
        return f
    return warp


@finmindrequests
def fin_taiwanstockpricek(d:date):
    url = r"https://api.finmindtrade.com/api/v4/data"
    parameter = {
        "dataset": "TaiwanStockPrice",
        "start_date": d.isoformat(),
        "token": finmindkey, 
    }
    resp = requests.get(url, params=parameter)
    data = resp.json()['data']
    return data


def fin_taiwanstockpricek_duration_to_csv(start_date:date, end_date:date):
    global user_count, request_limit, wait_count, sleep_time
    for d in date_range(start_date, end_date):
        data = fin_taiwanstockpricek(d)
        pdata = pd.DataFrame(data) 
        print(f"{user_count}/{request_limit} | {d.isoformat()} | ", end="", flush=True)
        pdata.to_csv(f".\\download_datas\\taiwanstockprice\\{d.isoformat()}.csv", index=False)
        print("v", flush=True)


import code
code.interact(local=locals())