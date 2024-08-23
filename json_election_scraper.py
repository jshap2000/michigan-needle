import requests
from bs4 import BeautifulSoup
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

def parse_json_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Access data
    ballotOptions = data["results"]["ballotItems"][0]["ballotOptions"]

    for option in ballotOptions:
        print(option["name"])
        for precinct in option["precinctResults"]:
            print(precinct['name'])
            print(precinct['voteCount'])

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

# URL to navigate to
url = "https://app.enhancedvoting.com/results/public/saginaw-county-MI/elections/August2024Primary"

# Navigate to the page
driver.get(url)

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
    filename = 'downloaded_data.json'
    download_json(url, filename)
    parse_json_data(filename)
finally:
    driver.quit()  # Clean up: close the browser


