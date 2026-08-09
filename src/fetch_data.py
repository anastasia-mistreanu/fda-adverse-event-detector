import requests
from dotenv import load_dotenv
import os

load_dotenv()

#get FDA API key
response = requests.get("https://api.fda.gov/drug/event.json",
                        params={"api_key": os.getenv("FDA_API_KEY"),
                                "limit": 1}
                                )
data = response.json()

#extract necessary information from the response
print(data["results"][0]["safetyreportid"])
print(data["results"][0]["serious"])




