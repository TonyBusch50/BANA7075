import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from pathlib import Path
import re

# -------------------------------
# CONFIGURATION
# -------------------------------
ZIP_CODES = [
    '45202', '45204', '45205', '45206', '45207', '45208', '45209', '45210',
    '45211', '45212', '45213', '45214', '45215', '45216', '45217', '45218', '45219', '45220',
    '45223', '45224', '45225', '45226', '45227', '45229', '45230',
    '45231', '45232', '45233', '45236', '45237', '45238', '45239', '45240',
    '45241', '45242', '45243', '45244', '45245', '45246', '45247', '45248', '45249', 
    '45251', '45252', '45255', '45277'
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SAVE_DIR = Path(r"C:\BANA7075 Final Project\csv Redfin Data\Zip Code Sell Time")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"median_days_on_market_{timestamp}.csv"
save_path = SAVE_DIR / filename

# -------------------------------
# SCRAPING FUNCTION
# -------------------------------

def get_median_days(zip_code):
    url = f'https://www.redfin.com/zipcode/{zip_code}/housing-market'
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)

    # Search for pattern like "Median Days on Market 48"
    match = re.search(r"Median Days on Market\s+(\d+)", text)
    if match:
        return match.group(1)
    return None

# -------------------------------
# MAIN SCRIPT
# -------------------------------

results = []

for zip_code in ZIP_CODES:
    days = get_median_days(zip_code)
    print(f"{zip_code}: {days}")
    results.append((zip_code, days))

# Save to CSV
with open(save_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Zip Code', 'Median Days on Market'])
    writer.writerows(results)

print(f"\n✅ Saved data to: {save_path}")