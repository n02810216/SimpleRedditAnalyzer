import numpy as np
from math import sqrt

# euclidean distance of two lists
def distance(a,b):
    sum = [0] * a.__len__()
    for i in range(a.__len__()):
        sum[i] = sqrt((a[i]-b[i])**2)
    tmp = 0
    for i in sum:
        tmp += i
    return tmp

# avg of 2D list
def avg(a):
    b = a.__len__()
    sum = [0.0] * a[0].__len__()
    for i in range(b):
        for x in range(sum.__len__()):
            sum[x] += a[i][x]
    for i in range(sum.__len__()):
        sum[i] = sum[i]/b
    return sum

# K means algorithm
def kmeans(data,k):
    m = data.__len__()
    n = data[0].__len__()
    centroids = []
    c = [-1] * m
    print m,n


    # Random centroid initialization
    rand = np.arange(data.__len__())
    np.random.shuffle(rand)
    rand = rand[0:k]
    for i in range(k):
        centroids.append(data[rand[i]])

    previous_centroids = [None] * k
    iterations = 0
    # Main loop
    while(previous_centroids != centroids):
        # Data point -> cluster assignment
        for i in range(m):
            min = 999999999999
            index = -1
            for j in range(k):
                dist = distance(data[i],centroids[j])
                if dist < min:
                    min = dist
                    index = j
            c[i]=index

        # Cluster reevaluation
        centroid_lists = []
        for l in range(k):
            centroid_lists.append([])
        for x in range(m):
            centroid_lists[c[x]].append(data[x])
        previous_centroids = centroids[:]
        for j in range(k):
            centroids[j] = avg(centroid_lists[j])
        iterations+=1
    return c
    print previous_centroids
    print centroids
    print iterations
    print time









