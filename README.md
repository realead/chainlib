# chainlib
a small framework demostrating O(n^2) behavior of the ld-linker

## Prerequisites

  1. linux + gcc + ld
  2. python 2.7
  3. python sh module (https://amoffat.github.io/sh/)
  
## Motivation
  This article is a great explanation how the linker works: http://eli.thegreenplace.net/2013/07/09/library-order-in-static-linking
  
  From this explanation follows, that the running time for the linking of a library is `O(n^2)` with `n` number of object files in this library. The important passage is this one:
  
  > When the linker encounters a new library, things are a bit more interesting. The linker goes over all the objects in the library. For each one, it first looks at the symbols it exports.
  >   - ...
  >   - Finally, if any of the objects in the library has been included in the link, the library is rescanned again - it's possible that symbols imported by the included object can be found in other objects within the same library.

For a chain library with following dependencies needs only `1` iteration:

    obj1->obj2->obj3->...->objn
    
(this means that the functions in `obj1` call (only) functions from `obj2` which call only functions from `obj3` and so on.)

Yet for a chain library with the following dependencies as many as `n` iterations could be needed: 

    obj1<-obj2<-obj3<-...<-objn

(this means that the functions in `objn` call (only) functions from `objn-1` which call only functions from `objn-2` and so on.)

This is the case if only a function from 'objn' is invoked in `main`. 

This framework verifys, that the ld-behavior is exactly how it is explained in the article above (which is a little bit surprisingly, because I think it is possible to avoid this `O(n^2)' behavior, but I guess it was never a bottle neck).

## Usage

The scripts are in *src*-folder. Call

    sh build.sh N
    
with `N` - the desired number of object files in the library.



## Results

There are 4 kinds of library created/used:
   1. *libforward.a* - only one iteration throught the library is needed
   2. *librandom.a* - the objects are shuffled randomly in the library
   3. *libackward.a* - worst case, *n* iteration through the library are needed.
   4. *libevenodd.a* - consists of 2 object files (thus way compiler cannot perform optimization and inline the functions as calls switch between the two object files): 
      1. even.o = contents of obj2.o+obj4.o+obj6.o+...
      2. odd.o = contents of  obj1.o+obj3.o+obj5.o+...
   
 The times needed for linking of main.o against the libraries with *ld*-linker are (depending on *N* - the number of the object files in the library):

|N        | libforward.a | librandom.a | libbackward.a |libevenodd.a  |
|:--------|-------------:|------------:|--------------:|-------------:|
|100      |     0.04s    |    0.04s    |      0.04s    |      0.04s   |
|1000     |    0.10s     |    0.12s    |      0.13s    |      0.04s   |
|5000     |    0.54s     |    0.81s    |      1.00s    |      0.04s   |
|10000    |    1.07s     |    2.43s    |      3.27s    |      0.05s   |
|50000    |    5.40s     |   52.2s     |     76.8s     |      0.13s   |

### Conclusion:
The worst case `O(n^2)` behavior of *ld* is pretty obvious (*libbackward.a*). But also the average case is also almost `O(n^2)` (*librandom.a*). This means that the linkager against libraries with very many object files can take disproportional longer. 

To put all functions in one object file would result in the fastest linking time (see *libevenodd.a*), however that would result in an executable with all symbols (even if some of them are not needed and would be excluded by linker for other libraries (forward, backward, random)).

### Explanation for running time of librandom.a

A hand waving explanation, why *librandom.a* is almost as bad as *libbackward.a*. 

The question is: 
>Given a chain library with n objects and random permutation, what is the expected streak length for the first iteration, i.e. how many object files are added to the exe. 

The position of the first object file is uniformly distributed in [0, n-1], thus the average streak length `L(n)` can be calculated as:

    L(n)=1+1/n\sum_{i=1}^{n-1}L(i)
    L(1)=1
    
from this we get:
    
    nL(n)-(n-1)L(n-1)=n+\sum_{i=1}^{n-1}L(i)-(n-1)-\sum_{i=1}^{n-2}L(i)=1+L(n-1) =>
    L(n)=1/n+L(n-1) =>
    L(n)=\sum_{i=1}^{n}\approx log(n)
    
So we could estimate the running time as `O(n^2/log(n))`
  
