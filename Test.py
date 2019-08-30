import numpy as np
import copy
import sys
import Optimizer as Op
from bitarray import bitarray
def Ob(a,b):

    return np.array([a],dtype='i1')

def aid(x):
    # This function returns the memory
    # block address of an array.
    return x.__array_interface__['data'][0]

class obj:

    def __init__(self):

        self.a=[1,2,3,8,9,2,1,4,5,1,6,1,5,1,3,2]
        self.b=None



Z=np.ndarray((4,),dtype=[('Eff_Val','i1'),('Sig_Hash','i4'),('Driver_Head','i4'),('Processes','object'),('Process_Driver_Hash_Map','object'),('Driver','object')])

print("Length="+str(Z.shape[0]))

for i in range(0,4):

        Z[i][0]=0
        Z[i][1]=-1
        Z[i][2]=-1
        Z[i][3]=np.ndarray((5,),dtype='i4')

print(Z[0]['Sig_Hash'])

print("Consider Location")

print(aid(Z), aid(Z[1:]))

print(Z.dtype)


d={}


d.update({1:1})

for i in range(2,10000):
        d.update({i:i})
        if(i%100 == 0):
                print(sys.getsizeof(d))


print(sys.getsizeof(d))

print(str(4*2*10000))


Fill=np.zeros((4,),dtype=(np.uint8,np.uint8))



print("Fill is "+str(Fill))

print("List")

L=[None]*8*10



del L[:]

print(hex(id(L)))

print(L)
print(hex(id(L)))

#func=Op.switcher.get(11,"Nothing")

#print(func(11))

b = 255 

if(bool(b ^ 255)):
        print("Set")
else:
        print("Not Set")


L=np.ndarray((2,),dtype=[("Val",'i1'),("Obj",'object')])

print("Size of L is "+str(sys.getsizeof(L)))

print("Size of object type "+str(sys.getsizeof(L[0][1])))

print("Next array pointer "+str(aid(L)))

m=np.zeros((10,0),dtype=int)

L[0][1]=m

print("Size of object type "+str(sys.getsizeof(L[0][1])))

print("Next array pointer "+str(aid(L)))



D = {}

print("Size of Dic = "+str(sys.getsizeof(D)))

for i in range(0,10):

        D.update({i:i})

print("Size of Dic = "+str(sys.getsizeof(D)))

#del D[:]

print("Size of Dic = "+str(sys.getsizeof(D)))

a = bitarray(5)
b = bitarray(5)

c = a | b

for i in range(0,len(c)):
        if(c[i]):
                print("Yes")
        else:
                print("No")

lst = []

for i in range(0,1):

        lst.append(bitarray(5))

print(lst)

Z = np.asarray(lst,dtype=bitarray)

print("Size of Z is "+str(sys.getsizeof(Z)))


M = np.zeros((11,),dtype=[('1','u1'),('2','u1')])

print("M is "+str(M))

ele = M[1]

print("Size of M = "+str(sys.getsizeof(M)))
print("Size of ele = "+str(sys.getsizeof(ele)))

print("Shape of ele = "+str(len(ele)))


ele['1'] = 89
ele['2'] = 89

print("M is "+str(M))


Ar = np.ndarray((1,),dtype='u1')

print("Size of Ar is "+str(sys.getsizeof(Ar)))

Ar[0]=255

if(Ar[0] < 0):
        print("Passed")
else:
        print("Failed")


for i in range(1,0):
        print("Guddu")
