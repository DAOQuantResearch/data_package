from DQR_Data.deribit.deribit import deribitAPI

import pytest


def test_get_book_summary_by_currency():
    client=deribitAPI()
    data=client.get_book_summary_by_currency("BTC")
    assert len(data['result'])>0








