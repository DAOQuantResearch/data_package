import websocket
import json
import time
import threading

### mainly for realtime data streaming
class websocketapi() :
    def __init__(self,api_key=None, api_key_secret=None):
        self.api_key = api_key
        self.api_key_secret = api_key_secret
        self.base_url = "wss://stream.binance.com:9443/ws"
        self.temp=[]
        self.timeout=10
        self.last_message_time = time.time()
        self.is_time=False
        self.thread=None

    def on_message(self, ws, message):
        print(message)
        data=json.loads(message)
        self.temp.append(data)
        self.last_message_time = time.time()

    def on_error(self,ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws, message):
        print("### Opened connection ###")
        ws.send(json.dumps(message))
    
    def check_timeout(self, ws):
        while not self.is_time:
            if time.time() - self.last_message_time > self.timeout:
                ws.close()
                break
            time.sleep(1)
        
    def query(self,subscribe_message):
        """
        crypto: the crypto currency
        stream_type: the type of stream
        """
        try:
            ws=websocket.WebSocketApp(self.base_url,on_message=self.on_message,on_close=self.on_close)
            ws.on_open = lambda ws: self.on_open(ws, subscribe_message)
            self.thread = threading.Thread(target=self.check_timeout, args=(ws,))
            self.thread.start()
            ws.run_forever()
            self.thread.join()
            return self.temp
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            self.thread.join()
            return self.temp
            
    def real_time(self,crypto_stream_type:list):
        """
        crypto: the crypto currency
        stream_type: the type of stream
        """
        
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params":crypto_stream_type,
             "id": 1
             }
        
        data=self.query(subscribe_message)
        return data
    


# if __name__ == "__main__":
#     client= websocketapi()
#     client.real_time(["btcusdt@trade","btcusdt@depth"])
