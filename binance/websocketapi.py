import websocket
import json

### mainly for realtime data streaming
class websocketapi :
    def __init__(self,api_key=None, api_key_secret=None):
        self.api_key = api_key
        self.api_key_secret = api_key_secret
        self.base_url = "wss://stream.binance.com:9443/ws"

    def on_message(self, ws, message):
        print(message)

    def on_error(self,ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws, message):
        print("Opened connection")
        ws.send(json.dumps(message))
        
    def query(self,subscribe_message):
        """
        crypto: the crypto currency
        stream_type: the type of stream
        """
        ws=websocket.WebSocketApp(self.base_url,on_message=self.on_message,on_close=self.on_close)
        ws.on_open = lambda ws: self.on_open(ws, subscribe_message)
        ws.run_forever()  
    
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
        self.query(subscribe_message)
    


# if __name__ == "__main__":
#     client= websocketapi()
#     client.real_time(["btcusdt@trade","btcusdt@depth"])
