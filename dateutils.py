from datetime import date, timedelta

valid_until = date.fromisoformat("2024-12-31")

skipdates = [ date.fromisoformat(x) for x in [
    '2021-01-01',
    '2021-01-04',
    '2021-02-05',
    '2021-02-08',
    '2021-02-09',
    '2021-02-10',
    '2021-02-11',
    '2021-02-12',
    '2021-02-13',
    '2021-02-14',
    '2021-02-15',
    '2021-02-16',
    '2021-02-17',
    '2021-02-28',
    '2021-03-01',
    '2021-04-02',
    '2021-04-03',
    '2021-04-04',
    '2021-04-05',
    '2021-04-30',
    '2021-05-01',
    '2021-06-14',
    '2021-09-20',
    '2021-09-21',
    '2021-10-10',
    '2021-10-11',
    '2021-12-31',

    '2022-01-01',
    '2022-01-03',
    '2022-01-26',
    '2022-01-27',
    '2022-01-28',
    '2022-01-31',
    '2022-02-01',
    '2022-02-02',
    '2022-02-03',
    '2022-02-04',
    '2022-02-07',
    '2022-02-28',
    '2022-04-04',
    '2022-04-05',
    '2022-05-01',
    '2022-05-02',
    '2022-06-03',
    '2022-09-09',
    '2022-09-10',
    '2022-10-10',

    '2023-01-01',
    '2023-01-02',
    '2023-01-03',
    '2023-01-17',
    '2023-01-18',
    '2023-01-19',
    '2023-01-20',
    '2023-01-21',
    '2023-01-22',
    '2023-01-23',
    '2023-01-24',
    '2023-01-25',
    '2023-01-26',
    '2023-01-27',
    '2023-01-30',
    '2023-02-27',
    '2023-02-28',
    '2023-04-03',
    '2023-04-04',
    '2023-04-05',
    '2023-05-01',
    '2023-06-22',
    '2023-06-23',
    '2023-09-29',
    '2023-10-09',
    '2023-10-10',
    '2024-01-01',
    '2024-01-02',
    '2024-02-05',
    '2024-02-06',
    '2024-02-07',
    '2024-02-08',
    '2024-02-09',
    '2024-02-10',
    '2024-02-11',
    '2024-02-12',
    '2024-02-13',
    '2024-02-14',
    '2024-02-15',
    '2024-02-28',
    '2024-04-04',
    '2024-04-05',
    '2024-05-01',
    '2024-06-10',
    '2024-09-17',
    '2024-10-10',
]]

skipdates.sort()

skipdates_include_weekend = set()

_s0 = skipdates[0]
_sN = skipdates[-1]
_dd1 = timedelta(days=1)
_sI = _s0
while(_sI<=_sN):
    if _sI in skipdates or _sI.isoweekday()>5:
        skipdates_include_weekend.add(_sI)
    _sI = _sI + _dd1


def date_range(startdate, enddate, delta=None, skipdates=set()):
    if not delta:
        if startdate>enddate:
            delta = timedelta(days=-1)
            
        else:
            delta = timedelta(days=1)

    assert type(startdate) == date
    assert type(enddate) == date
    assert type(delta) == timedelta
    assert type(skipdates) == set

    iday = startdate
    if delta.days<0:
        while(iday>enddate):
            if iday not in skipdates:
                yield iday
            iday += delta  
    else:
        while(iday<enddate):
            if iday not in skipdates:
                yield iday
            iday += delta
    if iday not in skipdates:
        yield iday