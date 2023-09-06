import requests
import json

access_token = "XhjlIeVEPg9K7XopJEE3apxHjLjqevzKWIVcbXEvhls"
access_token = "n-F758SVkllxJ38JmTJQPgjQ_M4C5Bdq4yUagciKA8U"

header = {"Authorization": "Bearer " + access_token,
          "Accept": "application/json",

          "Content-Type": "application/json"
          }

url = "https://app.pennylane.tech/api/external/v1/customers"


payload = {"customer": {
        "customer_type": "company",
        "name": "Pennylane",
        "reg_no": "XXXXXXXXX",
        "address": "4 rue du faubourg saint martin",
        "postal_code": "75010",
        "city": "Paris",
        "country_alpha2": "FR",
        "emails": ["hello@example.org"]
    }}

print(payload)

response = requests.request("POST", url, json=payload, headers=header)

data = json.loads(response.text)
print(data)
