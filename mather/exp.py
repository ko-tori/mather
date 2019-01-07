import mather.ops as ops

class Exp:
    def __repr__(self):
        return ''

    def __add__(self, other):
        return OpExp(ops.add, self, other)

    def __radd__(self, other):
        return OpExp(ops.add, other, self)

    def __sub__(self, other):
        return OpExp(ops.sub, self, other)

    def __rsub__(self, other):
        return OpExp(ops.sub, other, self)

    def __mul__(self, other):
        return OpExp(ops.mul, self, other)

    def __rmul__(self, other):
        return OpExp(ops.mul, other, self)

    def __truediv__(self, other):
        return OpExp(ops.div, self, other)

    def __rtruediv__(self, other):
        return OpExp(ops.div, other, self)

    def __pow__(self, other):
        return OpExp(ops.pow, self, other)

    def __rpow__(self, other):
        return OpExp(ops.pow, other, self)

    def __neg__(self):
        return OpExp(ops.neg, self)

class ConstExp(Exp):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

class VarExp(Exp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __add__(self, other):
        if isinstance(other, Exp):
            return OpExp(ops.add, self, other)
        else:
            return OpExp(ops.add, self, ConstExp(other))

    def __radd__(self, other):
        if isinstance(other, Exp):
            return OpExp(ops.add, other, self)
        else:
            return OpExp(ops.add, ConstExp(other), self)

    def __sub__(self, other):
        if isinstance(other, Exp):
            return OpExp(ops.sub, self, other)
        else:
            return OpExp(ops.sub, self, ConstExp(other))

    def __rsub__(self, other):
        if isinstance(other, Exp):
            return OpExp(ops.sub, other, self)
        else:
            return OpExp(ops.sub, ConstExp(other), self)

    def __mul__(self, other):
        if isinstance(other, Exp):
            return OpExp(ops.mul, self, other)
        else:
            return OpExp(ops.mul, self, ConstExp(other))

    def __rmul__(self, other):
        if isinstance(other, Exp):
            return OpExp(ops.mul, other, self)
        else:
            return OpExp(ops.mul, ConstExp(other), self)

    def __truediv__(self, other):
        if isinstance(other, Exp):
            return OpExp(ops.div, self, other)
        else:
            return OpExp(ops.div, self, ConstExp(other))

    def __rtruediv__(self, other):
        if isinstance(other, Exp):
            return OpExp(ops.div, other, self)
        else:
            return OpExp(ops.div, ConstExp(other), self)

    def __pow__(self, other):
        if isinstance(other, Exp):
            return OpExp(ops.pow, self, other)
        else:
            return OpExp(ops.pow, ConstExp(self), other)

    def __rpow__(self, other):
        if isinstance(other, Exp):
            return OpExp(ops.pow, other, self)
        else:
            return OpExp(ops.pow, ConstExp(other), self)
        
class OpExp(Exp):
    def __init__(self, op, *args):
        self.op = op
        self.args = list(args)
        if not op.nargs(len(args)):
            raise TypeError ('Invalid number of arguments for ' + op.symbol)

    def __repr__(self):
        if self.op.properties.nongroupingargs is True:
            return self.op.fmt.format(*(str(e) for e in self.args))
        formattedlist = []
        for i, e in enumerate(self.args):
            temp = str(e)
            if self.op.properties.nongroupingargs and not self.op.properties.nongroupingargs[i]:
                formattedlist.append(temp)
            elif isinstance(e, OpExp) and (e.op.precedence < self.op.precedence or
                        (not e.op.properties.associative and ((e.op.properties.associativity == 'left' and i == len(self.args) - 1 and e.op.precedence <= self.op.precedence) or
                        (e.op.properties.associativity == 'right' and i == 0 and e.op.precedence <= self.op.precedence)))):
                    formattedlist.append('(' + temp + ')')
            else:
                formattedlist.append(temp)
        return self.op.fmt.format(*formattedlist)
        
Var = VarExp

def match_formula(exp, formula):
    if isinstance(formula, ConstExp):
        if not (isinstance(exp, ConstExp) and exp.value == formula.value):
           return None
        else:
            return {}
    elif isinstance(formula, VarExp):
        return { formula.name: exp }
    elif isinstance(formula, OpExp) and isinstance(exp, OpExp) and exp.op == formula.op:
            matches = {}
            if len(exp.args) != len(formula.args):
                return None
            for e1, e2 in zip(exp.args, formula.args):
                ret = match_formula(e1, e2)
                if ret is None:
                    return None
                for k in matches.keys() & ret.keys():
                    if matches[k] != ret[k]: # the same variable matches two different expressions
                        return None
                matches.update(ret)
            return matches
    else:
        return None
    
