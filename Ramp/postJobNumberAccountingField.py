import requests, os, json
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("RAMP_ACCESS_TOKEN")

endpoint = f"https://demo-api.ramp.com/developer/v1/accounting/field-options"

with open ("Procore/Data/projects.json", "r") as f:
    projects = json.load(f)

with open ("Ramp/Data/CustomAccountingFieldOptions.json", "r") as f:
    existing_options = json.load(f)


headers = {
  "Accept": "application/json",
  "Authorization": f"Bearer {token}",
  "Content-Type": "application/json",
}

payload = {
  "accounting_connection_id": None,
  "field_id": "106e5fa4-fa9f-4032-8f15-8559940dad0a",
  "options":[],
}

existing_ids = {opt["id"] for opt in existing_options["data"]}
print(existing_ids)

for project in projects:
    if not project["active"]:
        continue

    project_id_str = str(project["id"])

    if project_id_str in existing_ids:
        print(f"Already Exists | ID: {project_id_str}")
        continue

    payload["options"].append({
        "id": project["name"],
        "value": project["name"],
        "code": project_id_str
    })


# Only send the request if there are new options
if not payload["options"]:
    print("No new options to send to Ramp. Skipping POST.")
else:
    print(f"Sending {len(payload['options'])} new options to Ramp...")
    response = requests.post(
        endpoint,
        headers=headers,
        json=payload,
        timeout=30
    )
    print(response.status_code, response.text)