import requests
import os
from dotenv import load_dotenv

load_dotenv()

#accessing the environment variables
auth_code = os.getenv("AUTH_CODE")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

# Define the URL
url = "https://login-sandbox.procore.com/oauth/token/"

# Define the payload (as x-www-form-urlencoded)
payload = {
    "grant_type": "authorization_code",
    "code": auth_code,  
    "client_id": client_id,      
    "client_secret": client_secret,  
    "redirect_uri": redirect_uri  
}

# Set the headers
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

print(f"CLIENT_ID: {client_id}")
print(f"CLIENT_SECRET: {client_secret}")


# Make the POST request
response = requests.post(url, data=payload, headers=headers)
if response.status_code == 200:
    print("success")
else:
    print("failed")


# Check if request was successful
if response.status_code == 200:
    access_token = response.json().get("access_token", "")
    refresh_token = response.json().get("refresh_token", "")

    # Get the correct Procore directory path
    script_dir = os.path.dirname(__file__)  # Current script directory
    procore_dir = os.path.join(script_dir, "Procore")  # Path to Procore folder
    env_file = os.path.join(script_dir, ".env")  # Path to .env inside Procore

    # Read existing environment variables
    env_vars = {}
    if os.path.exists(env_file):
        with open(env_file, "r") as file:
            for line in file:
                key, _, value = line.strip().partition("=")
                env_vars[key] = value.strip("'")  # Remove any existing quotes

    # Update only the ACCESS_TOKEN and REFRESH_TOKEN, keeping others intact
    env_vars["ACCESS_TOKEN"] = access_token
    env_vars["REFRESH_TOKEN"] = refresh_token

    # Write updated .env file
    with open(env_file, "w") as file:
        for key, value in env_vars.items():
            file.write(f"{key}='{value}'\n")

    print(f"✅ Access token saved successfully in {env_file}!")
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)

else:
    print("❌ Failed to get access token:", response.status_code, response.text)