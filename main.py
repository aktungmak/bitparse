import sys
import binascii
import bitstring
from PySide import QtGui
from bitparse import BitParse
from bitgui import MainView

def spacedHexToBytes(hexdata):
    return binascii.unhexlify(hexdata.translate(None, '\t\n\x0b\x0c\r '))

def process(inputData, specData):
    print "processing"
    try:
        bp = BitParse()
        parser = bp.parse(specData)[-1]

        d = spacedHexToBytes(inputData)
        bs = bitstring.BitStream(bytes=d)
        result = parser.parse(bs)
    except Exception as e:
        raise e
        # return '', str(e)
    else:
        return result, ''


if __name__ == '__main__':
    # app = QtGui.QApplication(sys.argv)
    # mw = MainView()
    # mw.registerCallback(process)

    # sys.exit(app.exec_())


    bp = BitParse(debug=1)
    with open('small.bit', 'r') as f:
        result = bp.parse(f.read())

    # d = spacedHexToBytes('FF FF 00 22 00 00 03 00 00 00 02 10 28 14 0A 01 01 01 00 0E 01 00 00 00 03 00 01 1F 40 0B B8 00 00 01')
    d = spacedHexToBytes('01 11 00 22 00 00 03')
    bs = bitstring.BitStream(bytes=d)

    try:
        res = result[-1].parse(bs)
    except bitstring.ReadError:
        print "its too short"

    print res