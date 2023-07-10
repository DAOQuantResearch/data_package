
import httpapi
import websocketapi
from util.util import convert_to_timestamp
from util.util import convert_dataframe

class BinanceAPI():
    
    def __init__(self):
        self.httpClient=httpapi()
        self.websocketClient=websocketapi()
    
    def get_historical_price(self,symbol:str,start_time:str,end_time:str,interval:str):
        """
        symbol: the crypto currency
        interval: the time interval
        start_time: the start time
        end_time: the end time
        """
        start_timestamp=convert_to_timestamp(start_time)
        end_timestamp=convert_to_timestamp(end_time)
        return convert_dataframe(self.httpClient.kline_V1(symbol,start_timestamp,end_timestamp,interval))
    
    def get_historical_trade(self,symbol:str,start_time:str,end_time:str):
        """
        symbol: the crypto currency
        start_time: the start time
        end_time: the end time
        """
        start_timestamp=convert_to_timestamp(start_time)
        end_timestamp=convert_to_timestamp(end_time)
        return convert_dataframe(self.httpClient.aggTrade_V1(symbol,start_timestamp,end_timestamp))
    
    def realtime_price(self,channel:str):
        """
        channel: eg : btcusdt@trade, btcusdt
        """
        return self.websocketClient.real_time(channel)
    

