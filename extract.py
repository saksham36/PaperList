#!/usr/bin/env python3
'''
Written by: Saksham Consul 04/05/2023
Script to extract data from pdf
'''
import os
import re
import tqdm
from PyPDF2 import PdfReader, PdfFileWriter


def get_pdf_text(file_path):
    '''Extracts the text from the PDF file and saves it to a text file'''
    pdf = PdfReader(file_path)
    file = file_path.split('/')[-1]
    with open('papers_parse/'+file[:-3]+'.txt', 'w') as f:
        for page_num in range(len(pdf.pages)):
            pageObj = pdf.pages[page_num]
            try:
                txt = pageObj.extract_text()
            except Exception as e:
                print(e)
                pass
            else:
                f.write(txt)
            f.write('\n')
        f.close()
    # print(dir_list)


def main():
    dir_list = os.listdir('papers')
    paper_list = tqdm.tqdm(dir_list)
    for file in paper_list:
        file_path = os.path.join('papers', file)
        get_pdf_text(file_path)


if __name__ == "__main__":
    main()
