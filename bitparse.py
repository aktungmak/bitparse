import ply.yacc as yacc
import ply.lex as lex
from astobjects import Field, ForLoop, IfBlock, Structure, Value
from bitlex import BitLex

class BitSyntaxException(Exception):
    pass

## start of parser ##############################
class BitParse(object):
    tokens = BitLex.tokens
    precedence = [
        ('left','PLUS','MINUS','TIMES','DIVIDE','EQUAL','UNEQUAL'),
    ]


    def __init__(self, **kw):
        self.debug = kw.get('debug', 0)
        self.scopestack = []
        self.current_scope = { }
        self.structures = { }
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        # self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        # Build the lexer and parser
        bl = BitLex()
        bl.build()
        yacc.yacc(module=self,
                  debug=self.debug,
                  # debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def parse(self, string):
        return yacc.parse(string)

    # a complete definition file, with zero or more structures
    def p_struct_list(self, p):
        '''
        struct_list : empty
                    | struct struct_list
        '''
        if p[1] is None:
            p[0] = []
        else:
            # self.structures[p[2].name] = p[2]
            p[0] = [p[1]]+p[2]

    def p_struct_name(self, p):
        'struct_name : ID'
        p[0] = p[1]

    # define a single structure
    def p_struct(self, p):
        'struct : struct_name LCURLY new_scope fields end_scope RCURLY'
        ns = Structure(p[1], p[4])
        p[0] = ns
        self.structures[ns.name] = ns

    # a structure can contain zero or more fields
    def p_fields(self, p):
        '''
        fields : empty
               | field fields
        '''
        if p[1] is None:
            p[0] = []
        else:
            p[0] = p[1]+p[2]

    # an individual field of a structure
    def p_field(self, p):
        '''
        field : ID expression type
              | ALIGN
              | struct_call
              | ifcond
              | forloop
        '''
        if len(p) == 4:
            f = Field(p[1], p[2], p[3])
            self.current_scope[p[1]] = f
            p[0] = [f]
        else:
            # todo handle ALIGN keyword
            p[0] = p[1]

    # specify the type of a field, so it can be interpreted
    def p_type(self, p):
        '''
        type : UINT
             | STUFF
             | BITSTR
             | RPCHOF
        '''
        p[0] = p[1]

    # call a previous definition of a structure
    def p_struct_call(self, p):
        'struct_call : struct_name LPAREN RPAREN'
        try:
            p[0] = [self.structures[p[1]]]
        except KeyError as e:
            raise BitSyntaxException('line %d: undeclared structure %s' % (p.lineno(1), p[1]))

    # add fields based on a condition
    def p_ifcond(self, p):
        'ifcond : IF LPAREN comparison RPAREN LCURLY fields RCURLY'
        p[0] = [IfBlock(p[3], p[6])]

    # repeat fields while for condition is true
    def p_forloop(self, p):
        'forloop : FOR LPAREN expression RPAREN LCURLY fields RCURLY'
        p[0] = [ForLoop(p[3], p[6])]

    def p_comparison_binop(self, p):
        '''comparison : expression EQUAL expression
                      | expression UNEQUAL expression
                      | expression MORE expression
                      | expression LESS expression
                      | expression MOREEQ expression
                      | expression LESSEQ expression
        '''
        # watch out! the lambdas don't close over the value
        # of p[1] and p[3]!! so when they are called they
        # get some bizarro results instead.
        # so, we need to make our own local copies.
        fst = p[1]
        snd = p[3]
        if   p[2] == '==': p[0] = lambda: fst() == snd()
        elif p[2] == '!=': p[0] = lambda: fst() != snd()
        elif p[2] == '>' : p[0] = lambda: fst() >  snd()
        elif p[2] == '<' : p[0] = lambda: fst() <  snd()
        elif p[2] == '>=': p[0] = lambda: fst() >= snd()
        elif p[2] == '<=': p[0] = lambda: fst() <= snd()

    # mathematical expression
    def p_expression_binop(self, p):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression
        '''
        if   p[2] == '+' : p[0] = lambda: p[1]() +  p[3]()
        elif p[2] == '-' : p[0] = lambda: p[1]() -  p[3]()
        elif p[2] == '*' : p[0] = lambda: p[1]() *  p[3]()
        elif p[2] == '/' : p[0] = lambda: p[1]() /  p[3]()

    # a numeric literal
    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = Value(p[1])

    # use the value of an existing field
    def p_expression_name(self, p):
        'expression : ID'
        p[0] = self.current_scope[p[1]]

    # Create a new scope for local variables
    def p_new_scope(self, p):
        'new_scope :'
        self.scopestack.append(self.current_scope)
        self.current_scope = { }

    def p_end_scope(self, p):
        'end_scope :'
        self.current_scope = self.scopestack.pop()

    # empty production, for clarity
    def p_empty(self, p):
        'empty :'
        pass

    # Error rule for syntax errors
    def p_error(self, p):
        print "Syntax error in input:", p


## end of parser ################################
if __name__ == '__main__':
    bp = BitParse(debug=1)
    with open('small.bit', 'r') as f:
        result = bp.parse(f.read())
    print "here is the result: ", map(str, result)
    print '== structures ====='
    print bp.structures
