import asyncio
import websocket
import websockets
import json
import threading
import time
from .all_websocket import all_websocket


class websocketapi():
    def __init__(self):
        self.base_url = "wss://test.deribit.com/ws/api/v2"
        self.timeout=10
        self.last_message_time = time.time()
        self.websocket_client=all_websocket(self.base_url)

        self.is_time=False

    def on_message(self, ws, message):
        print(message)
        self.last_message_time = time.time()


    def on_error(self,ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")


    def on_open(self, ws, message):
        #print("Opened connection")
        ws.send(json.dumps(message))

    def check_timeout(self, ws):
        while not self.is_time:
            if time.time() - self.last_message_time > self.timeout:
                ws.close()
                break
            time.sleep(1)


    def test(self,msg,params):
        websocket.setdefaulttimeout(5)
        ws = websocket.WebSocket()
        ws.connect(self.base_url)


        subscribe_message = {
             "jsonrpc" : "2.0",
                "id" : 9344,
                "method" : "public/"+msg,
                "params" : params
        }
        #print(subscribe_message)
        self.on_open(ws, subscribe_message)
        data=ws.recv()
        return data



    def call_api(self,msg,params):
        data=json.loads(self.test(msg,params))
        return data
    
    """
    def real_time(self,msg,params):
        websocket.setdefaulttimeout(5)

        ws=websocket.WebSocketApp(self.base_url,on_message=self.on_message,on_close=self.on_close)
        subscribe_message = subscribe_message = {
             "jsonrpc" : "2.0",
                "id" : 9344,
                "method" : "public/"+msg,
                "params" : params
        }
        ws.on_open = lambda ws: self.on_open(ws, subscribe_message)

        thread = threading.Thread(target=self.check_timeout, args=(ws,))
        thread.start()

        ws.run_forever()
        thread.join()

    """
    def real_time(self,msg,params):
        data=self.websocket_client.real_time(msg,params)
        return data
        
    


