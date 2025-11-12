import requests, os, json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("RAMP_ACCESS_TOKEN")

endpoint = "https://demo-api.ramp.com/developer/v1/accounting/field/4c81b017-c9ba-4de5-9bb4-a14eb85ccf1e"

headers = {
  "Accept": "application/json",
  "Authorization": f"Bearer {token}",
}

response = requests.get(
  endpoint,
  headers=headers,
)

print(response)