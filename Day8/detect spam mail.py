import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ABUSEIPDB_API_KEY")
IP = "8.8.8.8"

url = "https://api.abuseipdb.com/api/v2/check"

headers = {
    "Key": API_KEY,
    "Accept": "application/json"
}

params = {
    "ipAddress": IP,
    "maxAgeInDays": "90"
}

response = requests.get(url, headers=headers, params=params)

print(response.json())

if response.status_code == 200:
    print(response.json())
else:
    print("Error:", response.status_code)


data = response.json()["data"]

print("IP:", data["ipAddress"])
print("Abuse Score:", data["abuseConfidenceScore"])
print("Country:", data["countryCode"])
print("Total Reports:", data["totalReports"])
