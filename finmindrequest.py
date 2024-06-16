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


#TaiwanSecuritiesTraderInfo
@finmindrequests
def fin_taiwansecuritiestraderinfo():
    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
        "dataset": "TaiwanSecuritiesTraderInfo",
        "token": finmindkey
    }
    resp = requests.get(url, params=parameter)
    data = resp.json()['data']
    return data


#TaiwanSecuritiesTraderInfo to csv
def fin_taiwansecuritiestraderinfo_to_csv():
    global user_count, request_limit, wait_count, sleep_time
    d = date.today()
    data = fin_taiwansecuritiestraderinfo()
    pdata = pd.DataFrame(data) 
    print(f"{user_count}/{request_limit} | {d.isoformat()} | ", end="", flush=True)
    pdata.to_csv(f".\\download_datas\\taiwansecuritiestraderinfo\\retrievedate_{d.isoformat()}.csv", index=False)
    print("v", flush=True)


#TaiwanStockTradingDailyReport
@finmindrequests
def fin_taiwanstocktradingdailyreport(d:date, **kwargs):
    url = 'https://api.finmindtrade.com/api/v4/taiwan_stock_trading_daily_report'
    parameter = {}
    if "securities_trader_id" in kwargs:
        parameter["securities_trader_id"] = kwargs["securities_trader_id"]
    elif "secid" in kwargs:
        parameter["securities_trader_id"] = kwargs["scid"]
    elif "stock_id" in kwargs:
        parameter["data_id"] = kwargs["stock_id"]
    elif "data_id" in kwargs:
        parameter["data_id"] = kwargs["data_id"]
    elif "stkid" in kwargs:
        parameter["data_id"] = kwargs["stkid"]
    else:
        raise Exception
    if not d:
        d = date.today()
    parameter = parameter | { "date": d.isoformat(), "token": finmindkey }
    data = requests.get(url, params=parameter)
    data = data.json()['data']
    return data

#TaiwanStockTradingDailyReport to csv
def fin_taiwanstocktradingdailyreport_facade_to_csv(start_date:date, end_date:date, **kwargs):
    global user_count, request_limit, wait_count, sleep_time
    key = ""
    vals = None
    if "securities_trader_ids" in kwargs:
        key = "securities_trader_id"
        vals = kwargs["securities_trader_ids"]
    elif "stock_ids" in kwargs:
        key = "data_id"
        vals = kwargs["stock_ids"]
    elif "data_ids" in kwargs:
        key = "data_id"
        vals = kwargs["data_ids"]
    assert type(vals) == list
    for d in date_range(start_date, end_date):
        for v in vals:
            data = fin_taiwanstocktradingdailyreport(d, **{key: v})
            pdata = pd.DataFrame(data) 
            print(f"{user_count}/{request_limit} | {d.isoformat()} | {key}:{v} | ", end="", flush=True)
            pdata.to_csv(f".\\download_datas\\taiwanstocktradingdailyreport\\{d.isoformat()}_{key}_{v}.csv", index=False)
            print("v", flush=True)

#TaiwanStockWarrantTradingDailyReport
@finmindrequests
def fin_taiwanstockwarranttradingdailyreport(d:date, **kwargs):
    url = 'https://api.finmindtrade.com/api/v4/taiwan_stock_warrant_trading_daily_report'
    parameter = {}
    if "securities_trader_id" in kwargs:
        parameter["securities_trader_id"] = kwargs["securities_trader_id"]
    elif "secid" in kwargs:
        parameter["securities_trader_id"] = kwargs["scid"]
    elif "stock_id" in kwargs:
        parameter["data_id"] = kwargs["stock_id"]
    elif "data_id" in kwargs:
        parameter["data_id"] = kwargs["data_id"]
    elif "stkid" in kwargs:
        parameter["data_id"] = kwargs["stkid"]
    else:
        raise Exception
    if not d:
        d = date.today()
    parameter = parameter | { "date": d.isoformat(), "token": finmindkey }
    data = requests.get(url, params=parameter)
    data = data.json()['data']
    return data

#TaiwanStockWarrantTradingDailyReport to csv
def fin_taiwanstockwarranttradingdailyreport_facade_to_csv(start_date:date, end_date:date, **kwargs):
    global user_count, request_limit, wait_count, sleep_time
    key = ""
    vals = None
    if "securities_trader_ids" in kwargs:
        key = "securities_trader_id"
        vals = kwargs["securities_trader_ids"]
    elif "secids":
        key = "securities_trader_id"
        vals = kwargs["secids"]
    elif "stock_ids" in kwargs:
        key = "data_id"
        vals = kwargs["stock_ids"]
    elif "stkids":
        key = "data_id"
        vals = kwargs["stkids"]
    elif "data_ids" in kwargs:
        key = "data_id"
        vals = kwargs["data_ids"]
    assert type(vals) == list
    for d in date_range(start_date, end_date):
        for v in vals:
            data = fin_taiwanstockwarranttradingdailyreport(d, **{key: v})
            pdata = pd.DataFrame(data) 
            print(f"{user_count}/{request_limit} | {d.isoformat()} | {key}:{v} | ", end="", flush=True)
            pdata.to_csv(f".\\download_datas\\taiwanstockwarranttradingdailyreport\\{d.isoformat()}_{key}_{v}.csv", index=False)
            print("v", flush=True)




dtf = lambda x: date.fromisoformat(x)
import code
code.interact(local=locals())