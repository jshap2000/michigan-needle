import pdfplumber
import pandas as pd

pdf_path = 'output.pdf'

import fitz  # PyMuPDF
import tabula

def edit_text_in_pdf(pdf_path, output_path, search_text, replacement_text):
    doc = fitz.open(pdf_path)
    for page in doc:
        text_instances = page.search_for(search_text)
        
        for inst in text_instances:
            # Redact the text
            redact = page.add_redact_annot(inst, text="", fill=(1, 1, 1))
            redact.set_border(width=0)  # No border
            redact.update()

        # Apply the redactions, which permanently removes the text
        page.apply_redactions()

        # Optional: if you want to add new text exactly where the old was, do it here
        # This assumes you want the new text to be visible and not just a redaction replacement
        for inst in text_instances:
            # Adjust x, y coordinates as necessary, perhaps based on the inst bounds
            x, y = inst[0], inst[3]  # Bottom left of the bounding box
            page.insert_text((x, y), replacement_text, fontsize=11, color=(0, 0, 0))

    doc.save(output_path)

edit_text_in_pdf("baragacounty_results.pdf", "output.pdf", "Joseph R. Biden /Kamala D. Harris (DEM)", "New Text")

# Create an empty DataFrame
df = pd.DataFrame()
start_page = 7  # Start page (0-indexed, adjust as needed)
end_page = 7    # End page (0-indexed, adjust as needed)

# Create an empty DataFrame to store data from all pages
all_pages_data = pd.DataFrame()

with pdfplumber.open(pdf_path) as pdf:
    # Loop through the specified range of pages
    for i in range(start_page, end_page + 1):
        page = pdf.pages[i]

        rotation = page.rotation

        # Extract table or text based on the rotation
        if rotation in [90, 270]:
            # Assuming the page needs horizontal reading, we adjust parameters or use custom extraction logic
            # This example just rotates the page for illustration; adapt based on actual data layout
            extracted_data = page.extract_table(table_settings={"vertical_strategy": "text", "horizontal_strategy": "text"})
        else:
            # Normal extraction
            extracted_data = page.extract_table()

        if extracted_data:
            print(extracted_data[1:])
            # Create a temporary DataFrame and append to the main DataFrame
            temp_df = pd.DataFrame(extracted_data[1:], columns=extracted_data[0])
            #print(temp_df.loc[1])
            #print(temp_df.columns)

def extract_tables_from_pdf(pdf_path, output_folder):
    # Attempt to extract all tables from the PDF
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    
    # Loop through the tables and save each one to a separate CSV file
    for i, table in enumerate(tables):
        output_path = f"{output_folder}/table_{i+1}.csv"
        table.to_csv(output_path, index=False)
        print(f"Table {i+1} saved as {output_path}")

# Specify the path to your PDF file and the output folder
pdf_path = "baragacounty_results.pdf"
output_folder = 'test'

# Call the function
extract_tables_from_pdf(pdf_path, output_folder)