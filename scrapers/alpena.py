import requests
import pdfplumber
import pandas as pd


PDF_DOWNLOAD_LINK = "https://www.alpenacounty.org/DocumentCenter/View/1257/2022-November-PDF"
PAGE_START = 2
PAGE_END = 2

PRECINCT_COLUMN = 0
TOTAL_VOTE_COLUMN = 1
DEM_CANDIDATE_VOTE_COLUMN = 3
REP_CANDIDATE_VOTE_COLUMN = 4

START_ROW = 4
END_ROW = 12


def combine_tables_horizontally(table1, table2):
    # Ensure both tables have the same number of rows
    assert len(table1) == len(table2), "Tables do not have the same number of rows"
    
    # Initialize the combined table
    combined_table = []
    
    # Iterate through each row index
    for row1, row2 in zip(table1, table2):
        # Combine the rows and add to the combined table
        combined_row = row1 + row2
        combined_table.append(combined_row)
    
    return combined_table

def download_pdf(url, filename):
    # Send a HTTP GET request to the URL
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Write the content of the response to a file
        with open(filename, 'wb') as f:
            f.write(response.content)
        print("PDF downloaded successfully")
    else:
        print("Failed to retrieve PDF")

download_pdf(PDF_DOWNLOAD_LINK, "alpena.pdf")

with pdfplumber.open("alpena.pdf") as pdf:
    # Loop through the specified range of pages
    for i in range(PAGE_START, PAGE_END + 1):
        page = pdf.pages[i]

        rotation = page.rotation

        # Extract table or text based on the rotation
        if rotation in [90, 270]:
            # Assuming the page needs horizontal reading, we adjust parameters or use custom extraction logic
            # This example just rotates the page for illustration; adapt based on actual data layout
            extracted_data = page.extract_tables(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text"})
        else:
            # Normal extraction
            extracted_data = page.extract_tables()

        if extracted_data:
            combined_table = extracted_data[0]
            if len(extracted_data) > 1:
                combined_table = combine_tables_horizontally(extracted_data[0], extracted_data[1])
            else: 
                combined_table = extracted_data[0]

            combined_table = combined_table[START_ROW:END_ROW]
            combined_table = [[item for item in inner_array if item is not None and item != ''] for inner_array in combined_table]
            #print(extracted_data)
            temp_df = pd.DataFrame(combined_table)

            print(temp_df.iloc[5])

            #print(temp_df.loc[1])

            df_new = pd.DataFrame(columns=['PRECINCT', 'TOTAL', 'DEM', 'REP'])

            #print(temp_df)

            df_new['PRECINCT'] = temp_df.iloc[:, PRECINCT_COLUMN]  # Adjust 1 to the column index for precincts
            df_new['TOTAL'] = temp_df.iloc[:, TOTAL_VOTE_COLUMN]  
            df_new['DEM'] = temp_df.iloc[:, DEM_CANDIDATE_VOTE_COLUMN]       # Adjust 3 to the column index for DEM votes
            df_new['REP'] = temp_df.iloc[:, REP_CANDIDATE_VOTE_COLUMN]       # Adjust 5 to the column index for REP votes
            
            print(df_new)

