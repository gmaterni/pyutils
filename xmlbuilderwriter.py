#!/usr/bin/env python
import sys
from lxml import etree
from optparse import OptionParser


class UaBuilder(object):

    def __init__(self):
        self.root_tree = None
        self.xpths_list = []
        self.val_list = []
        self.col_list = []
        self.kn = {}
        self.test = ""

    def parse(self, tr):
        v = tr.text.strip() if tr.text is not None else ""
        self.val_list.append(v)
        xpth = self.root_tree.getpath(tr)
        xpths = xpth.split('/')[1:]
        self.xpths_list.append(xpths)
        # costruzione colonna db
        k = xpths[-1:][0].lower()
        self.kn[k] = (self.kn[k] + 1 if k in self.kn.keys() else 0)
        f = self.kn[k]
        s = (str(f) if f > 0 else '')
        self.col_list.append(k + s)
        for e in tr:
            self.parse(e)

    def writebuild(self):
        print("#!/usr/bin/env python")
        print("from uaxml.xmlbuilder import XmlBuilder")
        print("xb = XmlBuilder()")
        if self.test != 'test':
            print("\n")
            print("def get_xx(tag,default,opz=0):")
            print("    pass")
            print("\n")

        ll = len(self.xpths_list) - 1
        for i, r in enumerate(self.xpths_list):
            tag = r[-1:][0]
            if i == 0:
                print("xb.init(\"%s\")") % (tag)
                continue
            le = len(r)
            if i < ll:
                lnext = len(self.xpths_list[i + 1])
            else:
                lnext = le
            if lnext > le:
                print("xb.opn(%s,\"%s\")") % (le - 1, tag)
                continue
            if lnext == le:
                if self.test == "test":
                    v = self.val_list[i]
                    print("xb.ovc(%s,\"%s\",\"%s\")") % (le - 1, tag, v)
                else:
                    v = self.col_list[i]
                    print("xb.ovc(%s,\"%s\",get_xx(\"%s\",\"\",0),\"\")") % (le - 1, tag, v)
            if i == ll:
                print("xb.end()")

    def build(self, file_name, test):
        self.test = test
        f = open(file_name, 'r')
        src = f.read()
        f.close()
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.XML(src, parser)
        self.root_tree = etree.ElementTree(root)
        self.parse(root)
        self.writebuild()


def do_main(xml_path, test):
    builder = UaBuilder()
    builder.build(xml_path, test)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-x", "--xml")
    parser.add_option("-t", action="store_true", dest="test", default=False)
    try:
        opts, args = parser.parse_args()
    except Exception:
        opts = None
    if opts is None or opts.xml is None:
        print ("-x <file.xml> -t (test)")
        sys.exit(0)
    test = "test" if opts.test else ""
    do_main(opts.xml, test)
