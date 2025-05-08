import http.client
import json
import os
from dotenv import load_dotenv


load_dotenv()

#accessing the environment variables
access_token = os.getenv("ACCESS_TOKEN")

baseUrl = http.client.HTTPSConnection("sandbox.procore.com")
sandBoxID = "4267385"

headers = {"Authorization":f"Bearer {access_token  }"}

#get all projects in the sandbox
baseUrl.request("GET", "/rest/v1.0/projects?company_id=" + sandBoxID, headers=headers)

response = baseUrl.getresponse()
data = response.read()

# Decode the response from bytes to string
json_string = data.decode("utf-8")

# Convert string to JSON object (dict)
try:
    json_data = json.loads(json_string)  # Parse JSON response
except json.JSONDecodeError as e:
    print("❌ Failed to parse JSON:", e)
    exit()

# Define the file path to save JSON output
script_dir = os.path.dirname(__file__)  # Current script directory
output_file = os.path.join(script_dir, "projects.json")  # File path

# Write JSON data to a file with proper formatting
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(json_data, file, indent=4)  # Pretty-print JSON

print(f"✅ JSON output saved to {output_file}")