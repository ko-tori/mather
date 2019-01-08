from mather.exp import *

from string import ascii_lowercase

for i in ascii_lowercase:
    globals()[i] = Var(i)

exp = -x+(1+y)+1+1
exp2 = a+(b+c)+d+e
#print(match_formula(exp, exp2))

test = OpExp(ops.multiply, 1,2,3,x)

#print(test.evaluate(x=4))

a=convert_to_sum(1+x+1+2)
#print(a)
sort_sum(a)
#print(a)

e1 = x*y*z
e2 = z*y*x**2*b
print(common_factor(e1, e2))
