#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# json2db release 25-07-2019

import sys
import argparse
from uadb import UaDb
import json


def do_main(ini, file_json, table):
    uadb = UaDb.from_file(ini)
    with open(file_json, "r+") as f:
        txt = f.read()
    js = json.loads(txt)
    rows = js["rows"]
    for i in range(len(rows)):
        print(i)
        row = rows[i]
        uadb.insert_row(table, row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    parser.add_argument("-i",
                        dest="ini",
                        required=True,
                        metavar="",
                        help="-i <db.ini>")
    parser.add_argument("-j",
                        dest="json",
                        required=True,
                        metavar="",
                        help="-j <file.json>")
    parser.add_argument("-t",
                        dest="table",
                        required=True,
                        metavar="",
                        help="-t <table>")
    args = parser.parse_args()
    do_main(args.ini, args.json, args.table)
