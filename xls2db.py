#!/usr/bin/env python
# -*- coding: utf-8 -*-
# xls2db release 28-02-2019

import sys
from optparse import OptionParser
from uadb import UaDb
from uaxls.xlsreader import XlsReader
import re


def do_main(ini, file_xls, table):
    uadb = UaDb.from_file(ini)
    xr = XlsReader()
    xr.open(file_xls)
    rows = xr.list_dict()
    print("num.rows:%s" % (len(rows)))
    for i in range(len(rows)):
        if i % 1000 == 0:
            print(i)
        row = rows[i]
        r = {}
        # for k, v in row.iteritems(): python2
        for k, v in row.items():
            s = str(v, 'utf-8')
            x = re.sub(r'[^\x00-\x7F]', ' ', s)
            r[k] = x
        uadb.insert_row(table, r)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ini")
    parser.add_option("-x", "--xls")
    parser.add_option("-t", "--table")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.xls is None or opts.ini is None or opts.table is None:
        print ("-i <db.ini> -x <file.xls> -t <table> ")
        sys.exit(0)
    do_main(opts.ini, opts.xls, opts.table)
