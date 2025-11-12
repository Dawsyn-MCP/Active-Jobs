from dotenv import load_dotenv
import os, base64, requests

load_dotenv()

client_id = os.getenv("RAMP_CLIENT_ID")
client_secret = os.getenv("RAMP_CLIENT_SECRET")

auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

headers = {
  "Authorization": f"Basic {auth}",
  "Content-Type": "application/x-www-form-urlencoded"
}

data = {
  "grant_type": "client_credentials",
  "scope": "transactions:read accounting:read accounting:write",
}


if not client_id or not client_secret:
    raise Exception("Missing RAMP_CLIENT_ID or RAMP_CLIENT_SECRET")

resp = requests.post("https://demo-api.ramp.com/developer/v1/token", headers=headers, data=data)

# Production
# resp = requests.post("https://api.ramp.com/developer/v1/token", headers=headers, data=data)


# Check if request was successful
if resp.status_code == 200:
    access_token = resp.json().get("access_token", "")

    script_dir = os.path.dirname(__file__)  # Current script directory
    env_file = os.path.join(script_dir, "..", ".env")

    env_vars = {}
    if os.path.exists(env_file):
        with open(env_file, "r") as file:
            for line in file:
                key, _, value = line.strip().partition("=")
                env_vars[key] = value.strip("'")  # Remove any existing quotes

    # Write updated .env file
    with open(env_file, "w") as file:
        for key, value in env_vars.items():
            file.write(f"{key}='{value}'\n")

    # Update only the ACCESS_TOKEN, keeping others intact
    env_vars["RAMP_ACCESS_TOKEN"] = access_token

    # Write updated .env file
    with open(env_file, "w") as file:
        for key, value in env_vars.items():
            file.write(f"{key}='{value}'\n")

        print(f"✅ Access token saved successfully in {env_file}!")
    print("Access Token:", access_token)

else:
    print("❌ Failed to get access token:", resp.status_code, resp.text)