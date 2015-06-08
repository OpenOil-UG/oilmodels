'''
Wrapper for PDFTables
'''

APIKEY = '5z5um8568wpx'

import os
import requests
import tempfile
import openpyxl
import pdfsplit

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
    return response


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


def test_pdftables():
    url = 'http://www.nnpcgroup.com/Portals/0/Monthly%20Performance/2002%20Annual%20Statistical%20Bulletin%20ASB.pdf'
    page = 24
    return page_to_csv(url, page)
