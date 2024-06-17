import json, requests, time
from datetime import date, timedelta
from dateutils import date_range, skipdates_include_weekend
import pandas as pd
from io import StringIO
import os


def twse_warrantstock_pd(d:date = None):
    if not d:
        d = date.today()
    assert type(d) == date
    payload = { "date" : d.isoformat().replace('-','') }
    url = f"https://www.twse.com.tw/rwd/en/stock/warrantStock"
    resp = requests.get(url, params=payload)
    js = resp.json()
    js["fields"][2] = "Warrant Increase/Decrease"
    js["fields"][5] = "Underlying Instrument Increase/Decrease"
    for d in js["data"]:
        if len(d)>15:
            d.pop(4)
    fpd = pd.DataFrame(js["data"], columns=js["fields"])
    return fpd

    

if __name__ == '__main__':
    import code
    code.interact(local=locals())