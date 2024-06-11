from dataclasses import dataclass, asdict
from datetime import date

@dataclass
@dataclass(eq=False)
class TaiwanSecuritiesTraderInfo:
    securities_trader_id: str
    securities_trader: str
    establish_date: str
    address: str
    phone: str
    update_date: date
    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}
    
    def __eq__(self, other) -> bool:
        return (
            (self.securities_trader_id == other.securities_trader_id) and 
            (self.securities_trader == other.securities_trader) and
            (self.establish_date == other.establish_date) and
            (self.address == other.address) and
            (self.phone == other.phone) )
    
    def from_finmind(fdata:dict):
        d = fdata.copy()
        d["establish_date"] = date.fromisoformat(d.pop("date"))
        d["update_date"] = date.today()
        return TaiwanSecuritiesTraderInfo(**d)


@dataclass
class TaiwanStockTradingDailyReport:
    price: float
    buy: int
    sell: int
    securities_trader_id: str
    stock_id: str
    report_date: date

    def to_dict(self):
        return asdict(self)
    
    def from_finmind(fdata:dict):
        d = fdata.copy()
        d["report_date"] = d.pop("date")
        d.pop("securities_trader")
        return TaiwanStockTradingDailyReport(**d)


@dataclass
class TaiwanStockWarrantTradingDailyReport:
    price: float
    buy: int
    sell: int
    securities_trader_id: str
    stock_id: str
    report_date: date

    def to_dict(self):
        return asdict(self)
    
    def from_finmind(fdata:dict):
        d = fdata.copy()
        d["report_date"] = d.pop("date")
        d.pop("securities_trader")
        return TaiwanStockTradingDailyReport(**d)


@dataclass
class TaiwanStockDailyK:
    trading_date: date
    stock_id: str
    trading_volume: int 
    trading_money: int
    open_price: float 
    max_price: float 
    min_price: float 
    close_price: float 
    spread: float 
    trading_turnover: float

    def to_dict(self):
        return asdict(self)
    
    def from_finmind(fdata:dict):
        d = {
            "trading_date": fdata["date"],
            "stock_id": fdata["stock_id"],
            "trading_volume": fdata["Trading_Volume"],
            "trading_money": fdata["Trading_money"],
            "open_price": fdata["open"],
            "max_price": fdata["max"],
            "min_price": fdata["min"],
            "close_price": fdata["close"],
            "spread": fdata["spread"],
            "trading_turnover": fdata["Trading_turnover"]
        }
        return TaiwanStockDailyK(**d)
    

@dataclass
class TaiwanDividendResult:
    ex_date: str
    stock_id: str
    before_price: float
    after_price: float
    stock_and_cache_dividend: float
    stock_or_cache_dividend: str
    max_price: float
    min_price: float
    open_price: float
    reference_price: float

    def to_dict(self):
        return asdict(self)
    
    def from_finmind(fdata:dict):
        d = fdata.copy()
        d["ex_date"] = d.pop("date")
        return TaiwanDividendResult(**d)



holdingSharesLevel = {
    '1-999' : 1, 
    '1,000-5,000' : 2, 
    '5,001-10,000' : 3, 
    '10,001-15,000' : 4, 
    '15,001-20,000' : 5, 
    '20,001-30,000' : 6, 
    '30,001-40,000' : 7, 
    '40,001-50,000' : 8, 
    '50,001-100,000' : 9, 
    '100,001-200,000' : 10, 
    '200,001-400,000' : 11, 
    '400,001-600,000' : 12, 
    '600,001-800,000' : 13, 
    '800,001-1,000,000' : 14, 
    'more than 1,000,001' : 15, 
    '差異數調整（說明4）' : 16, 
    'total' : 17 }


@dataclass
class TaiwanStockHoldingSharesPer:

    report_date: str
    stock_id: str
    holding_shares_level: int
    people: int
    percent: float
    unit: int

    def to_dict(self):
        return asdict(self)

    def from_finmind(fdata:dict):
        d = fdata.copy()
        d["report_date"] = d.pop("date")
        d["holding_shares_level"] = holdingSharesLevel[d.pop("HoldingSharesLevel")]
        return TaiwanStockHoldingSharesPer(**d)