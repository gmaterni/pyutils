#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser
import os
from uadb import UaDb


def do_main(ini, file_csv, sep, sql):
    uadb = UaDb.from_file(ini)
    rt = uadb.fetchall(sql, [])
    csv = rt.csv(header=1, sep=sep)
    with open(file_csv, "w+")as f:
        f.write(csv)
    os.chmod(file_csv, 0o666)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ini")
    parser.add_option("-c", "--csv")
    parser.add_option("-p", "--sep")
    parser.add_option("-s", "--sql")
    parser.add_option("-f", "--filesql")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.csv is None or opts.ini is None:
        print ("-i <db.ini> -c <file.csv> -p <separator> -s <\"sql\">  -f < file.sql> ")
        sys.exit(0)
    sep = '|' if opts.sep is None else opts.sep
    sql = opts.sql
    if opts.filesql is not None:
        with open(opts.filesql, "r+") as f:
            sql = f.read()
    do_main(opts.ini, opts.csv, sep, sql)
