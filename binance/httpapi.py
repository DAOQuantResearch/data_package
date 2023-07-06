import requests
import time
import json

import aiohttp
import asyncio

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
                print(len(data))
                print(data)

               
                if type=="klines":
                    start_time = int(data[-1][0]) + 1
                elif type == "aggTrades":
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
   
    

        
    async def get_historical_data(self,session, params,stream):
        url = "https://api.binance.com/api/v3/"+stream
      
        async with session.get(url, params=params) as response:
            data = await response.json()
            return data
    
    async def get_price_data(self, params,stream):
        data = []
        tasks = []
        concurrency = 100  # Number of concurrent requests

        async with aiohttp.ClientSession() as sessions:
            sem = asyncio.Semaphore(concurrency)
            if stream=="klines":
                end_timestamp=params["endTime"]
                start_timestamp=params["startTime"]
                while start_timestamp < end_timestamp:
              
                    end_time = start_timestamp + (1000 * 1 * 1000)  # 1000 minutes
                  
                    params1=params
                    params1['startTime']=start_timestamp
                    params1['endTime']=end_time
                    async with sem:
                        tasks.append(asyncio.create_task(self.get_historical_data(sessions, params1,stream)))
                    start_timestamp = end_time

                data = await asyncio.gather(*tasks)
                return data
            
            elif stream=="aggTrades":
                end_timestamp=params["endTime"]
                params['limit']=1
                first_trade=requests.get("https://api.binance.com/api/v3/aggTrades",params)
                params['startTime']=params['endTime']
                params['endTime']=None
                end_trade=requests.get("https://api.binance.com/api/v3/aggTrades",params)
                end_trade=end_trade.json()
                end_trade_id=end_trade[0]["a"]
                print(first_trade)
                first_trade=first_trade.json()
                first_trade_id=first_trade[0]["a"]
                from_id=first_trade_id
                
                while ((from_id<end_trade_id)):
                    print("yes")
                    params1={
                        "symbol": params["symbol"],
                        "limit": 1000,
                        "fromId":from_id,
                    }
                    async with sem:
                        tasks.append(asyncio.create_task(self.get_historical_data(sessions, params1,stream)))
                    from_id+=1000
                data = await asyncio.gather(*tasks)
                return data

        
    async def data_pre(self,params,stream):
         
        data = await self.get_price_data(params,stream)
        print(data)
        # Process the kline_data as per your requirements
        print("finish")
    
    def kline_V2(self,crypto,start,end,interval):
        params = {
            "symbol": crypto,
            "interval": interval,
            "startTime": start,
            "endTime": end,
            "limit": 1000
        }
        asyncio.run(self.data_pre(params,"klines"))
    
     
    def aggtrade(self,crypto,fromtime,endtime):
          
            url_path = "/api/v3/aggTrades"
            payload = {
                "symbol": crypto,
                "limit": 1000,
                "startTime": fromtime,
                "endTime": endtime
            
            }
            asyncio.run(self.data_pre(payload,"aggTrades"))

          
            
        

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
    client.aggtrade("BTCUSDT",1617235200000,1617235206000)
    #print(client.aggtrade(crypto="BTCUSDT",limit=1000, fromtime=1688473945344))