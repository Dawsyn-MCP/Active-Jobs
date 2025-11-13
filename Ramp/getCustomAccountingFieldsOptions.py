import requests, os, json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("RAMP_ACCESS_TOKEN")

endpoint = "https://demo-api.ramp.com/developer/v1/accounting/field-options?field_id=106e5fa4-fa9f-4032-8f15-8559940dad0a"

headers = {
  "Accept": "application/json",
  "Authorization": f"Bearer {token}",
}

response = requests.get(
  endpoint,
  headers=headers,
)

# Define the file path to save JSON output
script_dir = os.path.dirname(__file__)  # Current script directory
output_file = os.path.join(script_dir, "Data/CustomAccountingFieldOptions.json")  # File path

data = response.json()
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)