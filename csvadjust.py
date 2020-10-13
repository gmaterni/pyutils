#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import os
from optparse import OptionParser
# from pdb import set_trace


class CsvAdjust(object):

    def __init__(self, sep):
        self.delimiter = sep

    def adjust(self, row):
        fso = row.split(self.delimiter)
        fsn = []
        for c, f in enumerate(fso):
            t = f.strip().replace("\"", "")
            s = re.sub(r'[^\x00-\x7F]', ' ', t)
            fsn.append(s)
        return self.delimiter.join(fsn)

    def csv_rw(self, csv_in, csv_ou):
        # set_trace()
        file_ou = open(csv_ou, 'w+')
        file_in = open(csv_in, 'r+')
        rows = file_in.readlines()
        file_ou.write(rows[0].replace("\"", ""))
        # file_ou.write(os.linesep)
        try:
            for row in rows[1:]:
                r = self.adjust(row)
                file_ou.write(r)
                file_ou.write(os.linesep)
        except Exception:
            print(row)
            print("row: %s" % (r))
        file_ou.close()
        file_in.close()
        os.chmod(csv_ou, 0o666)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--inp")
    parser.add_option("-o", "--out")
    parser.add_option("-s", "--sep")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.inp is None or opts.out is None:
        print("-i <csv input> -o <csv out> -s <separator> ")
        sys.exit(0)
    sep = '|' if opts.sep is None else opts.sep
    rx = CsvAdjust(sep)
    rx.csv_rw(opts.inp, opts.out)
