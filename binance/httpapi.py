import requests
import time
import json

class httpapi:

    def __init__(self, api_key=None, api_key_secret=None):
        self.api_key = api_key
        self.api_key_secret = api_key_secret
        self.base_url = "https://api.binance.com"

        self.session=requests.Session()
        self.session.headers.update({
            "Content-type": "application/json;charset=utf-8",
            "X-MBX-APIKEY": self.api_key
        })
    
    ### query the server
    def query(self,url_path,payload=None):
        """
        url_path: the path to the api
        payload: the parameters to the api
        
        """
        
        url = self.base_url + url_path
        if payload:
            query = self.session.get(url,params=payload)
        else:
            query = self.session.get(url)
        return query.json()
    
    def historical_data(self,originalurl,params,type):
        all_data = []
        url=self.base_url+originalurl
        while True:
            response =  self.session.get(url, params=params)
            if response.status_code == 200:
                data = json.loads(response.text)
                if len(data) == 0:
                    break  # No more data available
                all_data.extend(data)
                print(data)
                if type=="klines":
                    start_time = int(data[-1][0]) + 1
                if type == "aggTrades":
                    start_time = int(data[-1]["T"]) + 1
                else:
                    print("no type")
                    break
                params["startTime"] = start_time
            else:
                print("Request failed with status code:", response.status_code)
                return None

            time.sleep(1)  # Add a delay to comply with Binance rate limits
        
        return all_data
    

    ### check the connection to the server
    def exchangeinfo(self):
        url_path = "/api/v3/exchangeInfo"
        return self.query(url_path)
    
    
    # def orderbook(self,crypto:str,limit=1000,fromid=None):
    #     url_path = "/api/v3/depth"
    #     payload = {
    #         "symbol": crypto,
    #         "limit": limit,
    #     }
    #     if fromid:
    #         payload["fromId"]=fromid
        
    #     return self.historical_data(url_path,payload)
    
    
    # not working
    # def recent_trade (self,crypto,limit,fromtime):
    #         print(fromtime)
    #         url_path = "/api/v3/trades"
    #         payload = {
    #                 "symbol": crypto,
    #                 "limit": limit,
                
    #             }
            
    #         data=self.query(url_path,payload)
    #         all_data=[]
    #         url_historical_path="/api/v3/historicalTrades"
    #         all_data.extend(data)
    #         print(type(fromtime))
    #         print(data[0]['time'])
    #         print(type(data[0]['time']))
    #         if data[0]['time']>fromtime:
    #             print("yes")
    #         else:
    #             print("no")
    #         while True:
    #             from_id = data[0]["id"] - limit
    #             payload["fromId"]=from_id
    #             print(payload)
    #             data1=self.query(url_historical_path,payload)
    #             data1 = data1.json()
    #             print(data1)
    #             all_data.extend(data)
    #             print(data1[0]['time'])
    #             if data1[0]['time']>fromtime:
    #                 break
                
    #         return all_data


    
    def aggtrade(self,crypto:str,fromtime=None,endtime=None,limit=1000):
          
            url_path = "/api/v3/aggTrades"
            payload = {
                "symbol": crypto,
                "limit": limit
            }
           
            if fromtime:
                payload["startTime"]=fromtime
            if endtime==None and fromtime!=None:
                payload["endTime"]=int(time.time()*1000)
            if endtime:
                payload["endTime"]=endtime
            
            return self.historical_data(url_path,payload,"aggTrades")
    

    def Kline(self,crypto:str,interval:str,fromtime=None,endtime=None,limit=1000):
          
            url_path = "/api/v3/klines"
            payload = {
                "symbol": crypto,
                "interval": interval,
                "limit": limit
            }
            if fromtime:
                payload["startTime"]=fromtime
            if endtime==None and fromtime!=None:
                payload["endTime"]=int(time.time()*1000)
            if endtime:
                payload["endTime"]=endtime
            
            return self.historical_data(url_path,payload,"klines")
    

    def current_price(self,crypto:str):
        url_path = "/api/v3/avgPrice"
        payload = {
            "symbol": crypto
        }
        return self.query(url_path,payload)








## main 
if __name__ == "__main__":
    client=httpapi()
    #print(client.exchangeinfo())
    print(client.current_price("BTCUSDT"))
    #print(client.aggtrade(crypto="BTCUSDT",limit=1000, fromtime=1688473945344))