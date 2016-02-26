import sys
import binascii
import bitstring
import json
from collections import OrderedDict
from PySide import QtGui
from bitparse import BitParse
from bitgui import MainView

def to_sexpr(o, level=0):
    NEWLINE = '\n'
    SPACE = ' '
    INDENT = 2
    ret = ''
    if isinstance(o, basestring):
        ret += o
    elif isinstance(o, (list, tuple)):
        ret += SPACE * INDENT * level
        ret += '('
        if len(o) < 3:
            comma = SPACE
        else:
            comma = NEWLINE

        for v in o:
            if isinstance(v, (list, tuple)):
                ret += '\n'
            ret += to_sexpr(v, level + 1)
            ret += comma

        # ret += SPACE * INDENT * level
        ret += ')\n'


        # ret += '(' + ' '.join([to_sexpr(e, level+1) for e in o]) + ')' + NEWLINE
    elif isinstance(o, bool):
        ret += 'true' if o else 'false'
    elif isinstance(o, int):
        ret += str(o)
    elif isinstance(o, float):
        ret += '%.7g' % o
    elif o is None:
        ret += 'null'
    else:
        raise TypeError('Unknown type "%s" for sexpr serialization' % str(type(o)))
    return ret

def spacedHexToBytes(hexdata):
    hexdata = str(hexdata)
    return binascii.unhexlify(hexdata.translate(None, '\t\n\x0b\x0c\r '))

def formatResult(resultList, level=0):
    resStr = to_sexpr(resultList)
    # resStr = pprint.pformat(resultList, indent=2)
    resStr = resStr.replace('[', '(')
    resStr = resStr.replace(']', ')')
    resStr = resStr.replace(', \r\n', ' ')


    return resStr

def process(inputData, specData):
    print 'processing'
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


    # bp = BitParse(debug=1)
    # with open('mom_sample.bit', 'r') as f:
    #     result = bp.parse(f.read())

    # d = spacedHexToBytes('FF FF 00 22 00 00 03 00 00 00 02 10 28 14 0A 01 01 01 00 0E 01 00 00 00 03 00 01 1F 40 0B B8 00 00 01')
    # # d = spacedHexToBytes('01 11 00 22 00 00 03')
    # bs = bitstring.BitStream(bytes=d)

    # try:
    #     res = result[-1].parse(bs)
    #     left = len(bs) - bs.pos
    # except bitstring.ReadError:
    #     print 'its too short'
    # else:
    #     print 'finished with %d bits left over' % left

    # print res