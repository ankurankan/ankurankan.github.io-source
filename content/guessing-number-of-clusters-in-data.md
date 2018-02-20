---
layout: post
title: Guessing Number of Clusters in Data
date: 2014-10-11 08:39
comments: true
categories: Clustering, Machine Learning, KMeans 
---
I will start with stating a way to guess the number of clusters and then prove it.

```
Plot the total error (sum of distance between point and its cluster centre) vs number of clusters.
The point where the slope of this curve changes very steeply is the number of clusters in the data.
```

Now I will prove my point. Let's write a few functions to calculating error and plotting them.

```python3
import numpy as np
def total_error(X, cluster_centers, predicted_clluster):
    error = 0
    for point_index in range(X.shape[0]):
        error += np.linalg.norm(X[point_index] - cluster_centers[predicted_cluster[point_index]])
    return error
```
Another function to plot the `total_error` vs `number of clusters`:
```python3
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
def error_vs_cluster(X, max_clusters=100):
    err_arr = []
    for i in range(1, max_clusters):
        kmeans = KMeans(n_clusters=i, n_jobs=-1)
        kmeans.fit(X)
        err_arr.append(total_error(X, kmeans.cluster_centers_, kmeans.labels_))
    
    plt.plot(np.arange(1, max_clusters), err_arr)
```
Now let's generate some data:
```python3
from sklearn.datasets import make_blobs
X, y = make_blobs(centers=3, cluster_std=0.1)
```
I have created clusters with very less standard deviation because this shows things most clearly.
I will later disscuss with clusters having high deviation.
Let's plot this:
```python3
error_vs_cluster(X)
```
You can clearly see here that there's a steep change in the slope at `3` which is the number of clusters
 in our data.

If we try to think intuitively what is happening here. We start with trying to fit all the points in a single cluster. So we get a cluster center in between of all the clusters and the error is very high. As the number of clusters increase the error term keeps on decreasing.
After the perfect fit (ie 3) when the we try to increase the number of clusters the error still decreases but very slowly because we are trying to divide the cluster and there will always be points that will decrease the error but its effect will be very less. The error will keep on decreasing until we have a single cluster for each individual point (ie when the error is 0).

Now let's see what happens when we use data with much higher standard deviation.

```python3
X, y = make_blobs(centers=4, cluster_std=1)
error_vs_cluster(X)
```
So now we get a curve where the slope changes slowly and we don't have a very sharp change in the slope
as we saw in the case when we had data with less standard deviation.

So, why is this happening?
Let's plot the data and see:
```python3
plt.scatter(X[:, 0], X[:, 1], c=y)
```
As we can see here we don't have that clear distinction in the number of clusters. So when we increase the number of clusters from 3 to 4 we can still have a point that would decrease the error term by a 
good amount.
But in this case also you can see that there is a relatively more steep change in slope at 3.


