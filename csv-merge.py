#!/usr/bin/python

# __author__ = 'propbono'

import os, sys, csv

special_chars = {';', ':', '/','|','}','{','<','>','!','@','#','$','%'}

def read_csv_values(csv_name):
    with open(csv_name) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in reader:
            row['CONTENT'] = _update_pdf_name(csv_name)
            return row

def _update_pdf_name(name):
    for file in os.listdir(os.path.dirname(sys.argv[0]) +'/pdf/'):
        name = os.path.split(name)[1]
        if file[:6] == name[:6] and file.endswith('pdf'):
            return file
    return ""

def _delete_special_chars(special_chars, row):
    for char in special_chars:
        row['CONTENT'] = row['CONTENT'].replace(char,'')
        row['NAME'] = row['NAME'].replace(char,'')
    return row

def WriteJoinedCsv(path, output_name):
    with open(output_name, 'w', newline='') as csv_file:
        fieldnames = ['NAME','KINDS','QUANTITY','WIDTH','HEIGHT','SIDE 1 COLORS','SIDE 2 COLORS','CONTENT','PRODUCT GROUP','COMPANY','FIRST NAME','FAMILY NAME','DESCRIPTION','NOTES','DUE DATE','GRAIN','TOP OFFCUT','LEFT OFFCUT','BOTTOM OFFCUT','RIGHT OFFCUT','PRIORITY']
        writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        writer.writeheader()
        for file in os.listdir(path): # <- pdf path
            row = read_csv_values(path + file) # <- here we only need to
            # pass proper pdf name
            writer.writerow(_delete_special_chars(special_chars,row))

# ReadCsvValues(csv_name)
if __name__ == "__main__":
    output_name="output.csv"
    path = os.path.dirname(sys.argv[0]) +'/csv/'
    WriteJoinedCsv(path, output_name)