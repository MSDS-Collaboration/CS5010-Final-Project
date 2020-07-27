

from csv import writer
from csv import reader
import re

print('>>> Starting')

with open('grape_list.csv', 'r') as read_obj, \
    open('grape_list_parsed.csv', 'w', newline='') as write_obj:
    # Create a csv.reader object from the input file object
    csv_reader = reader(read_obj, delimiter=';')
    # Create a csv.writer object from the output file object
    csv_writer = writer(write_obj)
    # Read each row of the input csv file as list
    next(csv_reader) # Skip first line

    csv_writer.writerow(['Name', 'Type'])
    for row in csv_reader:
        color = row[2]
        # Append the default text in the row / list
        for phrase in re.split(r",|\/", row[0], flags=re.IGNORECASE):
            if len(phrase):
                phrase = re.sub(r"[\(\[].*?[\)\]]", "", phrase).strip()
                csv_writer.writerow([phrase, color])

        for phrase in re.split(r",|\/", row[1], flags=re.IGNORECASE):
            if len(phrase):
                phrase = re.sub(r"[\(\[].*?[\)\]]", "", phrase).strip()
                csv_writer.writerow([phrase, color])


print('>>> Finished')
