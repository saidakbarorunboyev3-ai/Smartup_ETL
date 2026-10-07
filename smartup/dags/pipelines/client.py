import requests
import pandas as pd
from config  import get_headers, endpoints



def get_data(url,key):
    response = requests.get(url,headers=get_headers())


    if response.status_code !=200:
        return "XATO"

    records = response.json()

    if not records:
        return pd.DataFrame()

    return pd.json_normalize(records[key])




get_data(endpoints['sales_url'], 'order')