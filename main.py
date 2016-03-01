import sys
import binascii
import bitstring
import json
from collections import OrderedDict
from PySide import QtGui
from bitparse import BitParse
from bitgui import MainView

def to_sexpr(o, level=0):
    INDENT = 2
    SPACE = " "
    NEWLINE = "\n"

    ret = ""
    if isinstance(o, dict):
        ret += "(" + NEWLINE
        comma = ""
        for k,v in o.iteritems():
            ret += comma
            comma = " \n"
            ret += SPACE * INDENT * (level+1)
            ret += '"' + str(k) + '":' + SPACE
            ret += to_sexpr(v, level + 1)
        ret += NEWLINE + SPACE * INDENT * level + ")"
    elif isinstance(o, list):
        ret += "(" + NEWLINE
        comma = ""
        for v in o:
            ret += comma
            comma = " \n"
            ret += SPACE * INDENT * (level+1)
            ret += to_sexpr(v, level + 1)

    elif isinstance(o, basestring):
        ret += o
    elif isinstance(o, tuple):
        ret += "(" + " ".join([to_sexpr(e, level+1) for e in o]) + ")"
    elif isinstance(o, bool):
        ret += "true" if o else "false"
    elif isinstance(o, (int, long)):
        ret += str(o)
    elif isinstance(o, float):
        ret += '%.7g' % o
    elif o is None:
        ret += 'null'
    else:
        raise TypeError("Unknown type '%s' for json serialization" % str(type(o)))
    return ret

def spacedHexToBytes(hexdata):
    hexdata = str(hexdata)
    return binascii.unhexlify(hexdata.translate(None, '\t\n\x0b\x0c\r '))

def formatResult(resultList, level=0):
    resStr = to_sexpr(resultList)
    return resStr

def process(inputData, specData):
    try:
        bp = BitParse()
        parser = bp.parse(specData)[-1]

        d = spacedHexToBytes(inputData)
        bs = bitstring.BitStream(bytes=d)
        result = parser.parse(bs)
        left = len(bs) - bs.pos
    except Exception as e:
        raise e
        return '', str(e)
    else:
        return formatResult(result), 'finished with %d bits left over' % left


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainView()
    mw.registerCallback(process)

    sys.exit(app.exec_())