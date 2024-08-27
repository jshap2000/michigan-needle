import requests
import pdfplumber
import pandas as pd

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

def retrieve_simple_pdf_results(name, link, start_page, end_page, start_row, end_row, should_skip_every_other_page, precinct_column, total_vote_column, dem_column, rep_column):
    pdf_filename = "{}.pdf".format(name)

    download_pdf(link, pdf_filename)

    with pdfplumber.open(pdf_filename) as pdf:
        # Loop through the specified range of pages
        for i in range(start_page, end_page + 1):
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
                
                temp_df = pd.DataFrame(combined_table[start_row:end_row])

                df_new = pd.DataFrame(columns=['PRECINCT', 'TOTAL', 'DEM', 'REP'])

                # TODO: DIGIT TRIMMING

                df_new['PRECINCT'] = temp_df.iloc[:, precinct_column]  # Adjust 1 to the column index for precincts
                df_new['TOTAL'] = temp_df.iloc[:, total_vote_column]  
                df_new['DEM'] = temp_df.iloc[:, dem_column]       # Adjust 3 to the column index for DEM votes
                df_new['REP'] = temp_df.iloc[:, rep_column]       # Adjust 5 to the column index for REP votes
                
                return df_new

