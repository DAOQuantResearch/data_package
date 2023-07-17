from DQR_Data.binance.httpapi import httpapi
import pytest


def test_klines_price():
    httpapi_client=httpapi()
    data=httpapi_client.kline_V1("BTCUSDT",1672531200000,1672617600000,"1d")
    assert len(data)==2


def test_aggtrade():
    httpapi_client=httpapi()
    data=httpapi_client.aggTrade_V1("BTCUSDT",1672531200000,1672617600000)
    assert len(data)>0





