# This script illustrates how to use k-means clustering in
# SciKit-Learn.
from sklearn.cluster import KMeans
import numpy as np
# We create a numpy array with some data. Each row corresponds to an
# observation.
X = \
    np.array(
        [[1, 2],
         [1, 4],
         [1, 0],
         [10, 2],
         [10, 4],
         [10, 0]])
# Perform k-means clustering of the data into two clusters.
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
# Show the labels, i.e. for each observation indicate the group
# membership.
kmeans.labels_
# Ifyou have two new observations (i.e. previously unseen by the
# algorithm), to which group would they be assigned?
kmeans.predict(
    [[0, 0],
     [12, 3]])
# Show the centers of the clusters as determined by k-means.
kmeans.cluster_centers_
