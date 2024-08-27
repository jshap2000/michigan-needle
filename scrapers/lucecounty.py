import requests
import pdfplumber
import pandas as pd
import tabula
import PyPDF2


PDF_DOWNLOAD_LINK = "https://www.lucecountymi.com/_files/ugd/e707c7_68a32b04fcfd46e7a8b039485d8589c3.pdf"
PAGE_START = 2
PAGE_END = 2

PRECINCT_COLUMN = 0
TOTAL_COLUMN = 1
DEM_CANDIDATE_VOTE_COLUMN = 4
REP_CANDIDATE_VOTE_COLUMN = 6

START_ROW = 3
END_ROW = 18

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

download_pdf(PDF_DOWNLOAD_LINK, "luce.pdf")

def extract_pages(input_path, output_path, start_page, end_page):
    # Open the existing PDF
    with open(input_path, "rb") as input_file:
        reader = PyPDF2.PdfReader(input_file)
        
        # Create a PDF writer for the output PDF
        writer = PyPDF2.PdfWriter()

        # Ensure page numbers are within the original document's range
        num_pages = len(reader.pages)
        if start_page < 1 or end_page > num_pages:
            raise ValueError(f"Page range must be within the range of 1 to {num_pages} (inclusive).")
        
        # Add pages from the specified range to the writer object
        for i in range(start_page - 1, end_page):  # adjusting index since Python uses 0-based index
            writer.add_page(reader.pages[i])

        # Write the new PDF
        with open(output_path, "wb") as output_file:
            writer.write(output_file)

        print(f"New PDF has been created from page {start_page} to {end_page} and saved to {output_path}")

# Usage example:
input_pdf_path = 'luce.pdf'
output_pdf_path = 'luce.pdf'
start_page = PAGE_START # Start of the page range (inclusive)
end_page = PAGE_END    # End of the page range (inclusive)

extract_pages(input_pdf_path, output_pdf_path, start_page, end_page)
   


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

# The path to your PDF file
file_path = "luce.pdf"

# Use tabula to read tables in the PDF
# You might need to adjust pages and multiple_tables based on your specific PDF
tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True)

print(tables)

# Iterate over extracted tables
for i, table in enumerate(tables):
    print(f"Table {i+1}")
    print(table)
    # Optionally, convert table data to a CSV file
    table.to_csv(f"table_{i+1}.csv", index=False)

    