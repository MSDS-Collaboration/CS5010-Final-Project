from csv import writer
from csv import reader
import re

# Function to split a comma or forward slash separated string to a list
def splitNames(namesStr):
    nameLst = re.split(r",|\/", namesStr, flags=re.IGNORECASE)
    nameLst = [name.strip() for name in nameLst]
    return nameLst

# Function to remove parenthesis or brackets and their contents
def removeComments(name):
    return re.sub(r"[\(\[].*?[\)\]]", "", name).strip()

def parseGrapeList():
    print('>>> Starting')
    with open('grape_list.csv', 'r') as read_obj, \
        open('grape_list_parsed.csv', 'w', newline='') as write_obj:

        # Create a csv.reader object from the input file object
        csv_reader = reader(read_obj, delimiter=';')
        # Create a csv.writer object from the output file object
        csv_writer = writer(write_obj)

        # Skip first header row
        next(csv_reader)

        # Write output file headers
        csv_writer.writerow(['Name', 'Type'])

        # Read each row of the input file as list
        for row in csv_reader:
            color = row[2]
            for phrase in splitNames(row[0]):
                if len(phrase):
                    phrase = removeComments(phrase)
                    csv_writer.writerow([phrase.lower(), color])

            for phrase in splitNames(row[1]):
                if len(phrase):
                    phrase = removeComments(phrase)
                    csv_writer.writerow([phrase.lower(), color])

    print('>>> Finished')

# Uncomment this and run to parse the grape_list.csv file
parseGrapeList()
