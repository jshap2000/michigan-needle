import pandas as pd
import re
import requests
import zipfile
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

COLUMN_TO_DROP = 1
OVERSIZED = 9

def unzip_file(zip_path, extract_to='.'):
    """
    Unzip a ZIP file to the specified directory.

    Args:
    zip_path (str): The path to the zip file.
    extract_to (str): The directory to extract the files into.
    """
    # Ensure the extraction directory exists
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    # Open the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all the contents into the directory
        zip_ref.extractall(extract_to)
        print(f'Files extracted to {extract_to}')

def delete_around_words(file_path, start_word, end_word):
    # Read the content of the file
    with open(file_path, 'r') as file:
        content = file.read()

    # Find the position of the start word and cut the content up to that word
    start_pos = content.find(start_word)
    if start_pos != -1:
        # Adding len(start_word) to include the word itself in the cut
        content = content[start_pos + len(start_word):]
    else:
        content = content

    # Find the position of the end word and cut the content from that word onward
    end_pos = content.find(end_word)
    if end_pos != -1:
        content = content[:end_pos]
    else:
        content = content

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

def retrieve_clarity_elections_results(name, link, start_word, end_word, precinct_column, total_vote_column, dem_column, rep_column):
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

    zip_filename = "{}.zip".format(name)
    txt_filename = "{}.txt".format(name)

    # Navigate to the page
    driver.get(link)

    try:
        # Set a timeout for the WebDriverWait
        timeout = 30  # seconds

        # Wait until the element with the specified aria-label is found
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[aria-label="Download Detail TXT"]'))
        )
        href = element.get_attribute('href')
        # Download the ZIP file from the href
        response = requests.get(href)
        # Specify the filename you want to save the downloaded file as
        custom_filename = zip_filename
        custom_file_path = os.path.join(os.getcwd(), custom_filename)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(href, headers=headers)
        if response.status_code == 200:
            with open(custom_file_path, 'wb') as f:
                f.write(response.content)
            print(f"ZIP file downloaded successfully: {custom_file_path}")
            
            unzip_file(custom_file_path)
            os.rename("detail.txt", txt_filename)
        else:
            print(f"Failed to download ZIP file, status code: {response.status_code}")
    finally:
        driver.quit()  # Clean up: close the browser

    delete_around_words(txt_filename, start_word, end_word)

    # Read the file into a list of lines
    with open(txt_filename, 'r') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        # Split the line on sequences of spaces (at least two spaces as a safe assumption)
        columns = re.split(r'\s{3,}', line.strip())

        if len(columns) == OVERSIZED:
            columns = columns[0:COLUMN_TO_DROP] + columns[COLUMN_TO_DROP+1:]

        if len(columns) > 5:
            data.append(columns)

    df = pd.DataFrame(data[1:], columns=data[0])

    df_new = pd.DataFrame(columns=['PRECINCT', 'TOTAL', 'DEM', 'REP'])

                # TODO: DIGIT TRIMMING

    df_new['PRECINCT'] = df.iloc[:, precinct_column]  # Adjust 1 to the column index for precincts
    df_new['TOTAL'] = df.iloc[:, total_vote_column]  
    df_new['DEM'] = df.iloc[:, dem_column]       # Adjust 3 to the column index for DEM votes
    df_new['REP'] = df.iloc[:, rep_column]       # Adjust 5 to the column index for REP votes
    return df_new