import time
import websocket
import threading
import json

class all_websocket():
    def __init__(self,url):
        self.base_url = url
        self.timeout=10
        self.last_message_time = time.time()
        self.is_time=False
        self.temp=[]
        self.thread=None

        pass
    
    
    def on_message(self, ws, message):
        print(message)
        data=json.loads(message)
        self.temp.append(data['result'])
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
    

    def real_time(self,msg,params):
        try:
            websocket.setdefaulttimeout(5)

            ws=websocket.WebSocketApp(self.base_url,on_message=self.on_message,on_close=self.on_close)
            subscribe_message = subscribe_message = {
                "jsonrpc" : "2.0",
                    "id" : 9344,
                    "method" : "public/"+msg,
                    "params" : params
            }
            #print(self.base_url)
            #print(subscribe_message)
            ws.on_open = lambda ws: self.on_open(ws, subscribe_message)

            self.thread = threading.Thread(target=self.check_timeout, args=(ws,))
            self.thread.start()

            ws.run_forever()
            self.thread.join()
            return self.temp
           
        except KeyboardInterrupt:
            print("KeyboardInterrupt has been caught.")
        
            self.thread.join()
            return self.temp
        

        