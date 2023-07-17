from .binance.binance import BinanceAPI
from .deribit.deribit import deribitAPI
from .uniswap.uniswap import uniswapAPI
class DQR_Data():
    def __init__(self):
        self.binance=BinanceAPI()
        self.deribit=deribitAPI()
        self.uniswap=uniswapAPI()
        
        self.count=10
        



# if __name__ == '__main__':
#     DQR_Data_client=DQR_Data()
    #print(DQR_Data_client.binance.get_historical_trade("BTCUSDT","01/02/2021 00:00:00","01/02/2021 00:05:00"))
    #print(DQR_Data_client.deribit.get_ticker("BTC-PERPETUAL"))
    #print(DQR_Data_client.binance.realtime_price(["btcusdt@trade"]))