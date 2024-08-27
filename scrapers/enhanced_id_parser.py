import requests
import pandas as pd
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_json(url, filename):
       # Send a HTTP request to the url
       response = requests.get(url)
       
       # Check if the request was successful
       if response.status_code == 200:
           # Write the file contents to a local file
           with open(filename, 'w') as file:
               file.write(response.text)
           print("Download completed successfully!")
       else:
           print(f"Failed to download file, status code: {response.status_code}")

def retrieve_enhanced_id_results(name, link, dem_candidate_id, rep_candidate_id):
    # Set up Chrome options
    options = Options()
    options.headless = True  # Enable headless mode
    options.add_argument("--window-size=1920,1080")  # Define window size
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    json_filename = "{}.json".format(name)

    # Navigate to the page
    driver.get(link)

    try:
        # Wait for the element to be present
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Media Export')]"))
        )
        
        # Print the href attribute of the found element
        print("Found the link:", element.get_attribute('href'))

        # URL of the JSON file you want to download
        url = element.get_attribute('href')
        # Local path where you want to save the file
        download_json(url, json_filename)
    finally:
        driver.quit()  # Clean up: close the browser
    
    with open(json_filename, 'r') as file:
        data = json.load(file)

    # Access data
    ballot_options = data["results"]["ballotItems"][0]["ballotOptions"]

    total_vote_count = {}
    dem_votes = {}
    rep_votes = {}
    
    df_new = pd.DataFrame(columns=['PRECINCT', 'TOTAL', 'DEM', 'REP'])
    for option in ballot_options:
        for precinct in option["precinctResults"]:
            precint_name = precinct['name']

            if precint_name not in total_vote_count:
                total_vote_count[precint_name] = 0

            total_vote_count[precint_name]+=precinct['voteCount']

            if option["id"] == dem_candidate_id:
                dem_votes[precint_name] = precinct['voteCount']
            elif option["id"] == rep_candidate_id:
                rep_votes[precint_name] = precinct['voteCount']
    
    df_new = pd.DataFrame(columns=['PRECINCT', 'TOTAL', 'DEM', 'REP'])

    for precinct in total_vote_count:
        # Create a new row to add
        new_row = {'PRECINCT': precinct, 'TOTAL': total_vote_count[precinct], 'DEM': dem_votes[precinct], 'REP': rep_votes[precinct]}

        # Append the row to the DataFrame
        df_new = pd.concat([df_new, pd.DataFrame([new_row])], ignore_index=True)

    return df_new


