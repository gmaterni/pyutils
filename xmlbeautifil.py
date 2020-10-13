#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser
from lxml import etree
import string


def do_main(xml_path, out_path):

    with open(xml_path, "rt") as f:
        xml = f.read()
    try:
        printable = set(string.printable)
        xml = filter(lambda x: x in printable, xml)
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.XML(xml, parser)
        s = etree.tostring(root, pretty_print=True)
    except etree.Error as e:
        s = e.message
        print("error")
        out_path = xml_path.replace('.xml', '_err.txt')
        print(s)
    if out_path is None:
        print(s)
    else:
        with open(out_path, "w+") as fo:
            fo.write(s)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-x", "--xml")
    parser.add_option("-o", "--out")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.xml is None:
        print( "-x <file.xml> --xml=<file.xml> [ -o <file di output>] out=<file di output> ]")
        sys.exit(0)
    do_main(opts.xml, opts.out)
