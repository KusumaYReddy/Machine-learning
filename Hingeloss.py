import sys
import random
import math


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

while(l != ''):
    a = l.split()
    length = len(a)
    l2 = []
    for j in range(0, length, 1):
        l2.append(float(a[j]))
        if j == (length-1) :
            l2.append(float(1))
    data.append(l2)
    l = f.readline()

rows = len(data)
cols = len(data[0])
f.close()

labelfile = sys.argv[2]
f = open(labelfile)
trainlabels = {}
size = []
size.append(0)
size.append(0)
l = f.readline()

while(l != ''):
    a = l.split()
    if int(a[0]) == 0:
        trainlabels[int(a[1])] = -1
    else:
        trainlabels[int(a[1])] = int(a[0])
    l = f.readline()
    size[int(a[0])] += 1



w = []
for j in range(0, cols, 1):
    w.append(0)
    w[j] = (0.02 * random.uniform(0,1)) - 0.01


eta_list = [1, .1, .01, .001, .0001, .00001, .000001, .0000001, .00000001, .000000001, .0000000001, .00000000001 ]
bestobj = 1000000000000000000
temp = 1
c = 0
error = 0.0

for i in range(0, rows, 1):
    if (trainlabels.get(i) != None):
        dp = dot_product(w, data[i], cols)
        temp = (trainlabels.get(i)*dp)
        if (temp <1):
            error += (trainlabels.get(i)-(1-temp))

prev_error = error
while(abs(temp)>0.001):
    dellf = []
    for j in range(0,cols,1):
        dellf.append(0)
    temp = 0
    for i in range(0, rows, 1):
        if (trainlabels.get(i) != None):
            dp = dot_product(w, data[i], cols)
            for j in range(0,cols,1):
                temp=(trainlabels.get(i)*dp)
                if temp<1:
                    dellf[j] += (data[i][j]*trainlabels.get(i))
    
    best_eta = 1
    for i in range(0, len(eta_list), 1):
        eta = eta_list[i]
        for j in range(0,cols,1):
            w[j] += eta*dellf[j]

        error = 0
        lc = 0
        for i in range(0,rows,1):
            if trainlabels.get(i)!=None:
                lc += 1
                dp = dot_product(w, data[i], cols)
                temp=(trainlabels.get(i)*dp)
                if temp<1:
                    error += (1-temp)
        obj = error
        if obj < bestobj:
            bestobj = obj
            best_eta = eta
        for j in range(0,cols,1):
            w[j] -= (eta*dellf[j])

    eta = best_eta

    for j in range(0,cols,1):
        w[j] += (eta*dellf[j])
    error = 0
    lc = 0
    for i in range(0,rows,1):
        if trainlabels.get(i)!=None:
            lc = lc +1
            dp = dot_product(w, data[i], cols)
            temp = (trainlabels.get(i)*dp)
            if temp < 1:
                error += (1 - temp)

    c += 1
    temp = error - prev_error
    prev_error = error


nw=0
for j in range(0,cols-1,1):
    nw=nw+(w[j]**2)

nw=nw**(1/2)


d_origin=w[len(w)-1]/nw

for i in range(0, rows, 1):
    if (trainlabels.get(i) == None):
        dp = dot_product(w, data[i], cols)
        if(dp>0):
            print("1",i)
        else:
            print("0",i)
