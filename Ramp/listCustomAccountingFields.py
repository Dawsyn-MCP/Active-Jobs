import requests, os, json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("RAMP_ACCESS_TOKEN")
print(f"Token: {token}")

# Sandbox endpoint
endpoint = "https://demo-api.ramp.com/developer/v1/accounting/fields"

# Production
# endpoint = "https://api.ramp.com/developer/v1/accounting/fields"

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
output_file = os.path.join(script_dir, "Data/CustomAccountingFields.json")  # File path

data = response.json()
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)