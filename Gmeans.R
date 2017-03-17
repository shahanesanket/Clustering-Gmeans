#setwd('C:/Users/Sanket Shahane/Documents/R/R files/')

#change the path in read.csv function to appropriate input file path
input = read.csv("hw45-r3b-test-data.csv")

normalitytest <- function(testData){
  set.seed(1000)
  result <- kmeans(testData,2)
  projectionVector <- result$centers[1,] - result$centers[2,]
  modprojectionVector = 0
  j=1
  for(j in 1:length(projectionVector)){
    modprojectionVector = modprojectionVector + (projectionVector[j]**2)
  }
  projectionVector <- data.matrix(projectionVector)
  projectedData <- testData %*% projectionVector
  standardizedData <- projectedData / modprojectionVector
  normalityResult <- ad.test(standardizedData)
  return(normalityResult$p.value)
}

Gmeans <- function(X,alpha=0.0001,k=1){
  set.seed(100)
  library(nortest)
  needtoinc = TRUE
  trialdata<-X
  initresult=kmeans(trialdata,k)
  centers = initresult$centers
  while(needtoinc)
  {
    needtoinc = FALSE
    k = nrow(centers)
    newcenters = matrix(NA,0,ncol = dim(centers)[2])
    for (i in 1:k) {
      clusterframe <- data.frame(initresult$cluster)
      opdata <- cbind(X,clusterframe)
      normtestdata <- opdata[which(opdata[,'initresult.cluster']==i),- length(opdata)]
      normtestdata <- data.matrix(normtestdata)
      if(dim(normtestdata)[1]<=7){
        #only one cluster
      }
      normtest.pvalue <- normalitytest(normtestdata)
      if(normtest.pvalue<=alpha)
      {
        needtoinc=TRUE
        tempresult = kmeans(normtestdata,2)
        newcenters = rbind(newcenters,tempresult$centers)
      }
      else{
        newcenters = rbind(newcenters,centers[i,])
      }
    }
    centers = newcenters
    initresult = kmeans(trialdata,centers = centers)
    centers = initresult$centers
  }
  print('Optimal number of clusters is:')
  print(dim(centers)[1])
  
  library(ellipse)
  trialdata <- cbind(trialdata,initresult$cluster)
  plot(trialdata$x1,trialdata$x2,col=initresult$cluster,pch=20,xlab = 'X1',ylab = 'X2',main = 'Scatter Plot X1,X2')
  points(initresult$centers[,1],initresult$centers[,2],pch=20,col='orange')
  for(i in seq(1,dim(centers)[1],1)){
    clusterData <- trialdata[which(trialdata[,ncol(trialdata)]==i),c(1,2)]
    lines(ellipse(cov(clusterData),centre=c(initresult$centers[i,1],initresult$centers[i,2]),level=0.95),col='blue',type = 'l')
  }
  plot(trialdata$x1,trialdata$x3,col=initresult$cluster,pch=20,xlab = 'X1',ylab = 'X3',main = 'Scatter Plot X1,X3')
  points(initresult$centers[,1],initresult$centers[,3],pch=20,col='orange')
  for(i in seq(1,dim(centers)[1],1)){
    clusterData <- trialdata[which(trialdata[,ncol(trialdata)]==i),c(1,3)]
    lines(ellipse(cov(clusterData),centre=c(initresult$centers[i,1],initresult$centers[i,3]),level=0.95),col='blue',type = 'l')
  }
  plot(trialdata$x2,trialdata$x3,col=initresult$cluster,pch=20,xlab = 'X2',ylab = 'X3',main = 'Scatter Plot X2,X3')
  points(initresult$centers[,2],initresult$centers[,3],pch=20,col='orange')
  for(i in seq(1,dim(centers)[1],1)){
    clusterData <- trialdata[which(trialdata[,ncol(trialdata)]==i),c(2,3)]
    lines(ellipse(cov(clusterData),centre=c(initresult$centers[i,2],initresult$centers[i,3]),level=0.95),col='blue',type = 'l')
  }
}
input = data.frame(input)
Gmeans(input,0.0001,1)