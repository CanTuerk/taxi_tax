import time
from playwright.sync_api import sync_playwright
from pprint import pprint
import requests
import json
import xml.etree.ElementTree as ET

min_date = "03.09.2025"
max_date = "09.02.2025"

filters = {
    "groupOp": "AND",
    "rules": [
        {"field": "TW_DATE_START", "op": "ge", "data": min_date},
        {"field": "TW_DATE_START", "op": "le", "data": max_date},
    ],
}

# Query parameters
params = {
    "_search": "true",
    "nd": str(int(time.time() * 1000)),
    "rows": 20,
    "page": 1,
    "sidx": "id",
    "sord": "desc",
    "filters": json.dumps(filters),  # Convert filters to a JSON string
}

personalNr = 43
taxometer_table = "https://www.starkcenter.de/script/module/abrechnungsdaten/kernel_dataview.php?q=1&content=show"
user_taxometer_table = "https://www.starkcenter.de/script/module/abrechnungsdaten/subgrid.php?option=stand&content=show&id=24148082&_search=false&nd=1739315213712&rows=1000&page=1&sidx=TIM_SEQ_NO_TRANSACTION&sord=asc"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Navigate to the login page
    page.goto("https://www.starkcenter.de/index.php")

    # Fill out the login form
    page.fill("#username", "MicoTaxi")
    page.fill("#password", "Ali2736?")
    page.click("#login")

    # Wait for login to complete
    page.wait_for_load_state("networkidle")

    playwright_cookies = page.context.cookies()

    page.goto("https://www.starkcenter.de/script/dataview.php")
    page.wait_for_timeout(5000)

    # Extract cookies
    browser.close()

# Convert cookies for requests
session = requests.Session()
for cookie in playwright_cookies:
    print(cookie["name"], cookie["value"])
    session.cookies.set(cookie["name"], cookie["value"])

# Use session for further authenticated requests
response = session.post(taxometer_table, params=params)

print(response.content)
xml_data = response.text
# pprint(response.text)  # Print a snippet

root = ET.fromstring(xml_data)
for row in root.findall(".//row"):
    row_id = row.attrib.get("id")  # `.get()` avoids KeyError

    if row_id:  # Only process rows that have an ID
        cells = row.findall("cell")

        if len(cells) >= 4:
            print(f"Row ID: {row_id}, Fourth Cell: {cells[3].text}")
