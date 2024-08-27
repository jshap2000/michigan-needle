import pandas as pd
import re

COLUMN_TO_DROP = 1
OVERSIZED = 9

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

# Usage
file_path = 'results.txt'
start_word = 'SLOTKIN'
end_word = 'Representative'
delete_around_words(file_path, start_word, end_word)

# Read the file into a list of lines
with open('results.txt', 'r') as file:
    lines = file.readlines()

data = []

for line in lines:
    # Split the line on sequences of spaces (at least two spaces as a safe assumption)
    columns = re.split(r'\s{3,}', line.strip())

    if len(columns) == OVERSIZED:
        columns = columns[0:COLUMN_TO_DROP] + columns[COLUMN_TO_DROP+1:]

    if len(columns) > 5:
        data.append(columns)

for data1 in data:
    print(len(data1))
# Create DataFrame
# Note: You may need to adjust column names and handle them if they are not properly formatted
df = pd.DataFrame(data[1:], columns=data[0])
print(df)