import json

import base64

endpoints={
    
"sales_url":"https://smartup.online/b/trade/txs/tdeal/order$export",

"return_url":"https://smartup.online/b/anor/mxsx/mdeal/return$export",

"warhouse_writeOFF_url":"https://smartup.online/b/anor/mxsx/mkw/writeoff$export",

"return_suppp_url":"https://smartup.online/b/anor/mxsx/mkw/return$export",

"finance_pay_url":"https://smartup.online/b/trade/txs/tcs/cashin$export",

"cash_url":"https://smartup.online/b/anor/mxsx/mkcs/cash_operation$export",

"finance_bank_url":"https://smartup.online/b/anor/mxsx/mkcs/bank_operation$export",

"references_inventory_url" :"https://smartup.online/b/anor/mxsx/mr/inventory$export",


"references_product_url" :"https://smartup.online/b/anor/mxsx/mr/product_group$export",

"ref_inventory_url":"https://smartup.online/b/anor/api/v2/mkf/product_price$export",

"legal_url":"https://smartup.online/b/anor/mxsx/mr/legal_person$export",

"natural_url" :"https://smartup.online/b/anor/mxsx/mr/natural_person$export",


"persons_url" :"https://smartup.online/b/anor/mxsx/mr/person_group$export"
}


















DB_URL = "postgresql+psycopg2://user:password@host.docker.internal:5432/database_name"


with open ("auth.json","r",encoding="utf-8") as file:
    data = json.load(file)


project_code = data["PROJECT_CODE"]
filial_id = data['FILIAL_ID']
username = data["username"]
password = data["password"]



def get_headers ():
    credentials = f"{username}:{password}"
    token = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    headers = {
    "Authorization": f"Basic {token}",  # Basic va {token} orasida bo'sh joy bo'lishi shart
    "project_code":project_code,
    "filial_id": filial_id,
    }

    return headers 


get_headers()

       
