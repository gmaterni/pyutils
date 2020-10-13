#!/usr/bin/env python3
# coding: utf-8
from uadb import UaDb, DB
from optparse import OptionParser
import json
import sys
import os
# from pdb import set_trace


def type_descr(uadb, t, w):
    tp = ""
    if t == uadb.db_types[DB.DATE]:
        tp = 'date'
    elif t == uadb.db_types[DB.TIMESTAMP]:
        tp = 'rimestamp'
    elif t == uadb.db_types[DB.DECIMAL]:
        tp = 'decimal(11,2'
    elif t == uadb.db_types[DB.LONG]:
        tp = 'long'
    elif t == uadb.db_types[DB.INT]:
        tp = 'int'
    elif t == uadb.db_types[DB.BOOL]:
        tp = 'boolean'
    elif t == uadb.db_types[DB.STRING]:
        tp = "char(%s)" % (w)
    return tp


def schema_json(uadb, rt):
    le = len(rt.cols)
    sch = {}
    row = {}
    for i in range(0, le):
        item = {}
        c = rt.cols[i]
        t = rt.types[i]
        w = rt._sizes[i]
        tp = type_descr(uadb, t, w)
        item['size'] = w
        item['type'] = tp
        item['label'] = c
        row[c] = item
    sch['row0'] = row
    return json.dumps(sch, indent=2)


def do_main(ini, table, file_json):
    uadb = UaDb.from_file(ini)
    sql = " select * from %s  where 1=2 " % (table)
    rt = uadb.fetchall(sql, [])
    js = schema_json(uadb, rt)
    with open(file_json, "w+")as f:
        f.write(js)
    os.chmod(file_json, 0o666)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ini")
    parser.add_option("-t", "--table")
    parser.add_option("-j", "--json")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.json is None or opts.ini is None or opts.table is None:
        print ("-i <db.ini> -t <table> -j <file.json> ")
        sys.exit(0)
    do_main(opts.ini, opts.table, opts.json)
