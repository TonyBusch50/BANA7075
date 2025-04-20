V2  4/20/25

# BANA7075 Final Project - A data scraper and combiner to pull recent sales and real estate data for the Cincinnati area.

py_GUI_Master_Controller - This GUI will automatically run all the scripts below on the last day of the month.  It also has an option to manuall initiate the scripts. Update the directories for the four python scripts listed below.

Hamilton_Co_DLer - This script downloads a parcel IDs into a csv file from Hamilton Co. Auditor of the current Months sales.  It timestamps the file with the date/time it was downloaded.  Update the save_directory to align with other scripts.  

Hamilton_Scraper - This script takes the parcel IDs and scrapes data from each property to include #bathrooms, #bedrooms, acerage, etc..  It then merges the data and timestamps the file with the new and reference date.  Update the sales_dir directory and the save_dir to align with other scripts.

Zip Extractor - This script goes to Redfin and scrapes the Median Days on Market for each zip code in Cincinnati and Hamilton County. It saves the data and timestamps.  Update the save_dir to align with other scripts.

Data_Merger - This script takes the csv file from the data scraper and the zip extractor and merges the data into one file.  It saves the date and timestamp of the new and reference files.  Update the Hamilton_dir, Redfin_zip_dir, and output_dir to align with other scripts.

