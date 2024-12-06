import json
import urllib.request
import time
import os

# NOAA API endpoint and headers
BASE_URL = "https://www.ncdc.noaa.gov/cdo-web/api/v2/locations"
HEADERS = {
    "token": "ntwdxtAnGGYXMTpxkxHBfBzBZTRoBRXg"  # actual NOAA API token
}

# Maximum number of retries for failed requests
MAX_RETRIES = 3

# Function to fetch data with retries and exponential backoff
def fetch_data_with_retries(url):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            request = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(request) as response:
                if response.status != 200:
                    raise Exception(f"HTTP Error: {response.status}")
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error fetching data: {e}. Retrying {retries + 1}/{MAX_RETRIES}...")
            retries += 1
            time.sleep(2 ** retries)  # Exponential backoff
    raise Exception(f"Failed to fetch data after {MAX_RETRIES} retries.")

# Function to save the data to a JSON file in the specified folder
def save_to_file(data, filename, folder):
    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Define the full path for the file
    file_path = os.path.join(folder, filename)

    # Save the data to a JSON file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Main function to fetch data and save it in 39 JSON files
def main():
    jsonFile = "jsonFile"  # Folder to save the JSON files
    total_files = 39  # Number of files to create (39 pages of results)

    for i in range(total_files):
        offset = (i * 1000) + 1  # Incrementing the offset for pagination
        url = f"{BASE_URL}?limit=1000&offset={offset}"  # Construct the URL with the offset
        print(f"Fetching data for offset {offset}...")

        # Fetch the data with retries
        try:
            data = fetch_data_with_retries(url)
            # Define the filename
            filename = f"locations_{i}.json"
            # Save the data to the specified folder
            save_to_file(data, filename, jsonFile)
            print(f"Data saved to {jsonFile}/{filename}")
        except Exception as e:
            print(f"Failed to fetch data for offset {offset}: {e}")
        
        # Optional: 
        time.sleep(1)  # Adjust delay time if required

if __name__ == "__main__":
    main()
