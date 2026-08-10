import requests
from dotenv import load_dotenv
import os
from drugs import TARGET_DRUGS

#get FDA API key
load_dotenv()

#guide on how to extract data
# print(data["results"][0]["safetyreportid"])
# print(data["results"][0]["serious"])

#empty list to hold results for all drugs combined
combined_results = []

#target amount of records to fetch for each drug
TARGET_PER_DRUG = 2000

#page size
PAGE_SIZE = 300

#dict for debugging each drug's results
results_by_drug = {}    #dict for debugging

#for loop to iterate through the TARGET_DRUGS list and fetch data for each drug
for drug in TARGET_DRUGS:
        skip = 0
        collected_count = 0
        results_by_drug[drug] = []  #empty list for each drug in the dict
        print(f"Fetching data for {drug}...")
        while True:
                try:
                        response = requests.get("https://api.fda.gov/drug/event.json",
                                        params={"api_key": os.getenv("FDA_API_KEY"),
                                                "limit": PAGE_SIZE,
                                                "skip": skip,
                                                "search": f"patient.drug.medicinalproduct:\"{drug}\""},
                                                timeout=30
                                                )
                        data = response.json()

                        combined_results.extend(data["results"])
                        results_by_drug[drug].extend(data["results"])

                        collected_count += len(data["results"]) 

                except Exception as e:
                        print(f"Error fetching data for {drug}: {e}")
                        break

                if len(data["results"]) < PAGE_SIZE:   #loop breaks if below PAGE_SIZE - all results fetched
                        break  
                if collected_count >= TARGET_PER_DRUG:  #loop breaks if target amount of records fetched
                        break
        
        
                #if not all results fetched, skip by PAGE_SIZE to fetch next batch
                skip += PAGE_SIZE      