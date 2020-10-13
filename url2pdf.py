#!/usr/bin/env python3

import pdfkit
import sys
import os

options_help = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'custom-header': [
        ('Accept-Encoding', 'gzip')
    ],
    'cookie': [
        ('cookie-name1', 'cookie-value1'),
        ('cookie-name2', 'cookie-value2'),
    ],
    'no-outline': None
}

options1 = {
    'margin-top': '0',
    'margin-right': '0',
    'margin-bottom': '0',
    'margin-left': '0',
    'encoding': 'UTF-8',
    'javascript-delay': '9000',
    'no-stop-slow-scripts': '',
}
options0 = {
    'quiet': '',
    'encoding': 'UTF-8',
    'no-stop-slow-scripts': '',
}

options = {
    'encoding': 'UTF-8',
    'no-stop-slow-scripts': ''
}


def url2pdf(url, pdf_name):
    print(pdf_name)
    pdfkit.from_url(url, pdf_name, options=options)
    os.chmod(pdf_name, 0o666)


if __name__ == '__main__':
    url = sys.argv[1]
    if(len(sys.argv) < 2):
        print("url2pdf.py <url> <file.pdf>")
        sys.exit(0)
    if(len(sys.argv) == 2):
        pdf = "file.pdf"
    else:
        pdf = str(sys.argv[2])
    url2pdf(url, pdf)
