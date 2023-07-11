from main import DQR_Data

DQR_Data_client=DQR_Data()
#print(DQR_Data_client.binance.get_historical_aggtrade("BTCUSDT","01/02/2021 00:00:00","01/02/2021 00:05:00"))
#print(DQR_Data_client.binance.realtime_price(["btcusdt@trade"]))
print(DQR_Data_client.deribit.get_ticker("BTC-PERPETUAL"))