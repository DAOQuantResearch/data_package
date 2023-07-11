# DQR Data Package

A python library for cryptocurrency trading for Binance and Deribit 

> we currently work on uniswap and other decentralized exchange platform :blush:



## Method :smiley:

### :arrow_forward:Binance

**Time format : `%d/%m/%Y %H:%M:%S`, eg: 01/02/2021 00:00:00**

| method |   parameter   |  explain    |
| -------------------- | ---- | ---- |
| realtime_price | `channel` | Get the real-time tick data. If you want to stop, press `ctr-c`, it will stop retrieve the data and return the data to you <br><br> `channel` is list type : ```["btcusdt@aggTrade","btcusdt@depth"]``` |
| get_historical_price | `crypto` `start_time` `end_time` **`interval`** | Get the historical price. <br> **`interval`** : `1s`, `1m`, `1h`, `1d`, `1w`,`1M` |
| get_historical_aggtrade | `crypto` `start_time` `end_time` | Get compressed, aggregate trades. Trades that fill at the time, from the same order, with the same price will have the quantity aggregated. |



### :arrow_forward:Deribit

| method                         | parameter                                                    | explain                                                      |
| ------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| get_instruments                | `crypto` `kind=None` `expired=False`                         | Retrieves available trading instruments. This method can be used to see which instruments are available for trading, or which instruments have recently expired.<br> `crypto` -- > eg: `BTC` `ETH` `USDC` <br><br>`kind` -- > eg : `future` `option` `spot` `future_combo` `option_combo`<br><br>`expired` --> Set to true to show recently expired instruments instead of active ones. |
| get_instrument                 | `instrument_name`                                            | Retrieves information about instrument                       |
| get_book_summary_by_currency   | `crypto`,`kind`                                              | Retrieves the summary information such as open interest, 24h volume, etc. for all instruments for the currency (optionally filtered by kind). <br><br> `kind`  is Instrument kind, if not provided instruments of all kinds are considered. eg : `future` `option` `spot` `future_combo` `option_combo` |
| get_book_summary_by_instrument | `instrument_name`                                            | Retrieves the summary information such as open interest, 24h volume, etc. for a specific instrument. |
| get_tradingview_chart_data     | `instrument_name` `start_timestamp` `end_timestamp` `resolution`:str | Publicly available market data used to generate a TradingView candle chart.  <br><br>`resolution`: Chart bars resolution given in full minutes or keyword `1D` (only some specific resolutions are supported). eg: `'1'`  `'5'` `'10'` `'15'` `'30'` `'60'` `'120'` `'180'` `'360'` `'720'` `'1D'` |
| get_ticker                     | `instrument_name`                                            | Get real-time ticker data                                    |



## Install :space_invader:

Make sure that you have already have correct library on your local environment

Check your pip library list on your environment

```powershell
pip3 list
```

if you can't find the required library, please install it :

```powershell
pip3 install requests
pip3 install websocket-client
pip3 install aiohttp
pip3 install pandas
```



## Example  :see_no_evil:

```python
DQR_Data_client=DQR_Data()
print(DQR_Data_client.binance.get_historical_aggtrade("BTCUSDT","01/02/2021 00:00:00","01/02/2021 00:05:00"))


print(DQR_Data_client.binance.realtime_price(["btcusdt@trade"]))

""" Example output
{
  "e": "trade",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "t": 12345,       // Trade ID
  "p": "0.001",     // Price
  "q": "100",       // Quantity
  "b": 88,          // Buyer order ID
  "a": 50,          // Seller order ID
  "T": 123456785,   // Trade time
  "m": true,        // Is the buyer the market maker?
  "M": true         // Ignore
}

"""

print(DQR_Data_client.deribit.get_ticker("BTC-PERPETUAL"))

""" Example output
{
  "jsonrpc": "2.0",
  "id": 8106,
  "result": {
    "best_ask_amount": 53040,
    "best_ask_price": 36290,
    "best_bid_amount": 4600,
    "best_bid_price": 36289.5,
    "current_funding": 0,
    "estimated_delivery_price": 36297.02,
    "funding_8h": 0.00002203,
    "index_price": 36297.02,
    "instrument_name": "BTC-PERPETUAL",
    "interest_value": 1.7362511643080387,
    "last_price": 36289.5,
    "mark_price": 36288.31,
    "max_price": 36833.4,
    "min_price": 35744.73,
    "open_interest": 502231260,
    "settlement_price": 36169.49,
    "state": "open",
    "stats": {
      "high": 36824.5,
      "low": 35213.5,
      "price_change": 0.2362,
      "volume": 7831.26548117,
      "volume_usd": 282615600
    },
    "timestamp": 1623059681955
  }
}

"""
```

