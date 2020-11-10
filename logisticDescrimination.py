
import sys
import random
import math

def dotProduct(a, b):
    sum = 0
    for i in range(0, cols, 1):
        sum += a[i] * b[i]
    return sum


def sigmoid(x):
    return 1.0/(1+math.exp(-x))

 
theta = 0.0000001        
#stopping_cond = 0.001          # for climate data

datafile = sys.argv[1]
fdata = open(datafile, 'r')
data = []
l = fdata.readline()

# Read Data file
while (l != ''):
    r = l.split()
    l2 = []
    for j in range(0, len(r), 1):
        l2.append(float(r[j]))
    l2.append(float(1))
    data.append(l2)
    l = fdata.readline()

rows = len(data)
cols = len(data[0])
print("rows=", rows, " cols=", cols)

fdata.close()

#read training labels 

labelfile = sys.argv[2]
flabel = open(labelfile,'r')
trainlabels = {}
n = [0,0]
l = flabel.readline()
while (l != ''):
    r = l.split()
    trainlabels[r[1]] = int(r[0])
    l = flabel.readline()
    n[int(r[0])] += 1

flabel.close()

w_vector = []
for j in range(0, cols, 1):    
    w_vector.append(0.02 * random.random() - 0.01)


eta = 0.01  
error = rows * 10
difference = 1
count = 0


while ((difference) > theta):
    dellf = [0] * cols
    for j in range(0, rows, 1):
        if (trainlabels.get(str(j)) != None):
            dp = dotProduct(w_vector, data[j])
            expo = (trainlabels.get(str(j))) - (1 / (1 + (math.exp(-1 * dp))))
            for k in range(0, cols, 1):
                dellf[k] += (expo) * data[j][k]
                
    

    for j in range(0, cols, 1):
        w_vector[j] = w_vector[j] + eta * dellf[j]
    previous = error
    error = 0
    
    # compute loss
  
    for j in range(0, rows, 1):
        if (trainlabels.get(str(j)) != None):
            try:
                sig = sigmoid(dotProduct(w_vector, data[j]))
            except OverflowError:
                sig = 1
            if (sig <= 0 or sig == 1):
                continue
            error += ((-1*trainlabels.get(str(j))*math.log((sigmoid(dotProduct(w_vector, data[j])))) - ((1-trainlabels.get(str(j)))*math.log(1-sigmoid(dotProduct(w_vector, data[j]))))))            
    difference = abs(previous - error)


ld = 0
for i in range(0, (cols - 1), 1):
    ld += w_vector[i] ** 2
print ("wvector ", w_vector)
ld = math.sqrt(ld)
print("||w||=" + str(ld))
d_org = (w_vector[len(w_vector) - 1] / ld)
print ("Distance to origin = " + str(d_org))


# calc of prediction 
for i in range(0, rows, 1):
    if (trainlabels.get(str(i)) == None):
        dp = dotProduct(w_vector, data[i])
        if (dp > 0):
            print("1 " + str(i))
        else:
            print("0 " + str(i))