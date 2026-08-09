print("test")

from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("FDA_API_KEY")
print(f"Loaded FDA API Key: {api_key}")
