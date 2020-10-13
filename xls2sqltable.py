#!/usr/bin/env python
# -*- coding: utf-8 -*-
# release 12-09-2016
import sys
import os
from optparse import OptionParser
from uaxls.xlsreader import XlsReader


def do_main(file_xls, file_sql):
    table = file_sql.partition('.')[0]
    xr = XlsReader()
    xr.open(file_xls)
    cols = xr.cols
    typs = xr.types
    sizes = xr.sizes
    le = len(cols)
    fsql = open(file_sql, "w+")
    fsql.write("create table %s (" % (table))
    for i in range(0, le):
        t = typs[i]
        # col = cols[i].lower().replace(' ', '_').replace('.', ' ')
        col = cols[i]
        if t == 2:
            s = "%s decimal(15,2) " % (col)
        else:
            s = "%s char(%s) " % (col, sizes[i])
        # s = s.encode("utf-8")
        if i > 0:
            fsql.write(',')
        fsql.write(os.linesep)
        fsql.write(s)
    fsql.write(os.linesep)
    fsql.write(");")
    fsql.write(os.linesep)
    fsql.close()
    os.chmod(file_sql, 0o666)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-x", "--xls")
    parser.add_option("-s", "--sql")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.sql is None or opts.xls is None:
        print ("-x <file.xls> -s <file.sql> ")
        sys.exit(0)
    do_main(opts.xls, opts.sql)
