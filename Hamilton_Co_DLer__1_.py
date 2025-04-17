import requests
import os
from datetime import datetime
from tqdm import tqdm  # Install with: pip install tqdm

# --------------------------------------------
# Instructions:
# This script downloads a CSV file from the Hamilton County Auditor site with a progress bar.
# If the download is interrupted or incomplete, it deletes the partial file and shows an error.
# --------------------------------------------

# Define save location
save_directory = r"C:\BANA7075 Final Project\csv Hamilton Recent Monthly Sales"
os.makedirs(save_directory, exist_ok=True)

# Hamilton County Auditor sales data URL
url = "https://www.hamiltoncountyauditor.org/download/transfer_dailysales_new.csv"

# Generate timestamped filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"hamilton_sales_data_{timestamp}.csv"
save_path = os.path.join(save_directory, filename)

def download_file_with_progress(download_url, destination_path):
    """Download a file from a URL with progress tracking and safe interruption handling."""
    progress_bar = None

    try:
        print(f"Starting download from: {download_url}")
        response = requests.get(download_url, stream=True, timeout=10)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        downloaded_size = 0

        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Downloading")

        with open(destination_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=block_size):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress_bar.update(len(chunk))

        progress_bar.close()

        if downloaded_size < total_size:
            raise Exception("Download incomplete. Only part of the file was received.")

        print(f"\n✅ File successfully downloaded and saved to: {destination_path}")

    except KeyboardInterrupt:
        if progress_bar:
            progress_bar.close()
        print("\n❌ Download canceled by user.")
        if os.path.exists(destination_path):
            os.remove(destination_path)
            print("🗑️ Incomplete file deleted.")
    except Exception as e:
        if progress_bar:
            progress_bar.close()
        print(f"\n❌ Error during download: {e}")
        if os.path.exists(destination_path):
            os.remove(destination_path)
            print("🗑️ Incomplete file deleted.")

# Start the download
download_file_with_progress(url, save_path)