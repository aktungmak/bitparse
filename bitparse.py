import ply.yacc as yacc
import ply.lex as lex
from astobjects import Field, Structure
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
        self.current_scope = { }
        self.structures = { }
        try:
            modname = os.path.split(os.path.splitext(__file__)[0])[1] + "_" + self.__class__.__name__
        except:
            modname = "parser"+"_"+self.__class__.__name__
        self.debugfile = modname + ".dbg"
        self.tabmodule = modname + "_" + "parsetab"

        # Build the lexer and parser
        bl = BitLex()
        bl.build()
        yacc.yacc(module=self,
                  debug=self.debug,
                  debugfile=self.debugfile,
                  tabmodule=self.tabmodule)

    def parse(self, string):
        return yacc.parse(string)

    # a complete definition file, with zero or more structures
    def p_structures(self, p):
        '''
        structures : empty
                   | structures structure
        '''
        if p[1] is None:
            p[0] = []
        else:
            self.structures[p[2].name] = p[2]
            p[0] = p[1]+[p[2]]


    # define a single structure
    def p_structure(self, p):
        'structure : ID LCURLY new_scope fields RCURLY'
        p[0] = Structure(p[1], p[4])

    # a structure can contain zero or more fields
    def p_fields(self, p):
        '''
        fields : empty
               | fields field
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
              | structcall
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
    def p_structcall(self, p):
        'structcall : ID LPAREN RPAREN'
        try:
            p[0] = [self.structures[p[1]]]
        except KeyError as e:
            raise BitSyntaxException('line %d: undeclared structure %s' % (p.lineno(1), p[1]))
    # add fields based on a condition
    def p_ifcond(self, p):
        'ifcond : IF LPAREN expression RPAREN LCURLY fields RCURLY'
        print "condition:", p[3], p.lineno(1)
        if p[3]:
            p[0] = p[6]
        else:
            p[0] = []

    # repeat fields while for condition is true
    def p_forloop(self, p):
        'forloop : FOR LPAREN expression RPAREN LCURLY fields RCURLY'
        p[0] = p[6] * p[3]

    # mathematical expression
    def p_expression_binop(self, p):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression
                      | expression EQUAL expression
                      | expression UNEQUAL expression
        '''
        print map(str, p)
        if   p[2] == '+' : p[0] = p[1] +  p[3]
        elif p[2] == '-' : p[0] = p[1] -  p[3]
        elif p[2] == '*' : p[0] = p[1] *  p[3]
        elif p[2] == '/' : p[0] = p[1] /  p[3]
        elif p[2] == '==': p[0] = p[1] == p[3]
        elif p[2] == '!=': p[0] = p[1] != p[3]

    # grouping mathemetical expressions
    def p_expression_group(self, p):
        'expression : LPAREN expression RPAREN'
        p[0] = p[2]

    def p_expression_number(self, p):
        'expression : NUMBER'
        p[0] = p[1]

    def p_expression_name(self, p):
        'expression : ID'
        p[0] = self.current_scope[p[1]].value

    # Create a new scope for local variables
    def p_new_scope(self, p):
        'new_scope :'
        return
        print '== old scope ====='
        for k, v in self.current_scope.iteritems():
            print k, v
        print 'making a new scope ======='
        self.current_scope = { }

    # empty ptoduction, for clarity
    def p_empty(self, p):
        'empty :'
        pass

    # Error rule for syntax errors
    def p_error(self, p):
        print "Syntax error in input: ", p


## end of parser ################################
if __name__ == '__main__':
    bp = BitParse(debug=1)
    with open('mom_sample.bit', 'r') as f:
        result = bp.parse(f.read())
    print "here is the result: ", result
    print '== structures ====='
    print bp.structures
