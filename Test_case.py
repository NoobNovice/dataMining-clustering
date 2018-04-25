from K_means import *
import math
x = k_means(1, 0.01)
xx = []
for i in range(len(x)):
    xx.append(len(x[i]))
    print(len(x[i]))

meanss = sum(xx)/len(x)
print(meanss)
sums = 0
for i in range(len(x)):
    sums += math.pow(len(x[i])-meanss,2)
sd = math.sqrt(sums/len(x))
print(sd)
