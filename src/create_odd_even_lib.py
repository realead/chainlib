import sh

import sys
import string
import random


n=int(sys.argv[1])
objs=[]


#even:
name="objs/even"
source=name+".c"
with open(source, "w") as f:
     for i in xrange(0,n,2):
        if(i==n-1):
            f.write("int fun{0}(){{return 42;}}\n".format(i))
        else:
            f.write("int fun{0}(); int fun{1}(){{return fun{0}();}}\n".format(i+1, i))
            
target= name+".o"
objs.append(target)
output=sh.gcc([source,"-c", "-o", target])


#odd:
name="objs/odd"
source=name+".c"
with open(source, "w") as f:
     for i in xrange(1,n,2):
        if(i==n-1):
            f.write("int fun{0}(){{return 42;}}\n".format(i))
        else:
            f.write("int fun{0}(); int fun{1}(){{return fun{0}();}}\n".format(i+1, i))
            
            
target= name+".o"
objs.append(target)
output=sh.gcc([source,"-c", "-o", target])

    
#create library
output=sh.ar(["rcs", "liboddeven.a"]+objs)

        
