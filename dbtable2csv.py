#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser
import os
from uadb import UaDb


def do_main(ini, file_csv, sep, table):
    uadb = UaDb.from_file(ini)
    sql = " select * from %s  " % (table)
    rt = uadb.fetchall(sql, [])
    csv = rt.csv(header=1, sep=sep)
    with open(file_csv, "w+")as f:
        f.write(csv)
    os.chmod(file_csv, 0o666)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ini")
    parser.add_option("-c", "--csv")
    parser.add_option("-s", "--sep")
    parser.add_option("-t", "--table")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.csv is None or opts.ini is None or opts.table is None:
        print ("-i <db.ini> -c <file.csv> -s <separator> -t <table> ")
        sys.exit(0)
    sep = '|' if opts.sep is None else opts.sep
    do_main(opts.ini, opts.csv, sep, opts.table)
