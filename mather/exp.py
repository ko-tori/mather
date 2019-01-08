import mather.ops as ops

class Exp:
    def __init__(self, *args):
        raise NotImplementedError('Do not instantiate Exp! Use a subclass instead')

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

    def __eq__(self, other):
        if isinstance(other, ConstExp):
            return self.value == other.value
        else:
            return self is other or self.value == other

    def evaluate(self, **kwargs):
        return self.value

class VarExp(Exp):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, VarExp):
            return self.name == other.name
        else:
            return False

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

    def evaluate(self, **kwargs):
        if self.name not in kwargs:
            return self
        else:
            return kwargs[self.name]
        
class OpExp(Exp):
    def __init__(self, op, *args):
        self.op = op
        self.args = [arg if isinstance(arg, Exp) else ConstExp(arg) for arg in args]
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

    def __eq__(self, other):
        if isinstance(other, OpExp):
            if self.op != other.op or len(self.args) != len(other.args):
                return False
            for i, j in zip(self.args, other.args):
                if i != j:
                    return False
            return True
        else:
            return False

    def evaluate(self, **kwargs):
        return self.op.apply(*(e.evaluate(**kwargs) for e in self.args))
        
Var = VarExp

def occurs(var, exp):
    if isinstance(exp, VarExp):
        return var.name == exp.name
    elif isinstance(exp, OpExp):
        for i in exp.args:
            if occurs(var, i):
                return True
    return False

def degree(exp):
    if isinstance(exp, ConstExp):
        return 0
    elif isinstance(exp, VarExp):
        return 1
    else:
        return 2 # TODO
    # degree is determined by this formula: deg(e) = 0 if e is a ConstExp, 1 if e is a VarExp, sum(deg(a[i]) for i in e.args) if e is a * OpExp, 

def convert_to_sum(exp):
    def issummate(e):
        return isinstance(e, OpExp) and e.op == ops.summate
    if isinstance(exp, OpExp):
        if exp.op == ops.add:
            arglist = []
            a1 = convert_to_sum(exp.args[0])
            a2 = convert_to_sum(exp.args[1])
            if issummate(a1):
                arglist.extend(a1.args)
            else:
                arglist.append(a1)
            if issummate(a2):
                arglist.extend(a2.args)
            else:
                arglist.append(a2)
            return OpExp(ops.summate, *arglist)
    else:
        return exp

def sort_sum(exp):
    if not (isinstance(exp, OpExp) and exp.op == ops.summate):
        return exp
    exp.args.sort(key=degree, reverse=True)
    return exp

def common_factor(e1, e2):
    # this function does not factor out constants
    exp1 = convert_to_mult(e1)
    exp2 = convert_to_mult(e2)
    if isinstance(exp1, VarExp):
        if isinstance(exp2, VarExp):
            if exp1.name == exp2.name:
                return (exp1, (ConstExp(1), ConstExp(1)))
            else:
                return (ConstExp(1), (exp1, exp2))
        elif isinstance(exp2, OpExp):
            index = next(filter(lambda ij: ij[1].name == exp1.name, enumerate(exp2.args)), (-1, None))[0]
            if index == -1:
                return (ConstExp(1), (exp1, exp2))
            else:
                del exp2.args[index]
                return (exp1, (ConstExp(1), exp2))
    elif isinstance(exp1, OpExp):
        if isinstance(exp2, VarExp):
            index = next(filter(lambda ij: ij[1].name == exp2.name, enumerate(exp1.args)), (-1, None))[0]
            if index == -1:
                return (ConstExp(1), (exp1, exp2))
            else:
                del exp1.args[index]
                return (exp2, (exp1, ConstExp(1)))
        elif isinstance(exp2, OpExp):
            i = 0
            result = []
            while i < len(exp1.args):
                index = next(filter(lambda ij: ij[1] == exp1.args[i], enumerate(exp2.args)), (-1, None))[0] # finds the index of the first occurrence of exp1[i] in exp2
                if index == -1:
                    i += 1
                else:
                    result.append(exp1.args[i])
                    del exp1.args[i]
                    del exp2.args[index]
            if len(exp1.args) == 0:
                exp1 = ConstExp(1)
            elif len(exp1.args) == 1:
                exp1 = exp1.args[0]
            if len(exp2.args) == 0:
                exp2 = ConstExp(1)
            elif len(exp2.args) == 1:
                exp2 = exp2.args[0]
            if len(result) == 0:
                return (ConstExp(1), (exp1, exp2))
            elif len(result) == 1:
                return (result[0], (exp1, exp2))
            else:
                return (OpExp(ops.multiply, *result), (exp1, exp2))
    return (ConstExp(1), (exp1, exp2))

def convert_to_mult(exp):
    def ismultiply(e):
        return isinstance(e, OpExp) and e.op == ops.multiply
    if isinstance(exp, OpExp):
        if exp.op == ops.mul:
            arglist = []
            a1 = convert_to_mult(exp.args[0])
            a2 = convert_to_mult(exp.args[1])
            if ismultiply(a1):
                arglist.extend(a1.args)
            else:
                arglist.append(a1)
            if ismultiply(a2):
                arglist.extend(a2.args)
            else:
                arglist.append(a2)
            return OpExp(ops.multiply, *arglist)
    return exp

def rebalance(exp):
    pass
    # this method should rebalance an expression's tree so that associative operations are reordered to be evaluated as if left-associative
    # actually, it will just put them into an ops.summate or ops.multiply
    # this method should also reorder commutative operations so that the operations occur in a particular order:
    #   + should order by degree then alphabet. degree is determined by the degree function
    #   * should order by alphabet, with constants first

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
    
