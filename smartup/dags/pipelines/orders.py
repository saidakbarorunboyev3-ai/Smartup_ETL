from client  import get_data
from config import get_headers,endpoints
import requests
import pandas as pd

import json
from sqlalchemy import create_engine 
from load import loader



orders = get_data(endpoints["sales_url"],"order")

ordersDF =pd.DataFrame(orders)

ordersDF.dtypes


kerakli = ["filial_id","filial_code","deal_id","deal_time","delivery_number","delivery_data","booked_date","total_amount","room_id","room_code","room_name","sales_manager_id","sales_manager_name","person_id","person_code","person_name"]

orders_table =ordersDF.reindex(columns=kerakli)

orders_table['filial_id'] =pd.to_numeric(orders_table['filial_id'])

orders_table['deal_id'] = pd.to_numeric(orders_table['deal_id'])

orders_table['deal_time'] = pd.to_datetime(orders_table['deal_time'],format="%d.%m.%y %H:%M:%S",errors="coerce")

orders_table['delivery_number'] = pd.to_numeric(orders_table['delivery_number'])

orders_table['booked_date']  = pd.to_datetime(orders_table["booked_date"],format="%d.%m.%y",errors="coerce")

orders_table['total_amount'] = pd.to_numeric(orders_table['total_amount'])

orders_table['room_id'] = pd.to_numeric(orders_table['room_id'])

orders_table['sales_manager_id'] = pd.to_numeric(orders_table['sales_manager_id'])


orders_table['person_id'] = pd.to_numeric(orders_table['person_id'])

orders_tabledf =pd.DataFrame(orders_table)

loader(orders_tabledf,"orders_table")


order_products = []




for _, column in ordersDF.iterrows():
   
   items= column['order_products']

   if not isinstance(items,list):
      continue

   for item in items:
      if not isinstance(item,dict):
         continue
      order_products.append({"filial_id":column.get("filial_id"), **item})


order_products_df = pd.DataFrame(order_products)

order_products_df.drop(columns=["details"], inplace=True)





loader(order_products_df,"order_products")

order_details = []

for _, abc in ordersDF.iterrows():
    ordera = abc["order_products"]

    if not isinstance(ordera, list):
        continue

    for item in ordera:                   
        if not isinstance(item, dict):
            continue

        details = item.get("details")       

        if not isinstance(details, list):
            continue

        for d in details:
            if not isinstance(d, dict):
                continue
            order_details.append({
                "filial_id": abc.get("filial_id"),
                "external_id": item.get("external_id"),  
                **d,
            })

order_details_df = pd.DataFrame(order_details)

loader(order_details_df,"order_details")


   


  

