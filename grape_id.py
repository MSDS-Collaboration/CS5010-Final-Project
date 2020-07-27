import pandas as pd
from csv import writer
from csv import reader
import re


# Removes parenthesis or brackets and their contents
def removeParens(string):
    s = re.sub(r"[\(\[].*?[\)\]]", "", string)
    return s.strip()

# Function to match grape color to wine variety (Red, White, Rose, Multiple, or Unknown)
def grapeId(description, variety):
    color = ''
    prefix = ''
    suffix = ''

    # First take color from wine variety name if applicable (e.g. Red Blend)
    if bool(re.search(r'\b' + 'red' + r'\b', variety)):
        color = 'Red'
    elif bool(re.search(r'\b' + 'white' + r'\b', variety)):
        color = 'White'
    elif bool(re.search(r'\b' + 'rosé' + r'\b', variety)):
        color = 'Rosé'

    # Next try to match wine variety to grape list from Wikipedia
    else:
        full_matches = grape_list[grape_list['Name'].str.lower() == variety] # Full name match
        partial_matches = grape_list[grape_list['Name'].str.contains(r'\b' + re.escape(variety) + r'\b', \
            case=False, na=False)] # Partial name match

        # If full matches exist, take those
        if len(full_matches):
            colors = full_matches['Type'].unique()
        # Otherwise if partial matches exist, take those
        elif len(partial_matches):
            colors = partial_matches['Type'].unique()
        # Otherwise, empty match list
        else:
            colors = []

        # If single color match
        if len(colors) == 1:
            color = colors[0]

        # If we still have no match, look in description
        if len(color) == 0:
            if bool(re.search(r'\b' + 'red' + r'\b', description, flags=re.IGNORECASE)):
                color = 'Red'
            elif bool(re.search(r'\b' + 'white' + r'\b', description, flags=re.IGNORECASE)):
                color = 'White'
            elif bool(re.search(r'\b' + 'blanc' + r'\b', description, flags=re.IGNORECASE)):
                color = 'White'
            elif bool(re.search(r'\b' + 'blanc' + r'\b', description, flags=re.IGNORECASE)):
                color = 'White'
            elif bool(re.search(r'\b' + 'rosé' + r'\b', description, flags=re.IGNORECASE)):
                color = 'Rosé'

    # Check if a sparkling wine
    if bool(re.search(r'\b' + 'sparkling' + r'\b', variety, flags=re.IGNORECASE)):
        prefix = 'Sparkling'
    elif bool(re.search(r'\b' + 'champagne' + r'\b', variety, flags=re.IGNORECASE)):
        prefix = 'Sparkling'
    elif bool(re.search(r'\b' + 'sparkling' + r'\b', description, flags=re.IGNORECASE)):
        prefix = 'Sparkling'
    elif bool(re.search(r'\b' + 'champagne' + r'\b', description, flags=re.IGNORECASE)):
        prefix = 'Sparkling'

    # This is where we make some best guesses since no match was found...
    # Almost all sparkling wines are white
    if len(color) == 0 & len(prefix):
        color = 'White'
    # Try this lookup list for white wines either not in our grape list or in both red and white but known usually white
    elif variety in ['pinot gris', 'muskat', 'muscadine', 'malvasia fina', 'malvasia', 'gros plant', 'cercial', 'cerceal']:
        color = 'White'
    # If still no match, assume Red
    elif len(color) == 0:
        color = 'Red'

    # Check if a blend
    if bool(re.search(r'\b' + 'blend' + r'\b', variety, flags=re.IGNORECASE)):
        suffix = 'Blend'
    elif bool(re.search(r'\b' + 'blend' + r'\b', description, flags=re.IGNORECASE)):
        suffix = 'Blend'

    return " ".join([prefix, color, suffix])



print('>>> Starting')

grape_list = pd.read_csv('grape_list_parsed.csv')

with open('winemag-data-130k-v2.csv', 'r') as read_obj, \
    open('winemag-data-modified.csv', 'w', newline='') as write_obj:
    # Create a csv.reader object from the input file object
    csv_reader = reader(read_obj)
    # Create a csv.writer object from the output file object
    csv_writer = writer(write_obj)
    # Read each row of the input csv file as list
    i = 0
    for row in csv_reader:
        # Append the default text in the row / list
        column = grapeId(row[2].lower(), row[12].lower()) if (i > 0) else 'type'
        row[11] = removeParens(row[11])
        row.append(column)
        # Add the updated row / list to the output file
        csv_writer.writerow(row)
        i += 1

# Count results
wine_list = pd.read_csv('winemag-data-modified.csv')
print(wine_list.groupby('type').count())

print('>>> Finished')
