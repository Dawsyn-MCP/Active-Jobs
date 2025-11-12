import requests, os, json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("RAMP_ACCESS_TOKEN")

endpoint = f"https://demo-api.ramp.com/developer/v1/accounting/field-options"

headers = {
  "Accept": "application/json",
  "Authorization": f"Bearer {token}",
  "Content-Type": "application/json",
}

payload = {
  "accounting_connection_id": None,
  "field_id": "106e5fa4-fa9f-4032-8f15-8559940dad0a",
  "options":[
        {
          "id": "450033-00",
          "value": "Big Project",
          "code": "450033-00"
        }
  ],
}

response = requests.post(
  endpoint,
  headers=headers,
  json=payload,
)

print(response.text)
