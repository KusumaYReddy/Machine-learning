import sys
import os

#datafile = sys.argv[1]
#f = open(datafile)
f = open ("C:/Users/Kusuma/OneDrive/Documents/testBayes.data")
data = []
i = 0
l = f.readline()

##read data##

while(l != ''):
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    data.append(l2)
    l = f.readline()
rows = len(data)
cols = len(data[0])
f.close()
print(data)

##read lables ##
#labelfile = sys.argv[2]
f = open("C:/Users/Kusuma/OneDrive/Documents/trainlabels.txt")
trainlabels = {}
n = [0,0]
l = f.readline()


while(l != ''):
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    l = f.readline()
    n[int(a[0])] += 1

######compute means###

m0 = []
for j in range(0, cols, 1):
    m0.append(0)
m1 = []
for j in range(0, cols, 1):
    m1.append(0)

for i in range(0, rows, 1):
    if(trainlabels.get(i) !=None and trainlabels[i] == 0):
        for j in range(0, cols, 1):
            m0[j] = m0[j] + data[i][j]
    if(trainlabels.get(i) !=None and trainlabels[i] == 1):
        for j in range(0, cols, 1):
            m1[j] = m1[j] + data[i][j]        
for j in range(0, cols, 1):
    m0[j] = m0[j]/n[0]
    m1[j] = m1[j]/n[1]
print(m0 , m1)
##compute Variance##

v0 = []
for j in range(0, cols, 1):
    v0.append(0)
v1 = []
for j in range(0, cols, 1):
    v1.append(0)

for i in range(0, rows, 1):
    if(trainlabels.get(i) !=None and trainlabels[i] == 0):
        for j in range(0, cols, 1):
            v0[j] = v0[j] + (m0[j] - data[i][j])**2
    if(trainlabels.get(i) !=None and trainlabels[i] == 1):
        for j in range(0, cols, 1):
            v1[j] = v1[j] + (m1[j] - data[i][j])**2       
for j in range(0, cols, 1):
    v0[j] = v0[j]/n[0]
    v1[j] = v1[j]/n[1]
print (v0, v1)

#####classify unlabels points###

for i in range(0, rows, 1):
    if(trainlabels.get(i) == None):
        d0=0
        d1=0
        for j in range(0, cols, 1):
            d0 = d0 + (( m0[j] - data[i][j])**2) / (v0[j]) 
            d1 = d1 + (( m1[j] - data[i][j])**2) / (v1[j])
        if(d0<d1):
            print ("0 " , i)
        else:
            print ("1 " , i)
        print(d0,d1)
            
        
                        
        
            








    
