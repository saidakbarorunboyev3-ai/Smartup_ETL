from client  import get_data
from config import get_headers,endpoints
import requests
import pandas as pd

import json
from sqlalchemy import create_engine 
from load import loader

products = get_data(endpoints["references_product_url"],'product_group')

products_cleaning = ["products_group_id","code","name","product_kind","state"]

products_table =  products.reindex(columns=products_cleaning)

df =pd.DataFrame(products_table)

loader(df,"products")

products_group =[]

for _,column in products.iterrows():
    for abs in column['product_group_types']:
        products_group.append({
            "product_group_id":column.get("product_group_id"),
            "product_type_id":abs.get("product_type_id"),
            "code":abs.get("code"),
            "name":abs.get("name"),
            "state":abs.get("state"),
            "order_no":abs.get("order_no")
        
        })


pgp_df = pd.DataFrame(products_group)       

loader(pgp_df,"products_group")