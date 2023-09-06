import requests
import json
access_token = "XhjlIeVEPg9K7XopJEE3apxHjLjqevzKWIVcbXEvhls"
access_token = "n-F758SVkllxJ38JmTJQPgjQ_M4C5Bdq4yUagciKA8U"

header = {"Authorization": "Bearer " + access_token}
data= {}

url = "https://app.pennylane.tech/api/external/v1/customers/ee2d5d3e-797b-4858-a381-a78ec90497b0"
response = requests.request("GET", url, headers=header)

data = json.loads(response.text)
print(data)

for customer in data["customer"]:
    print(customer)

# print(response.text)
# data['currency'] = "MGA"
# data['service'] = "om"
# data['order_id'] = "12042021"
# data['order_label'] = "Test Paiement"
# data['amount'] = "10000"
# data['return_url'] = "http://localhost:8000"
# data['notif_url'] = "http://localhost:8000"
# data['cancel_url'] = "http://localhost:8000"
#
# res = requests.post(url_paiement, json=data, headers= header)
# print (res.json())
#
# pay_url = res.json()['pay_url']
