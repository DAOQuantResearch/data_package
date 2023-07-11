from .deribit_websocket import websocketapi
from util import util
class deribitAPI():

    def __init__(self):
        self.websocketClient=websocketapi()
        

    
    # def call_api(self,method,params):
    #     msg={
    #         "method" : "public/"+method,
    #         "params" : params,
    #         "jsonrpc" : "2.0",
    #         "id" : 1
    #     }
    #     return self.websocketClient.call_api(msg)
   

    def get_instruments(self,crypto,kind=None,expired=False):
        """
    Retrieves available trading instruments. 
    This method can be used to see which instruments are available for trading, or which instruments have recently expired.
    """
        
        params={
            
                "currency" : crypto,
                "kind" : kind,
                "expired": expired
                    
           
        }
        data=self.websocketClient.call_api("get_instruments",params)
        return util.json_convert_dataframe(data['result'])
    

    def get_instrument(self,instrument_name):

        params={
           
                "instrument_name" : instrument_name
        }
        data=self.websocketClient.call_api("get_instrument",params)
        return data
    
    def get_book_summary_by_currency(self,crypto,kind):
        params={
            "currency" : crypto,
            "kind" : kind
        }
        data=self.websocketClient.call_api("get_book_summary_by_currency",params)
        return data
        

    def get_book_summary_by_instrument(self,instrument_name):
        params={
            "instrument_name" : instrument_name
        }
        data=self.websocketClient.call_api("get_book_summary_by_instrument",params)
        return data
    
    
    
    def get_tradingview_chart_data(self,instrument_name,start_timestamp,end_timestamp,resolution):
        
        params={
            "instrument_name" : instrument_name,
            "start_timestamp" : util.convert_to_timestamp(start_timestamp),
            "end_timestamp" : util.convert_to_timestamp(end_timestamp),
            "resolution" : resolution
        }
        data=self.websocketClient.call_api("get_tradingview_chart_data",params)
        return data
    

    def get_ticker(self,instrument_name):
        params={
            "instrument_name" : instrument_name
        }
        data=self.websocketClient.real_time("ticker",params)
        return data





