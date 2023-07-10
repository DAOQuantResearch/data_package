import time
import datetime
import pandas as pd
import json
import websocket
import threading

def convert_to_timestamp(date_time):
    string = date_time
    timestamp=int(time.mktime(datetime.datetime.strptime(string,"%d/%m/%Y %H:%M:%S").timetuple()))
    return timestamp


def convert_dataframe(data_json):
    dfItem = pd.DataFrame.from_records(data_json)
    return dfItem





    


#convert_to_timestamp("01/01/2018 00:00:00")



