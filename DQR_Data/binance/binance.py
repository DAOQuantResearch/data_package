
from DQR_Data.binance.httpapi import httpapi
from DQR_Data.binance.websocketapi import websocketapi
from DQR_Data.util import util
from DQR_Data.util import util

class BinanceAPI():
    
    def __init__(self):
        self.httpClient=httpapi()
        self.websocketClient=websocketapi()
    
    def get_historical_price(self,crypto:str,start_time:str,end_time:str,interval:str):
        """
        crypto: the crypto currency
        interval: the time interval
        start_time: the start time
        end_time: the end time
        """
        start_timestamp=util.convert_to_timestamp(start_time)
        end_timestamp=util.convert_to_timestamp(end_time)
        #print(end_timestamp)
        #df=util.convert_dataframe(self.httpClient.kline_V1(crypto,start_timestamp,end_timestamp,interval))
        
        return util.convert_dataframe(self.httpClient.kline_V1(crypto,start_timestamp,end_timestamp,interval))
    
    def get_historical_aggtrade(self,crypto:str,start_time:str,end_time:str):
        """
        crypto: the crypto currency
        start_time: the start time
        end_time: the end time
        """
        start_timestamp=util.convert_to_timestamp(start_time)
        end_timestamp=util.convert_to_timestamp(end_time)
        return util.convert_dataframe(self.httpClient.aggTrade_V1(crypto,start_timestamp,end_timestamp))
    
    def realtime_price(self,channel:str):
        """
        channel: eg : btcusdt@trade, btcusdt
        """
        return self.websocketClient.real_time(channel)
    

