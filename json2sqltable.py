#!/usr/bin/env python
# -*- coding: utf-8 -*-
# release 12-09-2016
import sys
import os
from optparse import OptionParser
import json


def get_type(x):
    t = ""
    if type(x) is int:
        t = "integer"
    elif type(x) is float:
        t = "decimal(10, 2)"
    else:
        t = "char(50)"
    return t


def do_main(file_json, file_sql):
    table = file_sql.partition('.')[0]
    with open(file_json, "r+") as f:
        txt = f.read()
    js = json.loads(txt)
    rows = js['rows']
    row0 = rows[0]
    cols = [c for c in row0.keys()]
    typs = [get_type(row0[c]) for c in cols]
    le = len(cols)
    fsql = open(file_sql, "w+")
    fsql.write("create table %s (" % (table))
    for i in range(0, le):
        t = typs[i]
        col = cols[i]
        s = "%s %s" % (col, t)
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
    parser.add_option("-j", "--json")
    parser.add_option("-s", "--sql")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.sql is None or opts.json is None:
        print ("-j <file.json> --json=<file.json>  -s <file.sql> --sql=<file.sql>  ")
        sys.exit(0)
    do_main(opts.json, opts.sql)
