from K_means import *

result = k_means(7, 0.000001)
for i in range(len(result)):
    print(len(result[i]))
