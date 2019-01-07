from mather.exp import *

import string

for i in string.ascii_lowercase:
    globals()[i] = Var(i)

exp = -x+(1+y)+1+1
exp2 = a+(b+c)+d+e
print(match_formula(exp, exp2))
