# Import libraries
import datetime as dt
from datetime import datetime
import json
import requests as rq
import pandas as pd
import numpy as np

def get_options_info(currency_name='BTC'):
    t1 = dt.datetime.now().timestamp()
    a = rq.get("https://test.deribit.com/api/v2/public/get_instruments?currency=" + currency_name + "&kind=option")
    b=json.loads(a.content)
    df=pd.json_normalize(b['result'])

    df.drop(['tick_size', 'settlement_currency','taker_commission', 'settlement_period',
           'rfq', 'quote_currency', 'price_index',
           'min_trade_amount', 'maker_commission', 'kind',
           'is_active', 'instrument_id',
           'counter_currency',
           'block_trade_commission'], axis=1, inplace=True)
    
    df.strike=pd.to_numeric(df.strike, downcast='integer')
    
    df.creation_timestamp=pd.to_datetime(df.creation_timestamp, unit='ms').apply(lambda x: x.strftime('%Y-%m-%d'))
    df.expiration_timestamp=pd.to_datetime(df.expiration_timestamp, unit='ms').apply(lambda x: x.strftime('%Y-%m-%d'))
    t2 = dt.datetime.now().timestamp()
    print('Processing time:', t2 - t1)
    return(df)

def get_option_data(contract_names):
    df=[]
    t1=dt.datetime.now().timestamp()
    for i in contract_names:
        temp='https://test.deribit.com/api/v2/public/get_order_book?instrument_name='
        df.append(rq.get(temp + i).json()['result'])

    df=pd.json_normalize(df)
    t2 = dt.datetime.now().timestamp()
    print('Processing time:', t2 - t1)
    return(df)

def get_index_price(index_name='btc_usdc'):
    a = rq.get("https://test.deribit.com/api/v2/public/get_index_price?index_name=" + index_name)
    b=json.loads(a.content)
    return b['result']['index_price']
