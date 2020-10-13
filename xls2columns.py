#!/usr/bin/env python
# -*- coding: utf-8 -*-
# release 25-01-2019
import sys
import os
from optparse import OptionParser
from uaxls.xlsreader import XlsReader
from pdb import set_trace


def do_main(file_xls, file_txt):
    xr = XlsReader()
    xr.open(file_xls)
    cols = xr.cols
    le = len(cols)
    fsql = open(file_txt, "w+")
    for i in range(0, le):
        # col = cols[i].encode("utf-8")
        col = cols[i]
        # set_trace()
        # s = "%s " % (col)
        s = str(col)
        # s = s.encode("utf-8")
        fsql.write(s)
        fsql.write(os.linesep)
    fsql.close()
    os.chmod(file_txt, 0o666)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-x", "--xls")
    parser.add_option("-t", "--txt")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.txt is None or opts.xls is None:
        print ("-x <file.xls> -t <file.txt> ")
        sys.exit(0)
    do_main(opts.xls, opts.txt)
