#!/usr/bin/env python
# coding: utf-8
import os
import sys
import stat
from optparse import OptionParser


class Text2CsvPipe(object):

    def __init__(self):
        self.fields = None
        self.rows = None
        self.cols = None

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

    def read_txt(self, file_txt):
        ftxt = open(file_txt, "r")
        lines = ftxt.readlines()
        ftxt.close()
        self.rows = []
        for line in lines:
            row = []
            for i, f in enumerate(self.fields):
                s = line[f['start']:f['end']].strip()
                if f['typ'] == 'N':
                    row.append(s)
                else:
                    row.append('\"' + s + "\"")
            self.rows.append(row)

    def write_csv(self, file_txt, file_conf, file_csv, sep='|'):
        self.read_conf(file_conf)
        self.read_txt(file_txt)
        fcsv = open(file_csv, 'w+')
        h = sep.join(self.cols)
        fcsv.write(h + os.linesep)
        for row in self.rows:
            line = sep.join(row)
            fcsv.write(line + os.linesep)
        fcsv.close()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-c", "--conf")
    parser.add_option("-t", "--text")
    parser.add_option("-f", "--csv")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.csv is None:
        print ("-c <file.conf> -t <file.text> -f <file.csv> ")
        sys.exit(0)

    rx = Text2CsvPipe()
    rx.write_csv(opts.text, opts.conf, opts.csv)
    os.chmod(opts.csv, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)
