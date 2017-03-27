

N=${1:-100}

LINKER="ld"
mkdir objs

############# FORWARD:


python create_main.py $N
python create_libs.py $N

gcc main.c -c -o main.o



echo "\n\ntime linking with lforward.a:"
time -f %U gcc -o 42 main.o -lforward -L .

./42 #does the result run?
echo "forward 42 exited with code $?"


echo "\n\ntime linking with lrandom.a:"
time -f %U  gcc -o 42 main.o -lrandom -L .

./42 #does the result run?
echo "random 42 exited with code $?"




############# BACKWARD:
echo "\n\ntime linking with lbackward.a:"

time -f %U gcc -o 42 main.o -lbackward -L .  

./42 #does the result run?
echo "backward 42 exited with code $?"




### LIB_ODD_EVEN:

python create_odd_even_lib.py $N

echo "\n\ntime linking with loddeven.a:"

time -f %U gcc -o 42 main.o -loddeven -L .

./42 #does the result run?
echo "oddeven 42 exited with code $?"

############# Clean Up

rm -r objs
rm *.a
rm *.o
rm *.c
rm 42
