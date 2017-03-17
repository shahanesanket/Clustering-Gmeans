from sklearn.cluster import KMeans;
from sklearn.preprocessing import scale;
from statsmodels.stats.diagnostic import normal_ad as ad_test;
import numpy as np;
import pandas as pd
import matplotlib.pyplot as plt;
from matplotlib.patches import Ellipse

#change the path in the read.csv function
inputData = pd.read_csv('hw45-r3b-test-data.csv')

def normalityTest(testData):
    fit = KMeans(n_clusters=2)
    result = fit.fit(testData)
    centers = result.cluster_centers_
    projectionvector = centers[0] - centers[1]
    projectionvector = np.matrix(projectionvector)
    projectionvector = projectionvector.transpose()
    projectedData = testData * projectionvector
    modprojectionVector = 0
    j=1
    for j in range(0,len(projectionvector)):
        modprojectionVector = modprojectionVector + (projectionvector[j]**2)
    standardizedData = projectedData/modprojectionVector
    statistic, pvalue = ad_test(standardizedData)
    return pvalue

def gmeans(X,alpha=0.0001,k=1):
    needtoinc = True
    trialData = X
    fit = KMeans(n_clusters=k)
    initresult = fit.fit(trialData)
    centers = initresult.cluster_centers_
    while(needtoinc):
        needtoinc = False
        i=0
        normTestData = trialData[initresult.labels_ == i]
        normTestData = np.matrix(normTestData)
        pvalue = normalityTest(normTestData)
        if pvalue <= alpha:
            needtoinc = True
            tempresults = KMeans(2)
            tempresults = tempresults.fit(normTestData)
            newcenters = tempresults.cluster_centers_
        else:
            newcenters = centers[i, :]

        k = centers.shape[0]
        for i in range(1, k):
            normTestData = trialData[initresult.labels_ == i]
            normTestData = np.matrix(normTestData)
            pvalue = normalityTest(normTestData)
            if pvalue <= alpha:
                needtoinc = True
                tempresults = KMeans(2)
                tempresults = tempresults.fit(normTestData)
                newcenters = np.vstack((newcenters, tempresults.cluster_centers_))
            else:
                newcenters = np.vstack((newcenters, centers[i,:]))
        centers = newcenters
        initresult = KMeans(centers.shape[0],init=centers).fit(trialData)
        centers = initresult.cluster_centers_
    print 'optimal no of clusters:',centers.shape[0]
    x = trialData.as_matrix()
    plt.figure()
    plt.scatter(x[:,0],x[:,1],c=initresult.labels_)
	plt.xlable('x1')
	plt.ylable('x2')
    for i in range(0,centers.shape[0]):
        covariance = np.cov(x[initresult.labels_==i,][:,[0,1]].transpose())
        val,vec = np.linalg.eig(covariance)
        e1 = Ellipse(xy=np.mean(x[initresult.labels_==i,][:,[0,1]].transpose(),axis = 1), width=6*np.sqrt(val[0]),height=6*np.sqrt(val[1]),angle=np.degrees(np.arctan2(*vec[1])),facecolor='none',edgecolor='blue')
        plt.gca().add_artist(e1)
    plt.show()

    plt.figure()
    plt.scatter(x[:,0],x[:,2],c=initresult.labels_)
    plt.xlable('x1')
	plt.ylable('x3')
	for i in range(0,centers.shape[0]):
        covariance = np.cov(x[initresult.labels_==i,][:,[0,2]].transpose())
        val,vec = np.linalg.eig(covariance)
        e1 = Ellipse(xy=np.mean(x[initresult.labels_==i,][:,[0,2]].transpose(),axis = 1), width=6*np.sqrt(val[0]),height=6*np.sqrt(val[1]),angle=np.degrees(np.arctan2(*vec[1])),facecolor='none',edgecolor='blue')
        plt.gca().add_artist(e1)
    plt.show()

    plt.figure()
    plt.scatter(x[:,1],x[:,2],c=initresult.labels_)
	plt.xlable('x2')
	plt.ylable('x3')
    for i in range(0,centers.shape[0]):
        covariance = np.cov(x[initresult.labels_==i,][:,[1,2]].transpose())
        val,vec = np.linalg.eig(covariance)
        e1 = Ellipse(xy=np.mean(x[initresult.labels_==i,][:,[1,2]].transpose(),axis = 1), width=6*np.sqrt(val[0]),height=6*np.sqrt(val[1]),angle=np.degrees(np.arctan2(*vec[1])),facecolor='none',edgecolor='blue')
        plt.gca().add_artist(e1)
    plt.show()

print "input data ready"
print inputData.shape

#change the alpha
gmeans(inputData,0.0001,1)