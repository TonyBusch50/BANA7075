# BANA7075 Final Project
GUI to operate multiple data scrapers and merge the data for ingestion.

Hamilton_Co_DLer - This script downloads a parcel IDs into a csv file from Hamilton Co. Auditor of the current Months sales.  It timestamps the file with the date/time it was downloaded.  Update the save directory to align with other scripts.  

Hamilton_Scraper - This script takes the parcel IDs and scrapes data from each property to include #bathrooms, #bedrooms, acerage, etc..  It then merges the data and timestamps the file with the new and reference date.  Update the sales_dir directory and the the save_dir.

