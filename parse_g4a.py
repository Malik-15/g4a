import requests
import yaml
import uuid
import random
import time
from datetime import datetime


# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


measurement_id = config["ga4"]["measurement_id"]
api_secret = config["ga4"]["api_secret"]

website_url = config["website"]["url"]

events = config["simulation"]["events"]

delay_min = config["simulation"]["delay_seconds"]["min"]
delay_max = config["simulation"]["delay_seconds"]["max"]


GA4_URL = (
    "https://www.google-analytics.com/mp/collect"
    f"?measurement_id={measurement_id}"
    f"&api_secret={api_secret}"
)



def send_event():

    client_id = str(uuid.uuid4())

    event_name = random.choice(events)


    payload = {

        "client_id": client_id,

        "events": [

            {

                "name": event_name,

                "params": {

                    "page_location": website_url,

                    "page_title": "G4A Learning Dashboard",

                    "engagement_time_msec":
                        random.randint(1000,15000),

                    "user_type":
                        random.choice(
                            [
                                "student",
                                "developer",
                                "engineer"
                            ]
                        ),

                    "timestamp":
                        datetime.utcnow().isoformat()

                }

            }

        ]

    }


    response = requests.post(
        GA4_URL,
        json=payload
    )


    if response.status_code == 204:

        print(
            "✓ Sent:",
            event_name,
            client_id[:8]
        )

    else:

        print(
            "GA4 Error:",
            response.status_code,
            response.text
        )




while True:

    send_event()

    wait = random.randint(
        delay_min,
        delay_max
    )

    time.sleep(wait)
