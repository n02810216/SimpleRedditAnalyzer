from kmeans import *
import time


def main():


    # Copy data to 2D list
    file = "Hepta.lrn"
    with open(file) as f:
        content = f.readlines()
    content = [x.strip('\n') for x in content]
    content = [x.replace('\t',' ') for x in content]
    data = []
    for i in content:
        data.append(i.split(' '))



    # Trim data
    for i in range(data.__len__()):
        for x in range(data[0].__len__()):
            data[i][x] = data[i][x][0:6]
    # Cast data to floats
    for i in range(data.__len__()):
        for x in range(data[0].__len__()):
            data[i][x] = float(data[i][x])
    # Remove IDs
    for i in range(data.__len__()):
        data[i] = data[i][1:]
    print data
    # Subset data for testing
    #data = data[0:100]

    k = 4

    # Run K Means
    c = kmeans(data,k)

    for i in range(data.__len__()):
        data[i].append(c[i])
        print data[i]

    clustered_data=[]
    for i in range(k):
        clustered_data.append([])

    for i in range(data.__len__()):
        clustered_data[c[i]].append(data[i])

    print data.__len__()
    print clustered_data[0].__len__()
    print clustered_data[1].__len__()
    print clustered_data[2].__len__()
    print clustered_data[3].__len__()

    # Write to file
    output = open("clustered_data.txt",'w')
    output.write('x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4 \n')
    for i in range(clustered_data.__len__()):
        for x in range(clustered_data[i].__len__()):
            for z in range(i*3):
                output.write(', ')
            output.write(str(clustered_data[i][x]).strip('[').strip(']') + '\n')


    output.close()




if __name__=="__main__":
    main()
