#!/usr/bin/env python
# -*- coding: utf-8 -*-
# release 12-09-2016
import sys
from optparse import OptionParser
from uaxls.xlsreader import XlsReader


def do_main(file_xls):
    xr = XlsReader()
    xr.open(file_xls)
    rows = xr.list_dict()
    for i in range(len(rows)):
        row = rows[i]
        print(row)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-x", "--xls")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.xls is None:
        print ("-x <file.xls> - ")
        sys.exit(0)
    do_main(opts.xls)
