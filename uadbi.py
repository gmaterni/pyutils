#!/usr/bin/env python
# coding: utf-8
from uadb import UaDb
import sys
import os


def init(ini):
    global __db
    global separator
    separator = "|"
    __db = UaDb.from_file(ini)


def query(sql):
    rt = __db.fetchall(sql)
    csv = rt.csv(header=1, sep=separator)
    print(csv)


def exe(sql):
    __db.execute(sql)


def h():
    print('query("<sql>")')
    print('exe("<sql>")')
    print("separator='<char>')")
    print("h() help")


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 0:
        print("uadb.py <file.ini>")
        sys.exit(0)
    os.putenv('PYTHONINSPECT', 'x')
    ini = args[0]
    init(ini)
    h()
