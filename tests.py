import time
import numpy as np
from class_item import Item

start_time = time.time()
it = Item(1, np.array([[0.3, 0], [0, 1], [0.7, 1.5], [1.2, 0.8], [3, 0.8], [3, 0.4], [1.2, 0.4], [0.6, 0.8]]))
it.list_of_MixedShiftC_4R(0.1)
print("--- %s seconds ---" % (time.time() - start_time))

# start_time=time.time()
# print("--- %s seconds ---" % (time.time() - start_time))

# mat0=np.array([[0,1,0],[1,1,0],[0,0,1]], dtype = int)
# print(mat0)
# mat1=np.copy(np.rot90(mat0, 1))
# print(mat0)
# print(mat1)
# mat1[0][0]=3
# print(mat1)


# print(1.3//0.5, int(1.4/0.5))
# print(int(12.9))
# print(round(3.75, 1))
# print(7.3 % 2)


# print("fghj"+str(10))
# print(type(u"tye"))
# print(type("tye"))


# for i in range(0, 3, 1): 
#     print(i)
