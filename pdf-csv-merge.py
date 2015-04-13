#!/usr/bin/python

# __author__ = 'propbono'

import os, sys, csv
import re


special_chars = {';', ':', '/','|','}','{','<','>','!','@','#','$','%'}

#TODO:// rewrite programm
# First check what pdf files we have in the folder
DIR = os.path.dirname(sys.argv[0])
PREPPED_PDF_PATH = DIR + '/prepped_pdf/'
PRESS_READY_PDF_PATH =DIR + 'press_ready_pdf/'
SOURCE_CSV_PATH = DIR +'/csv/'
MERGED_CSV = DIR + "/merged_csv/"


# Next search for csv
# Next merge csv
# Makes changes to csv

def _read_csv_values_for(pdf_name):
    #extract number from pdf name
    csv_name = _return_csv_name_for(pdf_name)

    with open(csv_name) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',', quoting=csv.QUOTE_ALL)
        for row in reader:
            return row

# Check what will happen if there will be no csv file for a pdf
def _return_csv_name_for(pdf_name):
    for file in os.listdir(SOURCE_CSV_PATH):
        name = os.path.split(pdf_name)[1]
        if file[:6] == name[:6] and file.endswith('csv'):
            return file

# add regular expressions it will be easier to delete characters
def _delete_special_chars(special_chars, row):
    for char in special_chars:
        row['CONTENT'] = row['CONTENT'].replace(char,'')
        row['NAME'] = row['NAME'].replace(char,'')
    return row

# Add rules to exctract notes
def _extract_notes_from_pdf_name(pdf_name, row):
    find_prepp = _find_prepp_notes(pdf_name)[0].split('-')
    # SampleName(3.5-2-16pt1000-SAMEDAY-DIECUT,PocketFolder 4 inch)-1000.pdf
    row['WIDTH'] = find_prepp[0]            # 3.5
    row['HEIGHT'] = find_prepp[1]           # 2
    row['PRODUCT GROUP'] = find_prepp[3]    # SAMEDAY
    row['NOTES']= find_prepp[4]             # DIECUT, PocketFolder 4 inch
    row['STOCK NAME'] = find_prepp[2]            # 16pt1000
    #row['Quantity'] =
    row['CONTENT'] = _delete_prepp_notes_from(pdf_name) # SampleName-1000.pdf

    return _delete_special_chars(special_chars,row), find_prepp[2]

# Add regular expressions to remove characters
def _find_prepp_notes(pdf):
    text_to_replace = re.findall(r'\(.*\)', pdf)
    return text_to_replace


def _delete_prepp_notes_from(pdf):
    text_to_replace = _find_prepp_notes(pdf)
    newpdf = pdf.replace(text_to_replace, '')
    return newpdf


def move_pdf_to_press_ready_pdf(list_of_pdf):
    for pdf in list_of_pdf:
        newpdf = _delete_prepp_notes_from(pdf)
        os.rename(PREPPED_PDF_PATH+pdf,PRESS_READY_PDF_PATH+newpdf)



def WriteJoinedCsv(pdf_list, output_name):
    with open(MERGED_CSV+output_name, 'w', newline='') as csv_file:
        fieldnames = ['QUANTITY','WIDTH','HEIGHT''CONTENT','PRODUCT GROUP',
                      'NOTES', 'STOCK NAME', 'COMPANY','FIRST NAME','FAMILY NAME',
                      'DESCRIPTION','DUE DATE','GRAIN','TOP OFFCUT','LEFT OFFCUT',
                      'BOTTOM OFFCUT','RIGHT OFFCUT','PRIORITY','SIDE 1 COLORS',
                      'SIDE 2 COLORS','NAME','KINDS']
        writer = csv.DictWriter(csv_file,fieldnames=fieldnames)
        writer.writeheader()
        for pdf_name in pdf_list:
            row = _read_csv_values_for(pdf_name)
            corrected_row, stock = _extract_notes_from_pdf_name(pdf_name, row)
            writer.writerow(corrected_row)
        move_pdf_to_press_ready_pdf(pdf_list)



if __name__ == "__main__":
    output_name="output.csv"
    pdf_list = os.listdir(PREPPED_PDF_PATH)
    WriteJoinedCsv(pdf_list, output_name)