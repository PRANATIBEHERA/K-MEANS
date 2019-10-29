
import numpy as np
from sklearn.cluster import KMeans

read_file=open("BCLL.txt",'r')
read_content= read_file.read()
all_data= read_content.splitlines()
#print (all_data)
No_data_points=len(all_data)
print ("Number of the data points ", No_data_points)
features = all_data[0].split("\t")
print ("features of the data points ", features)

No_of_dimension = len(features)

print ("Number the dimensions", No_of_dimension)
a=np.zeros((No_data_points,No_of_dimension-2))
counter = 0

for lines in all_data[1: ]:
    values=lines.split('\t')[2:No_of_dimension]
#    print (values)
    for i in range(0,(No_of_dimension-2)):
        a[counter][i]= values[i]
    counter+=1



import os     
def eucledianDistance(arg1,arg2):
    distance=0
    distanceRoot=0
    for i in range(len(arg1)):
        distance= distance + (arg1[i]-arg2[i])**2
    distanceRoot=(distance)**0.5
    return distanceRoot
def toleranceLevel(arg1,arg2):
    level=0
    for i in range(len(arg1)):
        level= level + abs(((arg2[i]-arg1[i])/arg1[i]))
    return level


from random import randrange
n=int((No_data_points)**0.5)
print("Square root no is",n)
for i in range(0,10):
    iteration=i
    ncluster=randrange(2,n)
    print("Random no is",ncluster)
    kmeans = KMeans(n_clusters=ncluster)
    print (kmeans)
    np.random.seed(1)
    newArray=np.zeros((No_data_points,No_of_dimension-2))  
    #K means will work till max-iterations or tolerance level convergence
#    for i in range(0,kmeans.max_iter) :
    for m in range(0,3) :
        centroids=np.zeros((ncluster,No_of_dimension-2))  
        centroidsNew=np.zeros((ncluster,No_of_dimension-2))
        for j in range(0,ncluster):
            centroids[j]=a[j]
        distances=np.zeros((ncluster))
        for k in range(0,No_data_points):
            for j in range(0,ncluster):
                distances[j]=eucledianDistance(a[k],centroids[j])
            minIndex = np.argmin(distances)
            filename_cluster="Cluster_number_"+ str(iteration)+"\Cluster_ "+ str(minIndex) + ".txt"
            os.makedirs(os.path.dirname(filename_cluster),exist_ok=True)
            with open(filename_cluster,"a+") as f1:
                np.savetxt(f1,np.array(a[k]),delimiter='\n', newline='\t' )
                f1.write("\n")

        for j in range(0,ncluster):      
            counter = 0
            filename_cluster="Cluster_number_"+ str(iteration)+"\Cluster_ "+ str(j) + ".txt"
            f= open(filename_cluster,"r+")
            read_content= f.read()
            all_cluster_points= read_content.splitlines()
            No_cluster_points=len(all_cluster_points)
            cluster_datapoints=np.zeros((No_cluster_points,No_of_dimension-2))
            for lines in all_cluster_points:
                values=lines.split('\t')
                for p in range(0,(No_of_dimension-2)):
                    cluster_datapoints[counter][p]= values[p]
                counter+=1
            centroidsNew[j]=np.mean(cluster_datapoints,axis=0,keepdims=1)
            f.close();
        for j in range(0,ncluster): 
#            if m < (kmeans.max_iter-1) : 
            if m < 2 : 
                filename_cluster="Cluster_number_"+ str(iteration)+"\Cluster_ "+ str(j) + ".txt"
                if os.path.exists(filename_cluster):
                    os.remove(filename_cluster)
                else:
                    print("The file does not exist")  
        convergence=np.zeros((1,ncluster))
        for l in range(0,ncluster):
            x1 = centroids[l]
            x2 = centroidsNew[l]
            print("Old Centroid",centroids[l])
            print("New Centroid",centroidsNew[l])
            level=toleranceLevel(x1,x2)
#            print("level",level)
            if  level>0.001 :
                convergence = 0
                break;
            else:      
                convergence = 1
        if convergence :
            print("break")
            break