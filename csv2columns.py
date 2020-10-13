#!/usr/bin/env python
# -*- coding: utf-8 -*-
# release 15-03-2017

import sys
# import os
from optparse import OptionParser
# import csv
import re
import os
# import pdb


def do_main(csv_path, delimiter, txt_path):
    ftxt = open(txt_path, 'w+')
    f = open(csv_path, 'rb')
    for line in f:
        fs = line.split(delimiter)
        for col in fs:
            v = re.sub(r'[^\x00-\x7F]', '', col)
            s = v.lower().strip().replace(' ', '_').replace('.', '').replace('"', '')
            ftxt.write(s)
            ftxt.write(os.linesep)
        break
    f.close()
    ftxt.close()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--csv")
    parser.add_option("-s", "--sep")
    parser.add_option("-t", "--txt")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.csv is None or opts.txt is None:
        print ("--c <file.csv> -s <separator> -t <file.txt> ")
        sys.exit(0)
    delimiter = '|' if opts.sep is None else opts.sep
    do_main(opts.csv, delimiter, opts.txt)
