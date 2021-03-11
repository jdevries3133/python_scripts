"""
The simplest example for sending a letter through the ClickSend API
"""

import json
from pathlib import Path
from base64 import b64encode

import requests
from requests.auth import HTTPBasicAuth
from docx import Document

with open(Path(Path(__file__).parent, 'secrets.json'), 'r') as jsonf:
    data = json.load(jsonf)


def main():

    # establish constants
    name = data['name']
    addr = [
        data['addr1'],
        data['addr2'],
        data['addr3'],
    ]
    endpoints = {
        'upload': 'https://rest.clicksend.com/v3/uploads',
        'send': 'https://res.clicksend.com/v3/post/letters/send',
    }

    # make doc to send
    doc = Document()
    doc.add_paragraph('Hello world!')
    doc.save(Path(Path(__file__).parent, 'temp.docx'))

    # open doc and read it into byte buffer
    with open(Path(Path(__file__).parent, 'temp.docx'), 'rb') as docxf:
        doc_raw = docxf.read()


###############################################################################

            ## Where the magic doesn't happen...  ##

    # upload to clicksend API
    payload = b'{"content":"' + b64encode(doc_raw) + b'"}'
    res = requests.post(
        endpoints['upload'],
        params={'convert': 'post'},
        auth=HTTPBasicAuth('jdevries3133@gmail.com', data['API_KEY']),
        headers={
            'Content-type': 'application/json'
        },
        data=payload
    )

###############################################################################




if __name__ == '__main__':
    main()
