#!/usr/bin/env python3.8
'''
Written by: Saksham Consul 04/05/2023
Script to extract data from pdf
'''
import os
import tqdm
import pandas as pd
from PyPDF2 import PdfReader, PdfFileWriter


def convert_pdf_text(dir_name):
    try:
        os.mkdir('papers_parse')
    except:
        pass
    dir_list = os.listdir(dir_name)
    paper_list = tqdm.tqdm(dir_list, desc='Extracting text from PDFs')
    for file in paper_list:
        # Skip files that have already been parsed
        if file[:-3]+'txt' in os.listdir('papers_parse'):
            continue
        file_path = os.path.join('papers', file)
        get_pdf_text(file_path)


def get_pdf_text(file_path):
    '''Extracts the text from the PDF file and saves it to a text file'''

    # write to a new file
    try:
        pdf = PdfReader(file_path)
    except Exception as e:
        print(file_path, '\n', e)
        return
    file = file_path.split('/')[-1]

    with open('papers_parse/'+file[:-3]+'txt', 'w') as f:
        for page_num in range(len(pdf.pages)):
            pageObj = pdf.pages[page_num]
            try:
                txt = pageObj.extract_text()
            except Exception as e:
                print(e)
                pass
            else:
                try:
                    txt = txt.encode('UTF-8', 'ignore').decode('UTF-8')
                except Exception as e:
                    print(e)
                    pass
                else:
                    f.write(txt)
            f.write('\n')
        f.close()
    # print(dir_list)


def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie


def saving_csv(dir_name):
    try:
        os.mkdir('processed')
    except:
        pass
    # Create a list to store the text files
    texts = []

    # Get all the text files in the text directory
    dir_list = os.listdir(dir_name)
    paper_list = tqdm.tqdm(dir_list, desc='Saving as csv')
    for file in paper_list:
        # Open the file and read the text
        with open(dir_name+'/'+file, "r", encoding="UTF-8") as f:
            try:
                text = f.read()

                # Replace -, _, and #update with spaces.
                texts.append(
                    (file.replace('-', ' ').replace('_', ' ').replace('#update', ''), text))
            except:
                pass
    # Create a dataframe from the list of texts
    df = pd.DataFrame(texts, columns=['fname', 'text'])

    # Set the text column to be the raw text with the newlines removed
    df['text'] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv('processed/scraped.csv')
    print(df.head())


def main():
    convert_pdf_text('papers')
    saving_csv('papers_parse')


# def reset_eof_of_pdf_return_stream(pdf_stream_in: list):
#     # find the line position of the EOF
#     for i, x in enumerate(pdf_stream_in[::-1]):
#         if b'%%EOF' in x:
#             actual_line = len(pdf_stream_in)-i
#             print(
#                 f'EOF found at line position {-i} = actual {actual_line}, with value {x}')
#             break

#     # return the list up to that point
#     return pdf_stream_in[:actual_line]


# def correct_pdf(dir_name):
#     '''Corrects the EOF of the PDF file and saves it to a pdf file'''
#     try:
#         os.mkdir('papers_fixed')
#     except:
#         pass
#     dir_list = os.listdir(dir_name)
#     paper_list = tqdm.tqdm(dir_list, desc='Correcting EOF of PDFs')
#     for file in paper_list:
#         # Skip files that have already been corrected
#         if file[:-3]+'txt' in os.listdir('papers_fixed'):
#             continue
#         # opens the file for reading
#         with open(dir_name + '/'+file, 'rb') as p:
#             txt = (p.readlines())

#         # get the new list terminating correctly
#         txtx = reset_eof_of_pdf_return_stream(txt)
#         print(type(txtx))

#         file = file.split('/')[-1]
#         with open('papers_fixed/'+file[:-3]+'txt', 'w') as f:
#             for txt in txtx:
#                 print(txt)
#                 txt = txt.encode('ascii', 'ignore').decode('ascii')
#                 f.write(txt)

if __name__ == "__main__":
    main()
