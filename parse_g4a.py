import requests
from bs4 import BeautifulSoup
import yaml
import json
import random
from datetime import datetime


# Load configuration
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)


url = config["website"]["url"]

output_file = config["output"]["file"]

samples = config["simulation"]["generate_samples"]


# -------------------------
# Download Website
# -------------------------

response = requests.get(url)

if response.status_code != 200:
    raise Exception(
        f"Website loading failed: {response.status_code}"
    )


html = response.text


# -------------------------
# Parse HTML
# -------------------------

soup = BeautifulSoup(
    html,
    "html.parser"
)


# Title

title = soup.title.text.strip() if soup.title else None


# Headings

headings = []

for tag in soup.find_all(["h1", "h2", "h3"]):

    headings.append(
        tag.get_text(strip=True)
    )


# Paragraphs

paragraphs = []

for p in soup.find_all("p"):

    text = p.get_text(strip=True)

    if text:
        paragraphs.append(text)



# Links

links = []

for a in soup.find_all("a", href=True):

    links.append(
        {
            "text": a.get_text(strip=True),
            "url": a["href"]
        }
    )



# -------------------------
# Generate Simulation Data
# -------------------------

simulation = []


for i in range(samples):

    record = {

        "id": i + 1,

        "timestamp":
        datetime.utcnow().isoformat(),

        "temperature":
        round(random.uniform(20,80),2),

        "pressure":
        round(random.uniform(950,1050),2),

        "system_status":
        random.choice(
            [
                "Normal",
                "Warning",
                "Critical"
            ]
        )
    }


    simulation.append(record)



# -------------------------
# Save Result
# -------------------------

output = {

    "website":
    {
        "url": url,
        "title": title
    },

    "content":
    {
        "headings": headings,
        "paragraphs": paragraphs,
        "links": links
    },

    "simulation_data":
    simulation
}



with open(output_file,"w",encoding="utf-8") as file:

    json.dump(
        output,
        file,
        indent=4,
        ensure_ascii=False
    )


print("Parsing completed")
print(f"Saved to {output_file}")
