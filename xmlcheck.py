#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser
from lxml import etree


def do_main(xml_path):

    with open(xml_path, "rt") as f:
        xml = f.read()
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.XML(xml, parser)
        s = etree.tostring(root, pretty_print=True)
    except etree.Error as e:
        s = e.message
        print("error")
        print(s)
        out_path = xml_path.replace('.xml', '_err.txt')
        with open(out_path, "w+") as fo:
            fo.write(s)
    else:
        print("XML corretto")


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-x", "--xml")
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.xml is None:
        print ("-x <file.xml> --xml=<file.xml> ")
        sys.exit(0)
    do_main(opts.xml)
