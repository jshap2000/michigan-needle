import requests
import pdfplumber
import pandas as pd


PDF_DOWNLOAD_LINK = "https://www.allegancounty.org/home/showpublisheddocument/9918/638043705361370000"
PAGE_START = 1
PAGE_END = 2

PRECINCT_COLUMN = 0
DEM_CANDIDATE_VOTE_COLUMN = 1
REP_CANDIDATE_VOTE_COLUMN = 1

START_ROW = 1
END_ROW = 50


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

#download_pdf(PDF_DOWNLOAD_LINK, "allegan.pdf")

total_extracted_data = []
with pdfplumber.open("allegan.pdf") as pdf:
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
        
        if i == PAGE_START:
            total_extracted_data+=extracted_data[-1]
        else:
            total_extracted_data+=extracted_data[0]
        
    if total_extracted_data:
        temp_df = pd.DataFrame(total_extracted_data[START_ROW:END_ROW])

        column_indices = [1, 2, 3, 4]  # These indices correspond to columns 'A', 'B', 'C'
        temp_df['TOTAL'] = temp_df.iloc[:, column_indices].sum(axis=1)
        print(temp_df.loc[0])

        #print(temp_df.loc[1])

        df_new = pd.DataFrame(columns=['PRECINCT', 'TOTAL', 'DEM', 'REP'])

            #print(temp_df)

        df_new['PRECINCT'] = temp_df.iloc[:, 0]  # Adjust 1 to the column index for precincts
        # TODO: total
        #df_new['TOTAL'] = temp_df.iloc[:, 1]  
        df_new['DEM'] = temp_df.iloc[:, 1]       # Adjust 3 to the column index for DEM votes
        df_new['REP'] = temp_df.iloc[:, 2]       # Adjust 5 to the column index for REP votes
                # Specify the column indices to sum


