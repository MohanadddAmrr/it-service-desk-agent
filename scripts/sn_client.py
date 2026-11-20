import os
import requests
from dotenv import load_dotenv

load_dotenv()

INSTANCE = os.getenv("SN_INSTANCE")
AUTH = (os.getenv("SN_USER"), os.getenv("SN_PASSWORD"))
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
TABLE_URL = f"{INSTANCE}/api/now/table/incident"


def create_incident(short_description, description, impact="3", urgency="3", category="inquiry"):
    payload = {
        "short_description": short_description,
        "description": description,
        "impact": impact,
        "urgency": urgency,
        "category": category,
    }
    response = requests.post(TABLE_URL, auth=AUTH, headers=HEADERS, json=payload, timeout=15)
    response.raise_for_status()
    result = response.json()["result"]
    return result["number"], result["sys_id"]


def get_incident(number):
    params = {
        "sysparm_query": f"number={number}",
        "sysparm_limit": 1,
        "sysparm_fields": "number,short_description,priority,state",
    }    
    response = requests.get(TABLE_URL, auth=AUTH, headers=HEADERS, params=params, timeout=15)
    response.raise_for_status()
    results = response.json()["result"]
    return results[0] if results else None


if __name__ == "__main__":
    try:
        number, sys_id = create_incident(
            "Teams audio not working", "Others can't hear me in calls", impact="3", urgency="2", category="software"
        )
        print(f"Created {number}")
        ticket = get_incident(number)
        print(f"Read back: {ticket}")
    except requests.HTTPError as e:
        print(f"ServiceNow error {e.response.status_code}: {e.response.text}")