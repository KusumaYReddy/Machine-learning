

import sys
import random
import math


#dot product function

def dot_product(a, b, cols):
    dp=0
    for j in range(0, cols, 1):
        dp += a[j]*b[j]
    return dp


datafile = sys.argv[1]
f = open(datafile)

data = []
i = 0
l = f.readline()


# READ DATA


while(l != ''):
    a = l.split()
    a_len = len(a)
    l2 = []
    for j in range(0, a_len, 1):
        l2.append(float(a[j]))
        if j == (a_len-1) :
            l2.append(float(1))
    data.append(l2)
    l = f.readline()

rows = len(data)
cols = len(data[0])
f.close()



#READ LABELS

labelfile = sys.argv[2]
f = open(labelfile)
c_var = {}
c_size = []
c_size.append(0)
c_size.append(0)
l = f.readline()

while(l != ''):
    a = l.split()
    if int(a[0]) == 0:
        c_var[int(a[1])] = -1
    else:
        c_var[int(a[1])] = int(a[0])
    l = f.readline()
    c_size[int(a[0])] += 1



#Initialize W


w = []
for j in range(0, cols, 1):
    w.append(0)
    w[j] = (0.02 * random.uniform(0,1)) - 0.01


##Gradient Descent Iteration

error = 0.0

#ompute Error
for i in range(0, rows, 1):
    if (c_var.get(i) != None):
        error += (-c_var.get(i) + dot_product(w, data[i], cols))**2

temp = 0
c=0

while(temp != 1):
    c += 1
    dellf = []
    for j in range(0,cols,1):
        dellf.append(0)
##Compute Dellf##############
    for i in range(0, rows, 1):
        if (c_var.get(i) != None):
            dp = dot_product(w, data[i], cols)
            for j in range(0, cols, 1):
                dellf[j] += ((-c_var.get(i) + dp)*data[i][j])

    eta_list = [1, .1, .01, .001, .0001, .00001, .000001, .0000001, .00000001, .000000001, .0000000001,.00000000001]
    bestobj = 1000000000000
    
    best_eta = 1
    for etas in range(0, len(eta_list), 1):
        eta = eta_list[etas]
        for j in range(0,cols,1):
            w[j] = w[j] - eta*dellf[j]
        
        error = 0.0
        for i in range(0,rows,1):
            if (c_var.get(i) != None):
                error += (-c_var.get(i) + dot_product(w, data[i], cols))**2
        obj = error

        if(obj < bestobj):
            best_eta = eta
            bestobj = obj

        for j in range(0,cols,1):
            w[j] = w[j] + eta*dellf[j]


    eta = best_eta

#Update W
    for j in range(0, cols, 1):
        w[j] = w[j] - eta*dellf[j]

#Compute Error New
    new_error = 0
    for i in range(0, rows, 1):
        if (c_var.get(i) != None):
            new_error += (-c_var.get(i) + dot_product(w, data[i], cols))**2


    if (error - new_error) < 0.001:
        temp = 1
    error = new_error

#print("count = ",c)
#print("w = ",w)

####Prediction
for i in range(0, rows, 1):
    if (c_var.get(i) == None):
        dp = dot_product(w, data[i], cols)
        if(dp>0):
            print("1",i)
        else:
            print("0",i)