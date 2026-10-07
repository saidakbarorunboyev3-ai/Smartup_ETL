from client  import get_data
from config import get_headers,endpoints
import requests
import pandas as pd

import json
from sqlalchemy import create_engine 
from load import loader


legal_entity = get_data(endpoints["natural_url"],'natural_person')


legal_entity['full_name'] = legal_entity['first_name'] + " " + legal_entity['last_name']


cols = ["person_id", "full_name", "middle_name", "gender",
        "birthday", "main_phone", "address", "legal_person_code",
        "telegram", "email", "passport_number", "state"]

legal_cleaning = legal_entity.reindex(columns=cols).to_dict("records")

legal_cleaningdf = pd.DataFrame(legal_cleaning)

legal_cleaningdf.dtypes

legal_cleaningdf['person_id'] =pd.to_numeric(legal_cleaningdf["person_id"])

legal_cleaningdf['birthday'] =pd.to_datetime(legal_cleaningdf["birthday"],format ="%d.%m.%y",errors="coerce")


legal_cleaningdf['types'] ='natural_person'



legal_groups =[]

for _, column in legal_entity.iterrows():
    for ustun in column['groups']:
        legal_groups.append({
            "person_id":column.get('person_id'),
           
            "group_code":ustun.get("group_code"),
            
            "type_code":ustun.get('type_code')

        })

legal_roomss = []


for _,qiymat in legal_entity.iterrows():
    for qator in qiymat['rooms']:
        legal_roomss.append({
            "person_id":qiymat.get("person_id"),
            "room_id":qator.get("room_id"),
            "room_code":qator.get("room_code"),
            "room_type_code":qator.get("room_tye_code")
        })     







natural_person = get_data(endpoints['legal_url'], "legal_person")

kerakli = ['person_id','name','short_name','code','main_phone','telegram','address','email','state']

natural_cleaning = natural_person.reindex(columns=kerakli).to_dict('records')

natural_cleaningDF = pd.DataFrame(natural_cleaning)




natural_cleaningDF["person_id"] =pd.to_numeric(natural_cleaningDF["person_id"])

natural_legal_group = []

for _, column in natural_person.iterrows():
    for ustun in column['groups']:
        natural_legal_group.append({
            "person_id":column.get("person_id"),
            "group_id":ustun.get("group_id"),
            "group_code":ustun.get("group_code"),
            "type_id":ustun.get("type_id"),
            "type_code":ustun.get("type_code")
        })

natural_bank_accounts = []

for _, abs in natural_person.iterrows():
    for sba in abs['bank_accounts']:
        natural_bank_accounts.append({
            "person_id":abs.get("person_id"),
            "bank_account_id":sba.get("bank_account_id"),
            "bank_account_code":sba.get("bank_account_code"),
            "bank_account_name":sba.get("bank_account_name"),
            "is_main":sba.get("is_main"),
            'state':sba.get("state"),
            "currency_code":sba.get("currency_code"),
            "note":sba.get("note")
        })



natural_rooms = []   

for _, abc in natural_person.iterrows():
    for ert in abc['rooms']:
        natural_rooms.append({
            "person_id":abc.get("erson_id"),
            "room_id":ert.get("room_id"),
            "room_code":ert.get("room_code"),
            "room_type_code":ert.get("room_type_code")

        
        })



legal_cleaning_DF = pd.DataFrame(legal_cleaning)

legal_cleaning_DF['types'] ='natural_person'

natural_cleaning_DF = pd.DataFrame(natural_cleaning)

natural_cleaning_DF['types'] ='legal_person'

customer =pd.concat([legal_cleaning_DF,natural_cleaning_DF],ignore_index=True)

loader(customer,"customers")





legal_groups_DF =pd.DataFrame(legal_groups)

natural_legal_group_df =pd.DataFrame(natural_legal_group)


customer_groops = pd.concat([legal_groups_DF,natural_legal_group_df],ignore_index=True)

loader(customer_groops,"customer_groops")





legal_roomssDF =pd.DataFrame(legal_roomss)

natural_roomsdf = pd.DataFrame(natural_rooms)

customer_rooms =pd.concat([legal_roomssDF,natural_roomsdf],ignore_index=True)

loader(customer_rooms,"customer_rooms")






customer_bank_accounts = pd.DataFrame(natural_bank_accounts)

loader(customer_bank_accounts,"customer_bank_accounts")










