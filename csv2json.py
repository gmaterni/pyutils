#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import argparse
import json
import os
# import stat
import csv


def list_json(csv_path, delimiter='|', doublequote=False):
    csv_file = open(csv_path, 'r+')
    csv_reader = csv.reader(csv_file, delimiter=delimiter, doublequote=doublequote)
    rows = []
    for row in csv_reader:
        rows.append(row)
    #
    cols = rows[0]
    lc = len(cols)
    lr = len(rows)
    rows_json = []
    for n in range(1, lr):
        rj = {}
        for c in range(0, lc):
            col = cols[c]
            val = rows[n][c]
            rj[col] = val
        rows_json.append(rj)
    return rows_json


def do_main(csv_path, delimiter, doublequote, json_path):
    rows_json = list_json(csv_path, delimiter, doublequote)
    # import pdb;pdb.set_trace()
    # print(rows_json)
    js = {"rows": rows_json}
    s = json.dumps(js, indent=4)
    with open(json_path, "w+") as f:
        f.write(s)
    os.chmod(json_path, 0o666)
    # os.chmod(json_path, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    parser.add_argument("-c",
                        dest="csv",
                        required=True,
                        metavar="",
                        help="-i <db.ini>")
    parser.add_argument("-j",
                        dest="json",
                        required=True,
                        metavar="",
                        help="-j <file.json>")
    parser.add_argument("-s",
                        dest="sep",
                        required=False,
                        metavar="",
                        default="|",
                        help="-s <separator> default=|")
    args = parser.parse_args()
    do_main(args.csv, args.sep, False, args.json)
