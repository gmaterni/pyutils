#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser
import os
from uadb import UaDb
import json
# import pdb


def do_main(ini, file_json, sql):
    uadb = UaDb.from_file(ini)
    rt = uadb.fetchall(sql, [])
    rs = rt.rows
    # print(rs)
    # js = {"rows": rs}
    s = json.dumps(rs, indent=4)
    with open(file_json, "w+")as f:
        f.write(s)
    os.chmod(file_json, 0o666)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ini")
    parser.add_option("-j", "--json")
    parser.add_option("-t", "--table")
    parser.add_option("-s", "--sql")
    parser.add_option("-f", "--filesql")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.json is None or opts.ini is None:
        print ("-i <db.ini>  -j <file.json> [ -t <table> | -s <\"sql\"> | -f < file.sql>] ")
        sys.exit(0)
    if opts.sql is not None:
        sql = opts.sql
    elif opts.table is not None:
        sql = "select * from %s " % (opts.table)
        print(sql)
    elif opts.filesql is not None:
        with open(opts.filesql, "r+") as f:
            sql = f.read()
        print(sql)
    else:
        exit(0)
    do_main(opts.ini, opts.json, sql)
