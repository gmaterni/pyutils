#!/usr/bin/env python
# -*- coding: utf-8 -*-
# csv2db release  28-02-2019
import sys
# import os
from optparse import OptionParser
from uadb import UaDb
# import csv
import re
# from pdb import set_trace


def do_main(ini, csv_path, delimiter, table):
    uadb = UaDb.from_file(ini)
    f = open(csv_path, 'r')
    for line in f:
        fs = str(line).split(delimiter)
        cols = []
        for col in fs:
            # set_trace()
            v = re.sub(r'[^\x00-\x7F]', '', col)
            s = v.lower().strip().replace(' ', '_').replace('.', '').replace('"', '').replace("'", "").replace("\\n", "")
            s = s.strip()
            if s == "":
                continue
            cols.append(s)
        break

    le = len(cols)
    rjs = {}
    i = 0
    for line in f:
        if i % 100 == 0:
            print(i)
        i += 1
        row = str(line).split(delimiter)
        try:
            for c in range(le):
                val = re.sub(r'[^\x00-\x7F]', ' ', row[c])
                col = cols[c].strip()
                col = "col%s" % c if col == '' else col
                rjs[col] = val.replace("\"", "").replace('\n', '').replace("'", "")
        except Exception as e:
            print("ERROR %s %s" % (i, e))
            print(line)
            continue
        uadb.insert_row(table, rjs)
    print(i)


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
    delimiter = '|' if opts.sep is None else opts.sep
    do_main(opts.ini, opts.csv, delimiter, opts.table)
