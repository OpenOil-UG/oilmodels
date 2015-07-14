'''
Wrapper for PDFTables
'''

APIKEY = '5z5um8568wpx'

import csv
import json
import os
import requests
import tempfile
import openpyxl
import pdfsplit


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [str(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')
        

def dl_pdf(pdfurl):
    tf = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
    tf.write(requests.get(pdfurl).content)
    tf.flush()
    return tf

def page_from_pdf(pdffn, pagenumber):
    partial_tf = tempfile.NamedTemporaryFile(mode='w+b', delete=False)
    pdfsplit.splitPages(pdffn,
                        [slice(pagenumber+1, pagenumber+2)], # 0-index vs 1-index
                        outputPat=partial_tf.name,                        
    )
    return partial_tf.name

def tables_from_page(pagefn):
    files = {'f': ('upload.pdf', open(pagefn, 'rb'))}
    response = requests.post("https://pdftables.com/api?key=5z5um8568wpx&format=csv", files=files)
    response.raise_for_status() # ensure we notice bad responses
    return response.text


def page_to_csv(pdfurl, pagenumber):
    '''
    Split out one page from a (potentially multipage) pdf file
    send it to pdftables, get back the table
    pagenumber is given **counting from 1** (not zero)
    '''
    fullfile = dl_pdf(pdfurl)
    fn_page = page_from_pdf(fullfile.name, pagenumber)
    result = tables_from_page(fn_page)
    os.unlink(fullfile.name)
    return result

def csv_to_json(csvtext):
    # XXX this unicode hack is mangling some text
    reader = unicode_csv_reader(csvtext.split('\n'))
    reader = csv.reader(csvtext.split('\n'))
    return json.dumps(
        {'data': list(reader)})


def interpret_range(rstr):
    '''
    turn a range specification string into a list of pages
    '''
    pages = []
    for spec in rstr.split(','):
        spec = spec.strip()
        if spec.isdigit():
            pages.append(int(spec))
        elif '-' in spec:
            l,r = [x.strip() for x in spec.split('-', 1)]
            if not (l.isdigit and r.isdigit()):
                raise ValueError
            for pn in range(int(l), int(r)+1):
                pages.append(pn)
    return pages
            

def test_pdftables():
    url = 'http://www.nnpcgroup.com/Portals/0/Monthly%20Performance/2002%20Annual%20Statistical%20Bulletin%20ASB.pdf'
    page = 24
    return page_to_csv(url, page)


