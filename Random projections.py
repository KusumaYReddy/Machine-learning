

import random as rnd;
import sys;

import math;
from sklearn import svm;
from sklearn import model_selection;

def dotproduct (X, Y):
    dp = 0
    for j in range(0, len(Y), 1):
        dp += X[j]*float(Y[j]);
    return dp

# Get the Inputs
datafile = sys.argv[1];
labelfile = sys.argv[2];
#testfile = sys.argv[3];

f = open(datafile ,'r');
data = [];
l = f.readline();
while(l != ''):
    a = l.split();
    l2 = [];
    for i in range(0, len(a), 1):
        l2.append(float(a[i]))
    data.append(l2);
    l = f.readline();
rows =len(data);
cols = len(data[0]);
f.close();

f = open(labelfile,'r');
trainlabels = {};
n = [];
n.append(0);
n.append(0);
l = f.readline();
while (l != ''):
    a = l.split();
    trainlabels[int(a[1])] = int(a[0]);
    l = f.readline();
    n[int(a[0])] += 1;
    if (trainlabels[int(a[1])] == 0):
        trainlabels[int(a[1])] = -1;
f.close();
err = open('Random_Hyperplane_Errors.txt', 'a+');
err.write('\n\n')
err.write(datafile);
# Labels Only
labels = [];
for label in trainlabels:
    labels.append(trainlabels.get(label));
# Progam
odata = [];
for i in range(0, rows, 1):
    if(trainlabels.get(i) != None):
        odata.append(data[i]);

ntrain = [];
planes = [10, 100, 1000, 10000];
for k in planes:
    print('\nFor K = {} Random Planes:'.format(k));
    for i in range(0, k, 1):
        ltrain = [];
        w = [];
        for j in range(0, cols, 1):
            w.append(0);
        for j in range(0, cols, 1):
            w[j] = w[j] + rnd.uniform(1, -1);
        for i in range(0, rows, 1):
            if(trainlabels.get(i) != None):
                dp = 0;
                dp = dotproduct(w, data[i]);
                s = int(math.copysign(1, dp));
                v = int((s+1)/2);
                ltrain.append(v);
        ntrain.append(ltrain);
        ntraint = zip(*ntrain);
        traindata = [];
        for r in ntraint:
            traindata.append(r);
    clf = svm.LinearSVC(C = 0.1, max_iter = 10000);
    scr = model_selection.cross_val_score(clf, traindata, labels, cv = 5);
    scr[:] = [1 - x for x in scr];

    oscr = model_selection.cross_val_score(clf, odata, labels, cv = 5);
    oscr[:] = [1 - x for x in oscr];

    print('Error for the New Features Data is {}\nMean Error for the New Features Data is {}'.format(scr, scr.mean()));
    print('Error for the Original Features Data is {}\nMean Error for the Original Features Data is {}'.format(oscr, oscr.mean()));


    err.write('\n\nFor K = {} Random Planes:'.format(k));
    err.write('\nError for the New Features Data is {}\nMean Error for the New Features Data is {}'.format(scr, scr.mean()))
    err.write('\nError for the Original Features Data is {}\nMean Error for the Original Features Data is {}'.format(oscr, oscr.mean()))
err.close();
