import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from pathlib import Path
import re
import os

# -------------------------------------
# CONFIGURATION
# -------------------------------------

SALES_DIR = Path("C:/BANA7075 Final Project/csv Hamilton Recent Monthly Sales")
SAVE_DIR = Path("C:/BANA7075 Final Project/csv Hamilton Data")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

DELAY_BETWEEN_REQUESTS = 0.25
MAX_RETRIES = 3

SCRAPE_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# -------------------------------------
# FIND MOST RECENT CSV FILE
# -------------------------------------

print("🔎 Searching for most recent sales CSV file...")
reference_files = list(SALES_DIR.glob("hamilton_sales_data_*.csv"))

if not reference_files:
    raise FileNotFoundError("❌ No matching CSV sales files found in the folder.")

REFERENCE_FILE = max(reference_files, key=os.path.getctime)
print(f"📂 Using file: {REFERENCE_FILE.name}")

# Extract timestamp from filename
match = re.search(r'(\d{8}_\d{6})', REFERENCE_FILE.name)
REFERENCE_TIMESTAMP = match.group(1) if match else "unknown"

EXPORT_FILENAME = f"Hamilton Data {SCRAPE_TIMESTAMP} _ {REFERENCE_TIMESTAMP}.csv"
EXPORT_PATH = SAVE_DIR / EXPORT_FILENAME

# -------------------------------------
# SCRAPER FUNCTION
# -------------------------------------

def extract_with_label(soup, label):
    tag = soup.find(string=label)
    return tag.find_next("td").get_text(strip=True) if tag and tag.find_next("td") else None

def scrape_auditor_data(parcel_id, retries=0):
    base_url = f"https://wedge.hcauditor.org/view/re/{parcel_id}/2024"
    summary_url = f"{base_url}/summary"
    appraisal_url = f"{base_url}/appraisal"
    data = {"Parcel ID": parcel_id}

    try:
        response_summary = requests.get(summary_url, timeout=10)
        soup_sum = BeautifulSoup(response_summary.text, 'html.parser')
        data.update({
            "Year Built": extract_with_label(soup_sum, "Year Built"),
            "Total Rooms": extract_with_label(soup_sum, "Total Rooms"),
            "# Bedrooms": extract_with_label(soup_sum, "# Bedrooms"),
            "# Full Bathrooms": extract_with_label(soup_sum, "# Full Bathrooms"),
            "# Half Bathrooms": extract_with_label(soup_sum, "# Half Bathrooms"),
            "Last Transfer Date": extract_with_label(soup_sum, "Last Transfer Date"),
            "Last Sale Amount": extract_with_label(soup_sum, "Last Sale Amount"),
            "Conveyance Number": extract_with_label(soup_sum, "Conveyance Number"),
            "Deed Type": extract_with_label(soup_sum, "Deed Type"),
            "Deed Number": extract_with_label(soup_sum, "Deed Number"),
            "# of Parcels Sold": extract_with_label(soup_sum, "# of Parcels Sold"),
            "Acreage": extract_with_label(soup_sum, "Acreage"),
            "Board of Revision": extract_with_label(soup_sum, "Board of Revision"),
            "Rental Registration": extract_with_label(soup_sum, "Rental Registration"),
            "Homestead": extract_with_label(soup_sum, "Homestead"),
            "Owner Occupancy Credit": extract_with_label(soup_sum, "Owner Occupancy Credit"),
            "Foreclosure": extract_with_label(soup_sum, "Foreclosure"),
            "Special Assessments": extract_with_label(soup_sum, "Special Assessments"),
            "Market Land Value": extract_with_label(soup_sum, "Market Land Value"),
            "CAUV Value": extract_with_label(soup_sum, "CAUV Value"),
            "Market Improvement Value": extract_with_label(soup_sum, "Market Improvement Value"),
            "Market Total Value": extract_with_label(soup_sum, "Market Total Value"),
            "TIF Value": extract_with_label(soup_sum, "TIF Value"),
            "Abated Value": extract_with_label(soup_sum, "Abated Value"),
            "Exempt Value": extract_with_label(soup_sum, "Exempt Value"),
            "Taxes Paid": extract_with_label(soup_sum, "Taxes Paid")
        })
    except Exception as e:
        data["Summary Error"] = str(e)

    try:
        response_appraisal = requests.get(appraisal_url, timeout=10)
        soup_app = BeautifulSoup(response_appraisal.text, 'html.parser')
        data.update({
            "Style": extract_with_label(soup_app, "Style"),
            "Exterior Wall Type": extract_with_label(soup_app, "Exterior Wall Type"),
            "Basement Type": extract_with_label(soup_app, "Basement Type"),
            "Heating": extract_with_label(soup_app, "Heating"),
            "Air Conditioning": extract_with_label(soup_app, "Air Conditioning"),
            "# Fireplaces": extract_with_label(soup_app, "# of Fireplaces"),
            "Basement Garage - Car Capacity": extract_with_label(soup_app, "Basement Garage - Car Capacity"),
            "Stories": extract_with_label(soup_app, "Stories"),
            "Finished Square Footage": extract_with_label(soup_app, "Finished Square Footage"),
            "First Floor Area (sq. ft.)": extract_with_label(soup_app, "First Floor Area (sq. ft.)"),
            "Upper Floor Area (sq. ft.)": extract_with_label(soup_app, "Upper Floor Area (sq. ft.)"),
            "Half Floor Area (sq. ft.)": extract_with_label(soup_app, "Half Floor Area (sq. ft.)"),
            "Finished Basement (sq. ft.)": extract_with_label(soup_app, "Finished Basement (sq. ft.)"),
            "Attached/Integral Garage": extract_with_label(soup_app, "Attached/Integral Garage"),
            "Deck": extract_with_label(soup_app, "Deck")
        })
    except Exception as e:
        data["Appraisal Error"] = str(e)

    return data

# -------------------------------------
# MAIN SCRIPT
# -------------------------------------

print("📄 Loading CSV file...")
df_sales = pd.read_csv(REFERENCE_FILE)
df_sales.columns = [col.lower() for col in df_sales.columns]

required_cols = {"book", "plat", "parcel"}
if not required_cols.issubset(df_sales.columns):
    raise Exception("❌ Input file must contain BOOK, PLAT, and PARCEL columns (case-insensitive).")

df_sales["Parcel ID"] = (
    df_sales["book"].astype(str).str.zfill(3) +
    df_sales["plat"].astype(str).str.zfill(4) +
    df_sales["parcel"].astype(str).str.zfill(4) +
    "00"
)

print(f"🔍 Scraping data for {len(df_sales)} parcels...")
scraped_data = []
for i, row in df_sales.iterrows():
    parcel_id = row["Parcel ID"]
    print(f"  → [{i+1}/{len(df_sales)}] Parcel ID: {parcel_id}")
    details = scrape_auditor_data(parcel_id)
    scraped_data.append(details)
    time.sleep(DELAY_BETWEEN_REQUESTS)

df_scraped = pd.DataFrame(scraped_data)
df_combined = pd.merge(df_sales, df_scraped, on="Parcel ID", how="left")
df_combined.to_csv(EXPORT_PATH, index=False)

print(f"✅ Done! Data saved to:\n{EXPORT_PATH.resolve()}")