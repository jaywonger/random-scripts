import requests

phone_number = input("Enter valid phone number: ")
print("--------------------------------------")

url = "https://api.apilayer.com/number_verification/validate?number="+ phone_number

payload = {}
headers= {
  "apikey": ""
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text
print(result)
