import requests
import zipfile
import os


def download_dams_data():
    """
    Download the data of dams in Germany from the GFZ Data Repository.
    
    """
    # URL of the data
    url = "https://datapub.gfz-potsdam.de/download/10.5880.GFZ.4.4.2020.005iwU/Dams_in_Germany_v.1.0.zip"

    # Download the data
    r = requests.get(url)
    with open("/input_data/Dams_in_Germany_v.1.0.zip", "wb") as f:
        f.write(r.content)

    # Unzip the data
    with zipfile.ZipFile("/input_data/Dams_in_Germany_v.1.0.zip", 'r') as zip_ref:
        zip_ref.extractall("/input_data")

    # Remove the zip file
    os.remove("/input_data/Dams_in_Germany_v.1.0.zip")

    print("Input data downloaded successfully.")


if __name__ == "__main__":
    download_dams_data()