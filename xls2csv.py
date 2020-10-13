#!/usr/bin/env python
# -*- coding: utf-8 -*-
# xls2csv release 28-02-2010

import sys
import os
from optparse import OptionParser
from uaxls.xlsreader import XlsReader
import re
import pdb

def do_main(file_xls, file_csv, sep):
    # pdb.set_trace()
    xr = XlsReader()
    xr.open(file_xls)
    csv = xr.list_csv(True, sep)
    fcsv = open(file_csv, "a+")
    for r in csv:
        # s = str(r, 'utf-8')
        r = re.sub(r'[^\x00-\x7F]', ' ', r)
        fcsv.write(r)
        fcsv.write(os.linesep)
    fcsv.close()
    os.chmod(file_csv, 0o666)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-x", "--xls")
    parser.add_option("-c", "--csv")
    parser.add_option("-s", "--sep")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.csv is None or opts.xls is None:
        print ("-x <file.xls> -c <file.csv> -s <separator>")
        sys.exit(0)
    sep = '|' if opts.sep is None else opts.sep
    do_main(opts.xls, opts.csv, sep)
