import ply.lex as lex

## start of lexer ###############################

class BitLex(object):
    reserved = {
        'if' : 'IF',
        'for' : 'FOR',
        'alignment' : 'ALIGN',
        'uimsbf' : 'UINT',
        'stuff' : 'STUFF',
        'bslbf' : 'BITSTR',
        'rpchof' : 'RPCHOF',
    }

    tokens = [
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
        'EQUAL', 'UNEQUAL', 'LESS', 'MORE', 'LESSEQ', 'MOREEQ',
        'LCURLY', 'RCURLY', 'LPAREN', 'RPAREN',
        'ID', 'NUMBER',
        ] + reserved.values()

    # Tokens

    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LCURLY  = r'\{'
    t_RCURLY  = r'\}'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_EQUAL   = r'=='
    t_UNEQUAL = r'!='
    t_MORE    = r'>'
    t_LESS    = r'<'
    t_MOREEQ  = r'>='
    t_LESSEQ  = r'<='

    def t_NUMBER_hex(self, t):
        r'0x[0-9A-Fa-f]+'

        t.type = 'NUMBER'
        t.value = t.value.split('0x')[1]
        try:
            t.value = int(t.value, 16)
        except ValueError:
            print "Couldn't parse integer ", t.value
            t.value = 0

        return t

    def t_NUMBER_dec(self, t):
        r'\d+'
        t.type = 'NUMBER'
        try:
            t.value = int(t.value, 10)
        except ValueError:
            print "Couldn't parse integer ", t.value
            t.value = 0

        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # Check for reserved words
        t.type = self.reserved.get(t.value,'ID')
        return t

    # Ignored characters
    t_ignore = ' \t\v\r'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

if __name__ == '__main__':
    bl = BitLex()
    bl.build()
    with open('mom_sample.bit', 'r') as f:
        bl.lexer.input(f.read())
    while True:
        tok = bl.lexer.token()
        if not tok:
            break
        print tok

## end of lexer #################################