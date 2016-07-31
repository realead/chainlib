import sh
import sys

n=int(sys.argv[1])

source="forward_main.c"
with open(source, "w") as f:
    f.write("int fun{0}(); int main(){{return fun{0}();}}".format(0))

        
