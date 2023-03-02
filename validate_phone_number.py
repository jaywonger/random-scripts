import requests

phone_number = input("Enter valid phone number: ")
print("--------------------------------------")

url = "https://api.apilayer.com/number_verification/validate?number="+ phone_number

payload = {}
headers= {
  "apikey": "Qzls9F04tJDZuvtE70QQOcV8ysZI0Ebr"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text
print(result)