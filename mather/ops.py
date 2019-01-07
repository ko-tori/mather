# 'commutative' means the order of the arguments does not matter.
# 'nogroup' means the operation does not require parentheses when performed before another operation with higher precedence.
# 'nongroupingargs' is a list of which arguments do not need to be grouped, e.g the arguments of max(a, b) would have a list [True, True] or just the value True to signify all arguments are nongrouping.
#                   Falsy values mean all arguments should be grouped as precedence dictates.

class Properties:
    commutative = False
    associative = False
    nogroup = False
    nongroupingargs = False
    associativity = 'left'
    def __init__(self, properties):
        if 'commutative' in properties:
            self.commutative = properties['commutative']
        if 'associative' in properties:
            self.associative = properties['associative']
        if 'nogroup' in properties:
            self.nogroup = properties['nogroup']
        if 'nongroupingargs' in properties:
            self.nongroupingargs = properties['nongroupingargs']
        if 'associativity' in properties:
            self.associativity = properties['associativity']

class Op:
    def __init__(self, symbol, fmt, nargs, apply, precedence, properties=Properties({})):
        self.symbol = symbol
        self.fmt = fmt
        if callable(nargs):
            self.nargs = nargs
        else:
            self.nargs = lambda x: x == nargs
        self.apply = apply
        self.precedence = precedence
        self.properties = properties

    def __repr__(self):
        return self.symbol

# precedence 0
add = Op('+', '{}+{}', 2, lambda x, y: x + y, 0, Properties({
    'commutative': True,
    'associative': True
}))
sub = Op('-', '{}-{}', 2, lambda x, y: x - y, 0)

summate = Op('+', type('summate_fmt_ty', (object,), { 'format': lambda *x: '+'.join(x[1:]) })(), lambda x: x > 0, lambda *x: sum(x), 0)

# precedence 1
neg = Op('-', '-{}', 1, lambda x: -x, 1)

mul = Op('*', '{}*{}', 2, lambda x, y: x * y, 1, Properties({
    'commutative': True,
    'associative': True
}))
div = Op('/', '{}/{}', 2, lambda x, y: x / y, 1)

# precedence 2
pow = Op('**', '{}**{}', 2, lambda x, y: x ** y, 2, Properties({
    'associativity': 'right'
}))
