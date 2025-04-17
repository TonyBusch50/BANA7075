import pandas as pd
from pathlib import Path
import os
from datetime import datetime
import re

# -----------------------------------
# CONFIGURATION
# -----------------------------------
hamilton_dir = Path(r"C:\BANA7075 Final Project\csv Hamilton Data")
redfin_zip_dir = Path(r"C:\BANA7075 Final Project\csv Redfin Data\Zip Code Sell Time")
output_dir = Path(r"C:\BANA7075 Final Project\csv Merged Data")
output_dir.mkdir(parents=True, exist_ok=True)

# -----------------------------------
# FIND MOST RECENT FILES
# -----------------------------------
def get_most_recent_file(directory: Path, pattern: str = "*.csv") -> Path:
    files = list(directory.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {directory}")
    return max(files, key=lambda f: f.stat().st_mtime)

hamilton_file_path = get_most_recent_file(hamilton_dir)
redfin_zip_file_path = get_most_recent_file(redfin_zip_dir)

# -----------------------------------
# LOAD DATA
# -----------------------------------
df_hamilton = pd.read_csv(hamilton_file_path)
df_redfin_zip = pd.read_csv(redfin_zip_file_path)

# -----------------------------------
# CLEAN AND PREPARE ZIP CODES
# -----------------------------------
df_hamilton['Zip_Code'] = (
    df_hamilton['locationzipcode']
    .astype(str)
    .str.extract(r'(\d{5})')[0]
    .fillna('00000')
)

df_redfin_zip['Zip Code'] = df_redfin_zip['Zip Code'].astype(str).str.zfill(5)

# -----------------------------------
# MERGE ON ZIP CODE
# -----------------------------------
merged_df = pd.merge(
    df_hamilton,
    df_redfin_zip,
    how='left',
    left_on='Zip_Code',
    right_on='Zip Code'
)

merged_df.rename(columns={'Median Days on Market': 'Estimated_Days_On_Market'}, inplace=True)

# -----------------------------------
# BUILD OUTPUT FILENAME WITH TIMESTAMPS
# -----------------------------------
def extract_timestamp_from_filename(filename):
    match = re.search(r'\d{8}_\d{6}', filename)
    return match.group(0) if match else 'unknown'

hamilton_timestamp = extract_timestamp_from_filename(hamilton_file_path.name)
redfin_timestamp = extract_timestamp_from_filename(redfin_zip_file_path.name)
created_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

output_filename = (
    f"hamilton_zip_merge__hamilton_{hamilton_timestamp}__redfin_{redfin_timestamp}__created_{created_timestamp}.csv"
)
output_path = output_dir / output_filename

# -----------------------------------
# SAVE TO CSV
# -----------------------------------
merged_df.to_csv(output_path, index=False)
print(f"✅ File saved:\n{output_path}")