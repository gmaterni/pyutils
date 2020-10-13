#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from optparse import OptionParser
import csv
import stat


class Csv2Txt(object):

    def __init__(self):
        self.fields = None
        self.rows = None
        self.cols = None
    """
raggrupp|12|13|N
causale|14|28|A
data|29|36|D
tipopn|37|37|A
    """

    def read_conf(self, file_conf):
        fconf = open(file_conf, "r")
        rows = fconf.readlines()
        fconf.close()
        self.fields = []
        self.cols = []
        for row in rows:
            fs = row.split('|')
            if len(fs) < 4:
                continue
            field = {}
            col = fs[0].strip()
            self.cols.append(col)
            field['col'] = col
            field['start'] = int(fs[1].strip()) - 1
            field['end'] = int(fs[2].strip())
            field['typ'] = fs[3].strip()
            self.fields.append(field)
            # pprint.pprint(field)

    def read_csv(self, csv_path, delimiter='|', doublequote=False):
        csv_file = open(csv_path, 'rb')
        csv_reader = csv.reader(csv_file, delimiter=delimiter, doublequote=doublequote)
        rows = []
        for row in csv_reader:
            rows.append(row)
        return rows

    def write_txt(self, file_conf, csv_path, sep, txt_path):
        self.read_conf(file_conf)
        ftxt = open(txt_path, "w+")
        rows = self.read_csv(csv_path, sep, False)
        lr = len(rows)
        for n in range(1, lr):
            row = rows[n]
            line = []
            for i, f in enumerate(self.fields):
                v = row[i]
                # print("v:%s  t:%s  ft:%s" % (v, type(v), f['typ']))
                sz = f['end'] - f['start']
                fs = "{:<%s}" % (sz)
                s = fs.format(v)
                line.append(s)
            s = "".join(line)
            ftxt.write(s)
            ftxt.write(os.linesep)
        ftxt.close()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--conf")
    parser.add_option("-v", "--csv")
    parser.add_option("-s", "--sep")
    parser.add_option("-t", "--txt")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.csv is None:
        print("-c <file.conf> -v <file.csv> -s <separato> -t <file.txt>")
        sys.exit(0)
    sep = '|' if opts.sep is None else opts.sep

    rx = Csv2Txt()
    rx.write_txt(opts.conf, opts.csv, opts.sep, opts.txt)
    os.chmod(opts.txt, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)
