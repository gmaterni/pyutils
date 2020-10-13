#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser
import os
from uadb import UaDb
import xlwt
import re
from decimal import *
# import pdb


def do_main(ini, xls_path, sql):
    stylenum = xlwt.XFStyle()
    stylenum.num_format_str = '#0.00'
    # rgx = re.compile(r'^\-?\d+\.\d*$')
    rgx = re.compile(r'^\-?\d+\.?\d*$')
    uadb = UaDb.from_file(ini)
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
                ws.write(r + 1, c, value)
            else:
                s = Decimal(value)
                ws.write(r + 1, c, s, stylenum)
    wb.save(xls_path)
    os.chmod(xls_path, 0o666)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ini")
    parser.add_option("-x", "--xls")
    parser.add_option("-s", "--sql")
    parser.add_option("-f", "--filesql")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.xls is None or opts.ini is None:
        print ("-i <db.ini> --ini=<db.ini> -x <file.xls> --xls=<file.xls> -s <\"sql\"> --sql=<\"sql\"> -f <file.sql> --filesql=<file.sql>")
        sys.exit(0)
    sql = opts.sql
    if opts.filesql is not None:
        with open(opts.filesql, "r+") as f:
            sql = f.read()
    do_main(opts.ini, opts.xls, sql)
