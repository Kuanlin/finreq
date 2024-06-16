import json, requests, time
from datetime import date, timedelta
from dateutils import date_range, skipdates_include_weekend
import pandas as pd
from io import StringIO
import os


def twse_warrantstock_pd(d:date):
    d_str = d.isoformat().replace('-','')
    payload = {
        "date" : d_str,
    }
    url = f"https://www.twse.com.tw/rwd/en/stock/warrantStock"
    resp = requests.get(url, params=payload)
    data = resp.json()
    return resp
    content = str(resp.content)
    #content = content.split('\n', 2)[2] #pop out first 2 lines
    cio = StringIO(content)
    return pd.read_csv(cio)

    

if __name__ == '__main__':
    import code
    code.interact(local=locals())