import binascii
import bitstring

def spacedHexToBytes(hexdata):
    return binascii.unhexlify(hexdata.translate(None, '\t\n\x0b\x0c\r '))

if __name__ == '__main__':
    d = spacedHexToBytes('62 63 64 65 66 67 68 69 70')
    bs = bitstring.BitStream(bytes=d)
    print bs.unpack('bytes:2, uint:12')

