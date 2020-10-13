#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser
import os
from uadb import UaDb
import xlwt
import re
from decimal import *
import decimal
# import pdb


def do_main(ini, file_xls, table):
    stylenum = xlwt.XFStyle()
    stylenum.num_format_str = '#0.00'
    # rgx = re.compile(r'^\-?\d+\.\d*$')
    rgx = re.compile(r'^\-?\d+\.?\d*$')
    uadb = UaDb.from_file(ini)
    sql = " select * from %s " % (table)
    rt = uadb.fetchall(sql, [])
    cols = rt.cols
    rows = rt.rowset
    wb = xlwt.Workbook()
    ws = wb.add_sheet("foglio1")

    for c, col in enumerate(cols):
        ws.write(0, c, col)

    for r, row in enumerate(rows):
        for c, col in enumerate(cols):
            value = row[c]
            if value is None:
                ws.write(r + 1, c, value)
                continue
            s = str(value)
            if rgx.match(s) is None:
                value = re.sub(r'[^\x00-\x7F]', ' ', value)
                ws.write(r + 1, c, value)
            else:
                try:
                    s = Decimal(value)
                    # print("c:%s col:%s val:%s" % (c,col,s))
                except decimal.InvalidOperation:
                    print("numeric ERROR! row:%s  col:%s value:%s " % (r, col, value))
                ws.write(r + 1, c, value, stylenum)

    wb.save(file_xls)
    os.chmod(file_xls, 0o666)


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
