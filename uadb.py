#!/usr/bin/env pytho
# coding: utf-8
# uadb release 26-09-2019
import json
import sys
import stat
import os
from datetime import date
import re
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import warnings
warnings.filterwarnings("error")
# from pdb import set_trace
# import pprint
# pp = pprint.pprint

__name__ = "uadb"
__date__ = "12-12-2019"
__version__ = "0.1.8"
__author__ = "Giuseppe Materni"


class Log(object):

    def __init__(self, path_log, out=1):
        self.out = out
        self.path_log = path_log
        self.log_start = 0

    def log(self, t):
        # if isinstance(t, unicode):
        #   t = t.encode('ascii', 'replace')
        # t = t.encode('ascii', 'replace')
        s = str(t)
        if self.out == 1:
            print(s)
        with open(self.path_log, "a+") as f:
            f.write(s)
            f.write(os.linesep)
        if self.log_start == 0:
            self.log_start = 1
            os.chmod(self.path_log, 0o666)
        return self


logerr = Log("uadb.log", out=1)


"""
class UaDb

from_file(cls, file_name):
from_pars(cls, pars):
connect(self):

fetchall(self, sql, params=[], size=None):
return Result

execute(self, sql, params=[]):
insert_row(self, table, row):

class Result

properties:
cols
rowset
rows
json

methods:
value(row_num,col_name)
csv(header=1,sep='|')
write_csv(header=1,sep='|')
write_json()
"""


class DB(object):
    DATE = 'date'
    TIMESTAMP = 'timestamp'
    DECIMAL = 'decimal'
    STRING = 'string'
    LONG = 'long'
    INT = 'int'
    BOOL = 'bool'


class UaDb(object):

    @classmethod
    def from_file(cls, file_name):
        f = open(file_name, "r+")
        txt = f.read()
        f.close()
        pars = json.loads(txt)
        return cls.from_pars(pars)

    # pars={'engine':<value>,'host':<value>..}
    @classmethod
    def from_pars(cls, pars):
        engine_ = pars['engine']
        host_ = pars.get('host', None)
        user_ = pars.get('user', None)
        passwd_ = pars.get('passwd', None)
        db_ = pars['db']
        return cls(engine=engine_, host=host_, user=user_, passwd=passwd_, db=db_)

    def __init__(self, engine=None, host=None, user=None, passwd=None, db=None):
        self.engine = engine
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.db_types = {
            DB.DATE: -1,
            DB.TIMESTAMP: -1,
            DB.STRING: -1,
            DB.LONG: -1,
            DB.INT: -1,
            DB.BOOL: -1,
            DB.DECIMAL: -1}
        self.tag = None
        self.conn = None
        self.connect()

    # gestione tipi per i diversi DB
    def connect(self):
        try:

            if self.engine == "sqlite":
                import sqlite3
                self.db_types[DB.DATE] = 10
                self.db_types[DB.TIMESTAMP] = -1
                self.db_types[DB.INT] = -1
                self.db_types[DB.LONG] = -1
                self.db_types[DB.DECIMAL] = -1
                self.db_types[DB.STRING] = -1
                self.tag = "?"
                self.conn = sqlite3.connect(self.db)

            elif self.engine == "odbc":
                import pyodbc
                # $conn = odbc_connect("DRIVER={IBM i Access ODBC Driver 64-bit};System=my_iSeries", 'my_i_UID', 'my_i_PWD'); $a = 'Doe';
                # pyodbc_driver_name = "{IBM i Access ODBC Driver 64-bit}"
                # pyodbc_driver_name = "{IBM DB2 ODBC DRIVER}"
                pyodbc_driver_name = "{iSeries Access ODBC Driver}"
                # self.db_types[DB.DATE] = 1082
                # self.db_types[DB.TIMESTAMP] = -1114
                if self.passwd is not None and len(self.passwd) > 2:
                    self.conn = pyodbc.connect(
                        driver=pyodbc_driver_name,
                        system=self.host,
                        database=self.db,
                        uid=self.user,
                        pwd=self.passwd)
                else:
                    self.conn = pyodbc.connect(host=self.host, database=self.db, user=self.user)

            elif self.engine == "mysql":
                import MySQLdb
                self.db_types[DB.DATE] = MySQLdb.FIELD_TYPE.DATE
                """
                self.db_types[DB.TIMESTAMP] = -1
                self.db_types[DB.INT] = 3
                self.db_types[DB.LONG] = 8
                self.db_types[DB.DECIMAL] = 246
                self.db_types[DB.STRING] = 253
                """
                self.db_types[DB.STRING] = MySQLdb.FIELD_TYPE.DATE
                # self.db_types[DB.DATE] = 10
                self.db_types[DB.TIMESTAMP] = -1
                self.db_types[DB.INT] = 3
                self.db_types[DB.LONG] = 8
                self.db_types[DB.DECIMAL] = 246
                # self.db_types[DB.STRING] = 253
                # self.db_types[DB.STRING] = 254
                if self.passwd is not None and len(self.passwd) > 2:
                    self.conn = MySQLdb.connect(host=self.host,
                                                db=self.db,
                                                user=self.user,
                                                passwd=self.passwd)
                else:
                    self.conn = MySQLdb.connect(host=self.host,
                                                db=self.db,
                                                user=self.user)

            elif self.engine == "postgresql":
                import psycopg2
                self.db_types[DB.DATE] = 1082
                self.db_types[DB.TIMESTAMP] = 1114
                self.db_types[DB.BOOL] = 16
                self.db_types[DB.INT] = 23
                self.db_types[DB.LONG] = -1
                self.db_types[DB.DECIMAL] = 1700
                self.db_types[DB.STRING] = 1043
                if self.passwd is not None and len(self.passwd) > 2:
                    self.conn = psycopg2.connect(host=self.host,
                                                 database=self.db,
                                                 user=self.user,
                                                 password=self.passwd)
                else:
                    self.conn = psycopg2.connect(host=self.host,
                                                 database=self.db,
                                                 user=self.user)

            elif self.engine == "oracle":
                import cx_Oracle
                port = 1521
                self.db_types[DB.DATE] = 1082
                self.db_types[DB.TIMESTAMP] = 1114
                """
                dsn_tns = cx_Oracle.makedsn(self.host, port, self.db)
                self.conn = cx_Oracle.connect(self.user, self.passwd, dsn_tns)
                """
                url = "%s/%s@%s:%s/%s" % (self.user, self.passwd, self.host, port, self.db)
                self.conn = cx_Oracle.connect(url)

            elif self.engine == "mssql":
                import pymssql
                self.db_types[DB.DATE] = pymssql._mssql.SQLDATETIME
                self.db_types[DB.TIMESTAMP] = pymssql._mssql.SQLDATETIME
                self.db_types[DB.INT] = pymssql._mssql.SQLINT4
                self.db_types[DB.LONG] = pymssql._mssql.SQLINT4
                self.db_types[DB.DECIMAL] = pymssql._mssql.SQLDECIMAL
                self.db_types[DB.STRING] = pymssql._mssql.STRING
                if self.passwd is not None and len(self.passwd) > 2:
                    self.conn = pymssql.connect(host=self.host,
                                                database=self.db,
                                                user=self.user,
                                                password=self.passwd)
                else:
                    self.conn = pymssql.connect(host=self.host,
                                                database=self.db,
                                                user=self.user)

            if self.conn is None:
                raise Exception("connection is None")
        except Exception as err:
            logerr.log("connect error")
            logerr.log(err)
            sys.exit(0)

    # tag usato per la sostituzione in sqlite ? negli altri %s
    def __sql_adjust(self, sql):
        if self.tag is None:
            return sql
        else:
            return sql.replace('%s', self.tag)

    def sql_test(self, sql, pamaters):
        s = self._cur.mogrify(sql, pamaters)
        return s

    def fetchall(self, sql, params=[], size=None):
        try:
            cur = self.conn.cursor()
            sql = self.__sql_adjust(sql)
            cur.execute(sql, params)
            if size is None:
                rows = cur.fetchall()
            else:
                rows = cur.fetchmany(size)
            rt = Result(cur, rows, self.db_types)
            return rt
        except Exception as err:
            logerr.log("fetchall err")
            logerr.log(err)
            logerr.log(sql)
            sys.exit()

    def execute(self, sql, params=[]):
        try:
            sql = self.__sql_adjust(sql)
            cur = self.conn.cursor()
            rt = cur.execute(sql, params)
            self.conn.commit()
            return rt
        except Exception as err:
            logerr.log("uadb.execute error")
            logerr.log(err)
            raise Exception(sql)
            # sys.exit(1)

    # table: nome tabella
    # row:{'col0':val0,'col1':val1, ..}
    def insert_row(self, table, row):
        ks = row.keys()
        cols = ','.join(ks)
        values = row.values()
        lst = ['%s' for i in range(len(values))]
        pars = ','.join(lst)
        rt = None
        try:
            # insert into table_name ('col1','col2',..) values (%s,%s,...)
            sql = "insert into % s (%s) values(%s)" % (table, cols, pars)
            cur = self.conn.cursor()
            rt = cur.execute(sql, values)
        # except Warning as err:
        #   print(sql)
        except Exception as err:
            logerr.log("uadb.insert_row ERROR")
            s = str(err)
            logerr.log(s + os.linesep)
            raise Exception(sql)
            # sys.exit(1)
        self.conn.commit()
        return rt


class Result(object):

    def __init__(self, cur, rowset, db_types):
        self.date_fmt = "%Y-%m-%d"
        self.timestamp_fmt = "%Y-%m-%d %H:%M:%S"
        self.db_types = db_types
        self.cur = cur
        self._rowset = rowset
        self._cols = None
        self._rows = None
        self._types = None
        self._sizes = None
        self._get_description()

    def _get_description(self):
        desc = self.cur.description
        self._cols = []
        self._types = []
        self._sizes = []
        for x in desc:
            self._cols.append(x[0])
            self._types.append(x[1])
            self._sizes.append(x[3])

    @property
    def cols(self):
        return self._cols

    @property
    def types(self):
        return self._types

    def value(self, row_num, col_name):
        n = self._cols.index(col_name)
        row = self._rowset[row_num]
        return row[n]

    @property
    def rowset_native(self):
        return self._rowset

    def _adjust_field(self, r, i):
        t = self._types[i]
        v = r[i]
        """
        f = self.cols[i]
        tp = str(type(v))
        tp = tp.replace('<type', '').replace('>', '').replace('\'', '').replace('<class', '').strip()
        s = "{:3} {:20} {:15} {:10} {}".format(i, f, tp, t, v)
        print(s)
        """
        if v is None:
            return v
        try:
            if t == self.db_types[DB.DATE]:
                if len(str(v)) < 9:
                    return None
                v = date.strftime(v, self.date_fmt)
            elif t == self.db_types[DB.TIMESTAMP]:
                v = date.strftime(v, self.timestamp_fmt)
            elif t == self.db_types[DB.DECIMAL]:
                v = str(v)
            elif t == self.db_types[DB.STRING]:
                # XXX da parametrizzare
                # v = unicode(v, errors='ignore')
                v = re.sub(r'[^\x00-\x7F]', ' ', v)
                # v = v.decode('cp1252').encode('utf-8')
        except Exception as err:
            logerr.log("adjust err")
            logerr.log(err)
            logerr.log(">>> type:%s  column:%s  v:%s " % (t, i, v))
            v = None
        return v

    # ritorna una lista di liste [[val1,vale,..][val1,val2,..]]
    @property
    def rowset(self):
        le = len(self._cols)
        rows = []
        for r in self._rowset:
            row = []
            for i in range(le):
                v = self._adjust_field(r, i)
                row.append(v)
            rows.append(row)
        return rows

    # ritrona una lista di Dict  [{'col1:val1,'col2':val2, ..},{},{}]
    @property
    def rows(self):
        le = len(self._cols)
        rs = []
        for r in self._rowset:
            row = {}
            for i in range(le):
                v = self._adjust_field(r, i)
                row[self._cols[i]] = v
            rs.append(row)
        return rs

    # ritorna un file testo nel formato csv  ["val0|val1|..","val0|val1|..",..]
    def csv(self, header=1, sep='|'):
        out = StringIO()
        le = len(self._cols)
        if header:
            out.write(sep.join(self._cols))
            out.write(os.linesep)
        for r in self._rowset:
            v = self._adjust_field(r, 0)
            out.write(str(v).strip())
            for i in range(1, le):
                v = self._adjust_field(r, i)
                out.write(sep)
                out.write(str(v).strip())
            out.write(os.linesep)
        out.flush()
        return out.getvalue()

    # ritorna un testo di  [{'col1:val1,'col2':val2, ..},{},{}]
    @property
    def json(self):
        return json.JSONEncoder().encode(self.rows)

    def _write(self, file_name, txt):
        f = open(file_name, 'w+')
        f.write(txt)
        f.close()
        os.chmod(file_name, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)

    def write_csv(self, file_name, header=1, sep='|'):
        csv = self.csv(header, sep)
        self._write(file_name, csv)

    def write_json(self, file_name):
        self._write(file_name, self.json)
