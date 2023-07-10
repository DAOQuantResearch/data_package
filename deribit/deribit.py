from deribit_websocket import websocketapi
class deribitapi():

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
   

    def get_instruments(self,crypto,kind=None,expired=None):
        """
    Retrieves available trading instruments. 
    This method can be used to see which instruments are available for trading, or which instruments have recently expired.
    """
        
        params={
            
                "currency" : crypto,
                "kind" : kind,
                "expired": expired
                    
           
        }
        return self.websocketClient.call_api("get_instruments",params)
    

    def get_instrument(self,instrument_name):

        params={
           
                "instrument_name" : instrument_name
        }
        return self.websocketClient.call_api("get_instrument",params)
    
    def get_book_summary_by_currency(self,crypto,kind):
        params={
            "currency" : crypto,
            "kind" : kind
        }
        return self.websocketClient.call_api("get_book_summary_by_currency",params)
        

    def get_book_summary_by_instrument(self,instrument_name):
        params={
            "instrument_name" : instrument_name
        }
        return self.websocketClient.call_api("get_book_summary_by_instrument",params)
    
    
    
    def get_tradingview_chart_data(self,instrument_name,start_timestamp,end_timestamp,resolution):
        params={
            "instrument_name" : instrument_name,
            "start_timestamp" : start_timestamp,
            "end_timestamp" : end_timestamp,
            "resolution" : resolution
        }
        return self.websocketClient.call_api("get_tradingview_chart_data",params)
    

    def get_ticker(self,instrument_name):
        params={
            "instrument_name" : instrument_name
        }
        return self.websocketClient.real_time("ticker",params)



deribitapi_client=deribitapi()
deribitapi_client.get_instrument("BTC")

