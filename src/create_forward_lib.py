import sh

import sys
import string
import random


n=int(sys.argv[1])
objs=[]


for i in xrange(n):
    name="objs/{0}{1:04d}".format(random.choice(string.ascii_letters), i)
    source=name+".c"
    with open(source, "w") as f:
        if(i==n-1):
            f.write("int fun{0}(){{return 42;}}".format(i))
        else:
            f.write("int fun{0}(); int fun{1}(){{return fun{0}();}}".format(i+1, i))
    target= name+".o"
    objs.append(target)
    output=sh.gcc([source,"-c", "-o", target])
    if i%500==0:
        print i
    
#create libraries
output=sh.ar(["rcs", "libforward.a"]+objs)

random.shuffle(objs)
output=sh.ar(["rcs", "librandom.a"]+objs)
        
