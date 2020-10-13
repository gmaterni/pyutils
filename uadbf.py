#!/usr/bin/env python
# coding: utf-8
from uadb import UaDb
import sys


def h():
    print("uadbf <file.ini> <file sql> [<file output>] ")


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 2:
        h()
        sys.exit(0)
    ini = args[0]

    fsql = args[1]
    f = open(fsql, "r+")
    sql = f.read()
    f.close()
    print(sql)
    sep = "|"

    fout = None if len(args) < 3 else args[2]

    db = UaDb.from_file(ini)
    rt = db.fetchall(sql)
    if rt is None:
        print("sql errore")
        sys.exit(1)
    if fout is None:
        print(rt.csv(header=1, sep=sep))
    else:
        rt.write_csv(fout, sep=sep)
