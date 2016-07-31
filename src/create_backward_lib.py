import sh

import sys

n=int(sys.argv[1])
objs=[]

for i in xrange(n):
    source="objs/src{0:04d}.c".format(i)
    with open(source, "w") as f:
        if(i==0):
            f.write("int fun{0}(){{return 42;}}".format(i))
        else:
            f.write("int fun{0}(); int fun{1}(){{return fun{0}();}}".format(i-1, i))
    target= "objs/src{0:04d}.o".format(i)
    objs.append(target)
    output=sh.gcc([source,"-c", "-o", target])
    if i%500==0:
        print i
    

output=sh.ar(["rcs", "libbackward.a"]+objs)
        
