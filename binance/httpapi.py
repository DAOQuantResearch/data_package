import requests
import time
import json
import concurrent.futures

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
                    if params['interval']=='1s':
                        end_time = start_timestamp + (1000 * 1 * 1000)  
                    elif params['interval']=='1m':
                        end_time = start_timestamp + (1000 * 60 * 1000)
                    elif params['interval']=='1h':
                        end_time = start_timestamp + (1000 * 60 * 60 * 1000)
                    elif params['interval']=='1d':
                        end_time = start_timestamp + (1000 * 60 * 60 * 24 * 1000)
                    elif params['interval']=='1w':
                        end_time = start_timestamp + (1000 * 60 * 60 * 24 * 7 * 1000)
                    elif params['interval']=='1M':
                        end_time = start_timestamp + (1000 * 60 * 60 * 24 * 30 * 1000)
                    

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
                #print(first_trade)
                first_trade=first_trade.json()
                first_trade_id=first_trade[0]["a"]
                from_id=first_trade_id
                
                while ((from_id<end_trade_id)):
                    #print("yes")
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
        #print("finish")
    
    def kline_V2(self,crypto,start,end,interval):
        params = {
            "symbol": crypto,
            "interval": interval,
            "startTime": start,
            "endTime": end,
            "limit": 1000
        }
        asyncio.run(self.data_pre(params,"klines"))
    
     
    def aggtrade_V2(self,crypto,fromtime,endtime):
          
            # url_path = "/api/v3/aggTrades"
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
    

    def get_kline_data_v1(self,params,stream):
        url = "https://api.binance.com/api/v3/"+stream
 
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            return data
        elif response.status_code==429:
            retry_after = int(response.headers.get("Retry-After", "5"))
            print("Rate Limit Exceeded. Waiting for rate limit reset...")
            time.sleep(retry_after)
            return self.get_kline_data_v1(self,params,stream)
        else:
            response.raise_for_status()

        
       

    def get_price_data_v1(self,params,stream):
        kline_data = []
        tasks = []
        end_timestamp=params["endTime"]
        start_timestamp=params["startTime"]

        if stream=="klines":
            with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
                while start_timestamp < end_timestamp:
                    if params['interval']=='1s':
                        end_time = start_timestamp + (1000 * 1 * 1000)  
                    elif params['interval']=='1m':
                        end_time = start_timestamp + (1000 * 60 * 1000)
                    elif params['interval']=='1h':
                        end_time = start_timestamp + (1000 * 60 * 60 * 1000)
                    elif params['interval']=='1d':
                        end_time = start_timestamp + (1000 * 60 * 60 * 24 * 1000)
                    elif params['interval']=='1w':
                        end_time = start_timestamp + (1000 * 60 * 60 * 24 * 7 * 1000)
                    elif params['interval']=='1M':
                        end_time = start_timestamp + (1000 * 60 * 60 * 24 * 30 * 1000)
                    else :
                        break
                    params['startTime']=start_timestamp
                    params['endTime']=end_time
                    tasks.append(executor.submit(self.get_kline_data_v1, params,stream))
                    start_timestamp = end_time
                    time.sleep(0.05) 

                for task in concurrent.futures.as_completed(tasks):
                    try:
                        data=task.result()
                        if data:
                            kline_data.extend(data)
                    except requests.exceptions.HTTPError as e:
                        # Handle other HTTP errors
                        print("HTTP Error:", e)
                    except Exception as e:
                        # Handle other exceptions
                        print("Error:", e)

            return kline_data
        
        elif stream=="aggTrades":
            params['limit']=1
            first_trade=requests.get("https://api.binance.com/api/v3/aggTrades",params)
            first_trade=first_trade.json()
            #print(first_trade)

            params['startTime']=params['endTime']
            params['endTime']=None
            end_trade=requests.get("https://api.binance.com/api/v3/aggTrades",params)
            end_trade=end_trade.json()
            end_trade_id=end_trade[0]["a"]
            first_trade_id=first_trade[0]["a"]
            from_id=first_trade_id
            with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:

                while ((from_id<end_trade_id)):
                    #print("yes")
                    params1={
                            "symbol": params["symbol"],
                            "limit": 1000,
                            "fromId":from_id,
                        }
                    tasks.append(executor.submit(self.get_kline_data_v1, params1,stream))
                    from_id+=1000
                for task in concurrent.futures.as_completed(tasks):
                    try:
                        data=task.result()
                        if data:
                            kline_data.extend(data)
                    except requests.exceptions.HTTPError as e:
                        # Handle other HTTP errors
                        print("HTTP Error:", e)
                    except Exception as e:
                        # Handle other exceptions
                        print("Error:", e)

            return kline_data

                

    def kline_V1(self,crypto,start,end,interval):
        params={
            "symbol": crypto,
            "interval": interval,
            "startTime": start,
            "endTime": end,           
        }

        kline_data = self.get_price_data_v1(params,"klines")
        print(kline_data)
        # Process the kline_data as per your requirements
        print("finish")

    def aggTrade_V1 (self,crypto,start,end):
        params={
            "symbol": crypto,
            "startTime": start,
            "endTime": end,
        }
        aggtrade_data=self.get_price_data_v1(params,"aggTrades")
        print(aggtrade_data)
        print("finish")










## main 
# if __name__ == "__main__":
#     client=httpapi()
#     #client.aggTrade_V1("BTCUSDT",1672531200000,1688626230000) # v1 is use the threading method -> faster than v2
#     client.kline_V1("BTCUSDT",1672531200000,1688626230000,"1d")
#     #client.aggTrade_V2("BTCUSDT",1688601600000,1688649391000) # v2 is use the threading method 
